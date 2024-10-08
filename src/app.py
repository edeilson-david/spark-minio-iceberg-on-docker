from minio import Minio
from minio.error import S3Error
from pyspark.sql import SparkSession

if __name__ == '__main__':

    # Configurações do MinIO
    minio_url = "172.20.0.5:9000"
    access_key = "minioadmin"
    secret_key = "minioadmin"
    bucket_name = "lakehouse"

    # Inicializa o cliente MinIO
    client = Minio(minio_url,
                   access_key=access_key,
                   secret_key=secret_key,
                   secure=False)

    # Cria o bucket
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' criado com sucesso.")
        else:
            print(f"Bucket '{bucket_name}' já existe.")
    except S3Error as e:
        print(f"Erro ao criar bucket: {e}")

    # Dependências
    packages = [
        "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1",
        "org.apache.iceberg:iceberg-hive-runtime:1.6.1",
        "org.apache.hadoop:hadoop-common:3.3.4",
        "org.apache.hadoop:hadoop-aws:3.3.4",
        "com.amazonaws:aws-java-sdk-bundle:1.12.262"
    ]

    # Criando Spark Session
    spark = (
        SparkSession.builder.appName("ExampleAppSpark")
        .master("spark://172.20.0.2:7077")
        .config("spark.jars.packages", ",".join(packages))
        .config("spark.hadoop.fs.s3a.endpoint", "http://172.20.0.5:9000")
        .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
        .config("spark.hadoop.fs.s3a.path.style.access", True)
        .config("spark.hadoop.fs.s3a.fast.upload", True)
        .config("spark.hadoop.fs.s3a.multipart.size", 104857600)
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
        .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkCatalog")
        .config("spark.sql.catalog.spark_catalog.type", "hadoop")
        .config("spark.sql.catalog.spark_catalog.warehouse", "s3a://lakehouse/")
        .enableHiveSupport()
        .getOrCreate()
    )

    sc = spark.sparkContext
    sc.setLogLevel("INFO")

    # Dataframe de exemplo
    data = [("James", "Sales", "NY", 90000, 34, 10000),
            ("Michael", "Sales", "NY", 86000, 56, 20000),
            ("Robert", "Sales", "CA", 81000, 30, 23000),
            ("Maria", "Finance", "CA", 90000, 24, 23000),
            ("Raman", "Finance", "CA", 99000, 40, 24000),
            ("Scott", "Finance", "NY", 83000, 36, 19000),
            ("Jen", "Finance", "NY", 79000, 53, 15000),
            ("Jeff", "Marketing", "CA", 80000, 25, 18000),
            ("Kumar", "Marketing", "NY", 91000, 50, 21000)
            ]

    schema = ["name", "department", "state", "salary", "age", "bonus"]
    df = spark.createDataFrame(data=data, schema=schema)

    df.write.format("iceberg").mode("append").saveAsTable("spark_catalog.db.departament")

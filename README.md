# Cluster Spark com MinIO e Apache Iceberg utilizando Docker Compose

Este projeto provisiona um cluster Apache Spark com MinIO e Apache Iceberg utilizando Docker Compose para um ambiente de
estudo. Ele permite processar grandes volumes de dados e gerenciar armazenamento em object storage de forma
eficiente, combinando a robustez do Spark com a flexibilidade do Minio e a confiabilidade do Apache Iceberg.

## Tecnologias Utilizadas

- **Apache Spark**: Plataforma de computação distribuída para processamento de grandes volumes de dados.
- **MinIO**: Armazenamento de objetos S3 compatível para armazenamento e recuperação de grandes volumes de dados.
- **Iceberg**: Camada de armazenamento unificada que traz confiabilidade e desempenho para dados no Apache Spark.
- **Docker**: Para containerização de serviços.
- **Docker Compose**: Para orquestração e provisionamento do ambiente.
- **Python**: Linguagem de programação utilizada para implementar scripts.

## Pré-requisitos

Certifique-se de ter conhecimento básico e a instalação na sua máquina dos seguintes:

- [Ubuntu 20.04](https://ubuntu.com/desktop/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Poetry](https://python-poetry.org/)
- [Python 3.11](https://www.python.org/)

## Serviços Disponíveis

### Apache Spark

Apache Spark é um framework para processamento de dados em larga escala que permite computação distribuída. Neste
ambiente, o cluster contém um Master e dois Workers.

**Spark Master**:

- URL: `spark://172.20.0.2:7077`
- Interface Web: `http://172.20.0.2:8080`

**Spark Workers**:

- Cada worker se conecta automaticamente ao Master.
- Interface Web do Worker: `http://172.20.0.3:8081` e `http://172.20.0.4:8082`

### MinIO

MinIO é um serviço de armazenamento de objetos compatível com o Amazon S3, permitindo armazenar e recuperar dados de
forma eficiente.

- **Interface Web**: `http://172.20.0.5:9000`
- **Credenciais padrão**:
    - **Access Key**: minioadmin
    - **Secret Key**: minioadmin

#### Apache Iceberg

Apache Iceberg é um formato de tabela open-source projetado para o gerenciamento de grandes volumes de dados em Data
Lake. Oferece recursos como versionamento, time travel, particionamento dinâmico e suporte a transações ACID e outros
funcionalidades. Se integra com diversas engine como Apache Spark, Flink, Presto e Trino.

## Instalação

Em um terminal de linha de comando, realize as seguintes etapas:

1. Crie uma pasta de trabalho e acessa-o, por exemplo:
   ```bash
   cd ~
   mkdir workspace
   cd workspace

2. Clone este repositório:
   ```bash
   git clone https://github.com/edeilson-david/spark-minio-iceberg-on-docker.git

3. Navegue até o diretório do projeto:
   ```bash
   cd spark-minio-iceberg-on-docker

4. Provisione e inicialize os serviços com Docker Compose:
   ```bash
   docker-compose up -d

5. Verifique se todos os serviços estão em execução:

- Spark Master na URL: `http://172.20.0.2:8080`
- MinIO na URL: `http://172.20.0.5:9000`

## Utilizando o Ambiente

### Processamento com Spark

Você pode enviar jobs para o cluster Spark usando a interface de linha de comando do Spark ou conectar-se a partir de
notebooks, como o **Jupyter Notebook**, para executar operações interativas.

### Armazenamento de Dados com MinIO

Você pode utilizar ferramentas como **AWS CLI** ou **mc (MinIO Client)** para armazenar e recuperar dados no MinIO.
Os dados podem ser armazenados no formato Apache Iceberg e acessados pelo Spark para processamento.

### Exemplo de Conexão ao MinIO com Apache Spark utilizando Python.

   ```bash
       packages = [
            "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1",
            "org.apache.iceberg:iceberg-hive-runtime:1.6.1",
            "org.apache.hadoop:hadoop-common:3.3.4",
            "org.apache.hadoop:hadoop-aws:3.3.4",
            "com.amazonaws:aws-java-sdk-bundle:1.12.262"
       ]

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
   ```

### Executando Script App.py

Execute os seguintes comandos no terminal de linha de comando para executar o script de exemplo:

```bash
cd ~/workspace/spark-minio-iceberg-on-docker
poetry install
poetry run python src/app.py
```

O comando acima criará e ativará um ambiente virtual Python, instalará as dependências do projeto utilizando o Poetry e
executará o script `app.py`.

## Comandos Docker

### Provisionar o Ambiente

Para provisionar e iniciar todos os serviços (Master Workers e MinIO), utilize o comando:

```bash
cd ~/workspace/spark-minio-iceberg-on-docker
docker-compose up -d
```

### Parar o Ambiente

Para **parar** os serviços sem removê-los:

```bash
cd ~/workspace/spark-minio-iceberg-on-docker
docker-compose stop
```

### Iniciar os Serviços

Caso tenha parado os serviços, você pode **iniciá-los** novamente com:

```bash
cd ~/workspace/spark-minio-iceberg-on-docker
docker-compose start
```

### Remover os Serviços

Se quiser remover os contêineres e limpar o ambiente, execute:

```bash
cd ~/workspace/spark-minio-iceberg-on-docker
docker-compose down
```

### Remover Volumes e Dados

Caso queira remover volumes e dados persistentes (como os armazenados no MinIO), adicione a flag `-V`

```bash
cd ~/workspace/spark-minio-iceberg-on-docker
docker-compose down -v
```

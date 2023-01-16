# Overview
There is a task which every admin in TOKI might upload files no matter where and those files must be processed to invoices. 
The main structure of the raw files contains the following columns:
- metering_point_id
- timestamp
- kwh

Because the files are created by humans is possible these files to have errors and these errors must be places somewhere for furher processing.
The main task is calculate on monthly basis when the admin upload the CSV file for the last month the total usage of energy, total price and average for the month.
For every day there is a service which give you a possibility to download  the price of the market with hourly granulation. To make sure the calculations are correct, we have on dalily basis to scrape this data for last date and store it somewhere for further purposes. 

# Technology Stack:

- MinioIO
- Kafka
- KafkaUI
- Schema Registry
  - SchemeRegistryUI
- AvroSchema
  - AvroSchemaUI
- DynamoDB
  - DynamoDBUI
- Python
  - Pandas
  - Boto3
  - Faust
  - Avro
  - Schema Registry
- Docker
- Docker-Compose

# Infrastructure

For the given solution I've used bare-metal services deployed through docker and docker-compose. There is a table with definitions, ports of accessing from the host and some other useful information

| Serivce | Port | Adress | Description |
| --- | --- | --- | --- |
| DynamoDB | 28000:8000 |
 | NoSQL database to ensure high demand |
| DynamodbAdmin | 28001:8001 | http://0.0.0.0:20085 | Web based interface for DynamoDB to debug and manage tables |
| Zookeeper | 2181:2181 |
 | ZooKeeper is a centralized service for maintaining configuration information, naming, providing distributed synchronization, and providing group services. |
| Kafka | 29092:29092 9092:9092 |
 | Apache Kafka is an open-source distributed event streaming platform for high-performance data pipelines |
| KafkaUI | 20085:8080 | http://0.0.0.0:20085 | Kafka Web based IU |
| SchemaRegistry | 8081:8081 |
 | Confluent Schema Registry provides a serving layer for your metadata |
| Schema Registry UI | 20082:8000 | http://0.0.0.0:20082 | Web Based Schema Registry UI |
| Minio | 20084:9090 | http://0.0.0.0:20084 | Alternative of s3 for bare metal solutions compatible with AWS cli and boto |


# Solution

The solution is divided by multiple microservices developed with the python framework called faust. It was used to consume messages from kafka and respectively to produce messages in kafka topics.

For development and testing purposes, all the agents (workers) are running in a single thread but through virtualisation or segmentation via docker, every agent might be executed and scalled independenty.

The taks is divided logically in four main steps.

- Upload to bucket called "new-files". Every worker subscribed to this topic with proper filter will validate the file and will place it in another bucket.
- The agent for uploaded files after a validation invokes SINK callback with move the files in bucket depending of the validation status:
 Respectively:
  - **valid-files**
    - Save meta information for the file in dynamoDB table
  - **mistaken-files**
    - Save meta information for the file in dynamoDB table with all found errors
- If the file is valid, there is another agent (Service) which is responsible to apply to every particular row the price rate from the market for the given period and sum the amount for the timeframe it is.
  - Because the files could comes with multiple metring\_ids, they are grouped per thiis field and they are stored separately in another bucket called: **pre-invoice-raw-files** where the structure pattern for the file tree is **{YEAR}/{MONTH}/{METERING\_ID}.csv**
- Generate invoices in JSON format for every metering ID

# Installation Instructions:

#### 1. Deploy the infrastructure you need
```bash
make up
```

> Make sure all the services are healthy. Sometime might takes longer. Wait them for min, or two after containers have been created

#### 2. Prepare all the buckets we need for the services

```bash
make buckets
```

#### 3. Prepare Virtual Python env
```bash
make venv
```

#### 4. Activate the Venv 
You’ll need to use different syntax for activating the virtual environment depending on which operating system and command shell you’re using.

On Unix or MacOS, using the bash shell: 
```bash
source /path/to/venv/bin/activate
```

On Unix or MacOS, using the csh shell: 
```bash
source /path/to/venv/bin/activate.csh
```

On Unix or MacOS, using the fish shell:
```bash
source /path/to/venv/bin/activate.fish
```

On Windows using the Command Prompt:
```bash
path\to\venv\Scripts\activate.bat
```
On Windows using PowerShell:
```bash
path\to\venv\Scripts\Activate.ps1
```

#### 5. Install PyPI libraries
```bash
make pypi-install 
```

#### 6. Install Toki as Module
```bash
make install
```

#### 7. RUN toki
```bash
make run
```

#### 8. Extract the prices for year ago. Please execute this in separate TTY
```bash
make prices
```
> Make sure VENV is activated for the last two command.

# Workflow

1. Get in to minio using the URL from the table above
2. Log in with admin / Eemi8cah
3. Go to  Object browser
4. Select new-files bucket and upload valid csv
5. If the file is not valid will be moved in the bucket: mistaken-files

# Changelog

Backlog: https://docs.google.com/spreadsheets/d/1DKRkmIwxZobCtgwgNI5tsZz_SghfYXiCWJ-O3SbAROM/edit?usp=sharing

- [x] TOK-1  As Developer,  I have to create initial boilerplate which will make me eligible to develop python applications 
- [x] TOK-6	As User, I want to be able to upload CSV file to a storage
- [x] TOK-7	As Developer, I have to create an mechanism to download all the price rates from the exchange to be able afterwirds to be used in the invocies
- [x] TOK-8	As Business Admin, I Want to be able to upload CSV with data to multiple customers either single customer and the data must be processed well
- [x] TOK-9	As Developer, I have to subscribe for new pre-invoice files and generate invoices in s3 bucket
- [ ] TOK-10 Create API endpoints for some reporting
- [ ] TOK-21 As Developer, I have to ensure the code with unit testing
- [ ] TOK-22 As Developer, I have to prepare docker-composition for microservicing
- [ ] TOK-23 I have to setup a CI/CD

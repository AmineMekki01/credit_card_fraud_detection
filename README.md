# credit_card_fraud_detection

Real time credit card fraud detection

## 1. Run with docker

ll

## 2. Testing Locally

To test the app locally, you first need to download and install Kafka and Cassandra.

### 2.1 Setup kafka

#### 2.1.1 download kafka

Download Kafka from the following link:

```
https://kafka.apache.org/downloads
```

After downloading, navigate to the Kafka folder. Ensure the `bin` folder is in the current directory.

#### 2.1.1 Start Zookeeper

Run the following command:

```
bin/zookeeper-server-start.sh config/zookeeper.properties
```

#### 2.1.2 Start kafka server

Run the following command:

```
bin/kafka-server-start.sh config/server.properties
```

#### 2.1.3 Creating a kafka topic

Run the following command:

```
kafka-topics.sh --create --topic transactions --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### 2.2 Running Cassandra

#### 2.2.1 Download Cassandra

Download Cassandra from the following link:

```
https://cassandra.apache.org/_/download.html
```

After installing, access the Cassandra shell:

```
cqlsh
```

#### 2.2.2 Create KEYSAPCE

Run the following commands:

```
CREATE KEYSPACE fraud_detector WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};
USE fraud_detector ;
```

#### 2.2.3 Create a table

Run the following commands:

```
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    status TEXT
);
```

The `status` indicates whether the transaction is fraudulent or not.

### 2.3 Setting up Front end

I am using react for the front end, so you should have node installed in you machine. You can do that by doing the following :

```
https://nodejs.org/en/download/prebuilt-installer/current
```

After downloading, ensure Node.js is added to your PATH. Verify the installation by running:

```
npm -v
```

Navigate to the `frontend` folder and install the required packages:

```
npm install 
```

Run the development server:

```
npm start
```

The React app should run on `http://localhost:3000` by default.

### 2.4 Setting up the backend.

Navigate to the `backend` folder.

#### 2.4.1 create a conda env

Run the following command:

```
conda create -n credit_fraud python=3.11 -y
```

#### 2.4.2 install all requirements

Run the following command:

```
pip install -r requirements.txt
```

#### 2.4.3 create .env

Create a `.env` file in the main project folder (`credit_card_fraud_detection`) with the following content:

```
PYTHONPATH="/path_to_the_main_folder/credit_card_fraud_detection"

CASSANDRA_HOST=localhost

CASSANDRA_KEYSPACE=fraud_detector

KAFKA_BROKER=localhost:9092
```

#### 2.4.4 Run the backend

Ensure Kafka is running (refer to previous steps).

Export the PYTHONPATH before running the app (replace `path_to_main_directory` with the actual path):

```
export PYTHONPATH="path_to_main_directory/credit_card_fraud_detection"
```

Run the backend:

```
uvicorn cc_fraud_detector.main:app --reload --host 0.0.0.0 --port 8000
```


Now you also need to run the Kafka consumer so it consumes the transactions and triggers prediction.

You need to open another terminal, navigate to the `backend` folder, and run the following command:

```
python -m cc_fraud_detector.api.services.kafka_consumer
```

If you face any errors, run the export command again:

```

export PYTHONPATH="path_to_main_directory/credit_card_fraud_detection"
```

Now you can use the web app to simulate a transaction and wait for the prediction.

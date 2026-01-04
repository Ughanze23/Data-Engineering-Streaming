# Real-Time Ride Booking Streaming Pipeline

A comprehensive data engineering project demonstrating a real-time streaming pipeline for ride-sharing booking data using modern big data technologies.

## Overview

This project implements an end-to-end real-time data streaming pipeline that ingests ride booking data through a REST API, processes it using Apache Spark Structured Streaming, stores it in MongoDB, and visualizes the data in real-time using an interactive Streamlit dashboard.

## Architecture

![alt text](image.png)
The pipeline consists of the following components:

1. **FastAPI Ingestion Service** - REST API endpoint to receive ride booking data
2. **Apache Kafka** - Distributed streaming platform for message buffering
3. **Apache Zookeeper** - Coordination service for Kafka
4. **Apache Spark** - Stream processing engine with Jupyter notebook interface
5. **MongoDB** - NoSQL database for storing processed data
6. **Mongo Express** - Web-based MongoDB admin interface
7. **Streamlit Dashboard** - Real-time analytics and visualization dashboard

## Technology Stack

- **FastAPI** - Modern Python web framework for building APIs
- **Apache Kafka** (v7.5.0) - Distributed event streaming platform
- **Apache Spark** - Unified analytics engine for large-scale data processing
- **MongoDB** - Document-oriented NoSQL database
- **Streamlit** - Framework for creating data dashboards
- **Docker & Docker Compose** - Containerization and orchestration
- **Python** - Primary programming language
- **Plotly** - Interactive visualization library

## Project Structure

```
Data-Engineering-Streaming-main/
├── document-streaming/
│   ├── api/
│   │   ├── api-ingest/           # FastAPI ingestion service
│   │   │   ├── app/
│   │   │   │   └── main.py       # API endpoints and Kafka producer
│   │   │   └── requirements.txt
│   │   └── api-client/           # Client to send test data
│   │       ├── api-client.py     # Script to post data to API
│   │       └── transformer.py
│   ├── ApacheSpark/              # Spark streaming notebooks
│   │   ├── 01-spark-streaming-srckafka-dstkafka.ipynb
│   │   └── 02-spark-streaming-srckafka-dstmongodb.ipynb
│   ├── dashboard/                # Streamlit dashboard
│   │   ├── rides-dashboard.py
│   │   └── requirements.txt
│   ├── docker-compose.yml        # Service orchestration
│   └── pipeline Architecture.png
└── README.md
```

## Data Flow

1. **Ingestion**: Ride booking data is sent via HTTP POST to the FastAPI endpoint
2. **Streaming**: FastAPI produces messages to Kafka topic `ride-bookings`
3. **Processing**: Spark Structured Streaming consumes from Kafka, processes the data
4. **Storage**: Processed data is written to MongoDB collection
5. **Visualization**: Streamlit dashboard reads from MongoDB and displays real-time analytics

## Data Schema

The ride booking data includes:

- Date & Time
- Booking ID
- Booking Status (Completed, Cancelled, etc.)
- Customer ID
- Vehicle Type (eBike, Car, etc.)
- Pickup & Drop Locations
- Booking Value
- Ride Distance
- Driver Ratings
- Customer Rating
- Payment Method

## Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ (for running API client locally)
- At least 8GB RAM available for Docker containers

## Getting Started

### 1. Start the Services

Navigate to the project directory and start all services using Docker Compose:

```bash
cd document-streaming
docker-compose up -d
```

This will start the following services:

| Service | Port | Description |
|---------|------|-------------|
| API Ingest | 80 | FastAPI ingestion endpoint |
| Kafka | 9093 | Kafka broker (external) |
| Zookeeper | 2181 | Kafka coordination |
| Spark/Jupyter | 8888 | Jupyter notebook for Spark |
| MongoDB | 27017 | Database |
| Mongo Express | 8081 | MongoDB admin UI |
| Streamlit Dashboard | 8501 | Analytics dashboard |

### 2. Access the Services

- **API Documentation**: http://localhost:80/docs
- **Jupyter Notebook**: http://localhost:8888 (check logs for token)
- **Mongo Express**: http://localhost:8081
  - Username: `admin`
  - Password: `tribes`
- **Streamlit Dashboard**: http://localhost:8501

### 3. Set Up Spark Streaming

1. Access Jupyter notebook at http://localhost:8888
2. Navigate to the notebook: `02-spark-streaming-srckafka-dstmongodb.ipynb`
3. Execute the cells to start the Spark streaming job
4. The job will consume from Kafka and write to MongoDB

### 4. Send Test Data

Use the API client to send test ride booking data:

```bash
cd api/api-client
python api-client.py
```

The client reads from a data file and posts records to the ingestion API with a configurable delay between requests.

### 5. View the Dashboard
<img width="1762" height="1216" alt="image" src="https://github.com/user-attachments/assets/3f9639b1-ae88-4881-aa8d-57c8c20c9717" />

Navigate to http://localhost:8501 to see the real-time dashboard with:

- Total bookings count
- Average booking value
- Average ride distance
- Bookings by vehicle type
- Booking status distribution
- Payment method breakdown
- Time-series booking trends

The dashboard auto-refreshes every 30 seconds to show the latest data.

## API Usage

### Ingest Ride Booking

**Endpoint**: `POST /ride-booking`

**Request Body**:
```json
{
  "Date": "2024-03-23",
  "Time": "12:29:38",
  "Booking ID": "CNR5884300",
  "Booking Status": "Completed",
  "Customer ID": "CID1982111",
  "Vehicle Type": "eBike",
  "Pickup Location": "Palam Vihar",
  "Drop Location": "Jhilmil",
  "Booking Value": 250.50,
  "Ride Distance": 15.3,
  "Driver Ratings": 4.5,
  "Customer Rating": 4.8,
  "Payment Method": "Credit Card"
}
```

**Response**: `201 Created`

## Configuration

### MongoDB Connection

Default MongoDB connection:
- Host: `localhost:27017`
- Username: `root`
- Password: `example`
- Database: `uberstreaming`
- Collection: `bookings`

### Kafka Configuration

- Bootstrap Servers: `localhost:9093` (external) or `kafka:9092` (internal)
- Topic: `ride-bookings`

## Development

### Building Custom Images

If you need to build custom images for the API or dashboard:

```bash
# Build API image
cd api/api-ingest
docker build -t api-ingest .

# Build dashboard image
cd dashboard
docker build -t dashboard .
```

### Installing Dependencies Locally

For local development:

```bash
# API dependencies
pip install -r api/api-ingest/requirements.txt

# Dashboard dependencies
pip install -r dashboard/requirements.txt
```

## Monitoring

### Check Kafka Topics

Access the Kafka container:
```bash
docker exec -it <kafka-container-id> bash
kafka-topics --list --bootstrap-server localhost:9092
```

### View Spark Streaming Logs

Check Spark UI at: http://localhost:4040 (when streaming job is running)

### MongoDB Data

Access Mongo Express at http://localhost:8081 to view collections and documents.

## Troubleshooting

### Kafka Connection Issues

If services can't connect to Kafka, ensure:
- Kafka and Zookeeper containers are running
- Use `kafka:9092` for internal container communication
- Use `localhost:9093` for external connections

### Spark Streaming Not Starting

- Check if Kafka topic exists
- Verify MongoDB connection string
- Review Jupyter notebook logs

### Dashboard Not Showing Data

- Ensure Spark streaming job is running
- Verify MongoDB has data in the `uberstreaming.bookings` collection
- Check MongoDB connection credentials

## Stopping the Pipeline

To stop all services:

```bash
docker-compose down
```

To remove volumes as well:

```bash
docker-compose down -v
```

## Future Enhancements

- Add authentication and authorization to API
- Implement data validation and quality checks
- Add alerting for anomalies
- Scale Kafka and Spark for production workloads
- Implement data retention policies
- Add more visualization metrics

## License

This project is for educational purposes demonstrating data engineering streaming pipelines.

## Contributing

Feel free to open issues or submit pull requests for improvements.

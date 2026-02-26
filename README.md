# ETL Data Pipeline Project

A personal end-to-end ETL (Extract, Transform, Load) project designed to showcase my skills in data engineering, cloud computing, and DevOps automation.

## Overview

This project demonstrates how to build a scalable, cost-efficient, and production-ready data pipeline, following modern Data Engineering best practices.

It simulates a real-world environment — from raw data ingestion to analytics — using AWS services (S3, Lambda, MWAA, Glue, Athena) and Terraform.

## Architecture

```
API (CoinGecko) → S3 Raw Zone → Python Transform → S3 Silver Zone → Glue Crawler → Athena (SQL Analytics)
```

## Pipeline Phases

### 1. Extraction

- Collects raw data from CoinGecko API
- Stores the data in Amazon S3 Raw Zone with date partitioning (year/month/day)
- Handles retries, request throttling, and basic validation

### 2. Transformation

- Cleans, enriches, and structures data using Python (pandas)
- Converts raw JSON into optimized Parquet format
- Implements schema enforcement and normalization
- Writes processed data into S3 Silver Zone

### 3. Catalog & Analytics

- AWS Glue Crawler auto-discovers schema
- AWS Lake Formation manages data catalog
- Amazon Athena enables SQL queries on S3 data

### 4. Orchestration

- AWS MWAA (Managed Workflows for Apache Airflow) manages the workflow
- Each ETL task runs as a DAG with logging, alerting, and retry policies
- Provides complete visibility and monitoring via Airflow UI

### 5. Infrastructure as Code

- All cloud resources (S3, MWAA, Glue, IAM) are provisioned with Terraform
- Ensures reproducible, automated, and version-controlled deployments

## Technologies

- **Language:** Python
- **Cloud:** AWS (S3, MWAA, Glue, Athena, Lake Formation)
- **IaC:** Terraform
- **Orchestration:** Apache Airflow (via AWS MWAA)
- **Format:** JSON → Parquet

🚀 ETL Data Pipeline Project

🧠 A personal end-to-end ETL (Extract, Transform, Load) project designed to showcase my skills in data engineering, cloud computing, and DevOps automation.

🌍 Overview

This project demonstrates how to build a scalable, cost-efficient, and production-ready data pipeline, following modern Data Engineering best practices.

It simulates a real-world environment — from raw data ingestion to automated orchestration — using AWS services, PySpark, and Terraform.

🔄 Pipeline Phases
🧲 1. Extraction

Collects raw data from public APIs (e.g., Alpha Vantage) or CSV files.

Stores the data in the Amazon S3 Raw Zone with proper date partitioning.

Handles retries, request throttling, and basic validation.

🧪 2. Transformation

Cleans, enriches, and structures data using PySpark.

Converts raw JSON into optimized Parquet format.

Implements schema enforcement, deduplication, and normalization.

Writes processed data into the Curated Zone of S3.

🏗️ 3. Loading

Loads curated data into Amazon Redshift using the COPY command.

Supports incremental updates and automatic schema mapping.

Enables analytical queries with SQL or BI tools.

🕹️ 4. Orchestration

Apache Airflow manages the workflow through a Dockerized environment.

Each ETL task runs as a DAG with logging, alerting, and retry policies.

Airflow UI provides complete visibility and monitoring.

☁️ 5. Infrastructure as Code

All cloud resources (S3, Redshift, IAM, VPC) are provisioned with Terraform.

Ensures reproducible, automated, and version-controlled deployments.

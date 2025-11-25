## 🚀 Overview

The client manages financial transactions and user metadata stored across two operational databases:

- MongoDB
- PostgreSQL

To improve analytics, reporting, and regulatory visibility, they needed all data centralized in Snowflake using a modern ELT workflow.

This project automates ingestion by:
1. Extracting data from MongoDB & PostgreSQL
2. Implementing timestamp-based CDC to capture only new or updated records
3. Loading CDC-filtered data into an AWS S3 data lake
4. Using Snowflake COPY INTO operations to stage data into Bronze, then transform to Silver & Gold

![architectural diagram](assets/nomba-gif.gif)


## 🏗️ Technologies Used
| Component            | Technology                                |
| -------------------- | ----------------------------------------- |
| **Source Databases** | MongoDB, PostgreSQL                       |
| **Orchestration**    | Python scripts (optionally Airflow-ready) |
| **Data Lake**        | AWS S3                                    |
| **Warehouse**        | Snowflake                                 |
| **CDC Strategy**     | Timestamp-based CDC                       |
| **Containerization** | Docker (local development)                |


## 🔐 Security Considerations

- Credentials stored using environment variables or a secrets manager
- S3 bucket has restricted IAM roles


## 📈 Outcome

This pipeline provides the fintech client with:
- A single source of truth in Snowflake
- Faster analytics and BI dashboarding
- Incremental ingestion (CDC) that reduces compute cost
- A scalable, cloud-native ELT system

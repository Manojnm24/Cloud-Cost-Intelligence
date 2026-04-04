# Cloud-Cost-Intelligence

### A cloud cost monitoring and anomaly detection dashboard built using AWS Cost Explorer API, FastAPI, and React.
### This project provides real-time AWS billing visibility, service-level breakdown, and rule-based anomaly detection to help monitor abnormal spending patterns.

## Features

- AWS Cost Explorer API integration
- Daily cost tracking
- Service-wise cost breakdown
- Rule-based anomaly detection
- Cost spike severity classification
- Interactive dashboard with charts
- Currency formatting abstraction
- Auto refresh support
- CSV export support
- JWT-based User Authentication
- Clean modular backend architecture

## Architecture Overview

```

Frontend (React)
⬇
FastAPI Backend
⬇
AWS Cost Explorer API
⬇
Anomaly Detection Service

The backend fetches billing data from AWS Cost Explorer, processes it, detects anomalies, and serves structured data to the frontend dashboard.

```

## Core Functionalities

1. Cost Monitoring

- Fetches daily unblended cost data
- Groups cost by AWS service
- Displays total cost trend over time
- Shows service-level cost contribution
  
2. Anomaly Detection

  Implements rule-based anomaly detection:
- Compares latest cost against baseline average
- Flags abnormal percentage increases
- Classifies severity levels
- Highlights cost spikes in UI

3. Anomaly Detection

- Drill-down modal for service-wise daily breakdown
- Displays individual AWS service contribution
- Useful for identifying cost-heavy services

## Why This Project?

### Cloud cost optimization is a real-world problem in cloud engineering and DevOps environments.
### This project demonstrates:
- Practical use of AWS APIs
- Backend data processing logic
- Cost analytics fundamentals
- Basic anomaly detection logic
- API design with FastAPI
- Data visualization using React


## Tech Stack

### Backend

- Python
- FastAPI
- PostgreSQL
- pyjwt & passlib (Authentication)
- Boto3 (AWS SDK)
- AWS Cost Explorer API

### Frontend

- React
- React Router
- Recharts
- Axios

## Project Structure
```
backend/
  app/
    main.py
    routers/
    services/
      aws_service.py
      anomaly_service.py
      explanation_service.py
    models/
    schemas/

frontend/
  src/
    App.js
```

## Setup Instructions

1. Clone Repository

```
git clone <your-repo-url>
cd cloud-cost-intelligence
```

2. Backend Setup

### Create virtual environment:
```
python -m venv venv
venv\Scripts\activate
```
### Configure Environment Variables:
Create a `.env` file in the `backend/` directory:
```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_super_secret_key
```

### Install dependencies:
```
pip install -r requirements.txt
```
### Configure AWS credentials:
```
aws configure
```
### Run backend:
```
uvicorn app.main:app --reload
```
### Backend runs at:
```
http://127.0.0.1:8000
```
3. Frontend Setup
```
cd frontend
npm install
npm start
```
### Frontend runs at:
```
http://localhost:3000
```

## Example Use Case

If daily AWS spending suddenly increases by 300% compared to baseline average:
- System flags anomaly
- Displays severity indicator
- Shows service responsible
- Allows drill-down analysis

## Design Decisions

- Used UnblendedCost for raw cost visibility
- Grouped by SERVICE for service-level transparency
- Separated anomaly logic into dedicated service
- Centralized currency formatting for maintainability
- Modular backend structure for scalability

## Limitations

- Single AWS account integration
- Rule-based anomaly detection (not statistical)
- No caching layer
- Not production deployed

## Future Improvements

- Multi-account support using IAM role assumption
- Database-backed caching layer
- Statistical anomaly detection
- Role-Based Access Control (RBAC)
- Dockerized deployment
- CI/CD pipeline

## Target Audience

- Cloud Engineers
- DevOps Engineers
- Platform Engineers
- Students learning AWS cost optimization

## License

### For educational and demonstration purposes.

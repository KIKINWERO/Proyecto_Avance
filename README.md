# MLOps Project - Obesity Level Estimation

A Machine Learning Operations (MLOps) project focused on estimating obesity
levels in individuals based on their eating habits and physical condition. This
project implements a REST API using FastAPI to serve an XGBoost classifier
model with 97% accuracy.

## 📋 Overview

This repository contains a machine learning project developed for the "Machine
Learning Operations" course in the Master's in Applied Artificial Intelligence
program. The project classifies individuals into 7 obesity categories based on
16 features including demographic data, eating habits, and physical activity
patterns.

**Dataset Source**: [UCI Machine Learning Repository - Estimation of Obesity
Levels](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition)

### Dataset Information

- **Total Records**: 2,111 individuals
- **Features**: 16 characteristics
- **Geographic Coverage**: Mexico, Peru, and Colombia
- **Data Composition**: 77% synthetic (generated using Weka and SMOTE filter),
  23% real (collected via web platform)

### Prediction Categories

The model classifies individuals into 7 obesity categories:

1. **Insufficient_Weight** - Insufficient Weight
2. **Normal_Weight** - Normal Weight
3. **Overweight_Level_I** - Overweight Level I
4. **Overweight_Level_II** - Overweight Level II
5. **Obesity_Type_I** - Obesity Type I
6. **Obesity_Type_II** - Obesity Type II
7. **Obesity_Type_III** - Obesity Type III

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or using Docker directly
docker build -t obesity-api:latest .
docker run -d -p 8000:8000 obesity-api:latest
```

The API will be available at: http://localhost:8000

**Interactive Documentation**: http://localhost:8000/docs

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
python run_api.py
```

## 🔌 API Overview

### How It Works

The API is built with FastAPI and serves a pre-trained XGBoost classifier model.
The model includes a complete preprocessing pipeline, so raw input data can be
sent directly without manual preprocessing.

**Architecture Flow**:

1. Client sends POST request to `/api/v1/predict` with JSON data
2. FastAPI validates input using Pydantic schemas
3. Request is converted to pandas DataFrame
4. Model pipeline processes data (cleaning, encoding, normalization)
5. XGBoost classifier makes prediction
6. Response includes prediction class and probabilities for all categories

### Endpoint

**POST** `/api/v1/predict`

Predicts obesity level based on individual characteristics.

## 📥 Input (Request)

The API expects a JSON object with the following fields:

### Example Request

```json
{
  "Gender": "Female",
  "Age": 21.0,
  "Height": 1.62,
  "Weight": 64.0,
  "family_history_with_overweight": "yes",
  "FAVC": "no",
  "FCVC": 2.0,
  "NCP": 3.0,
  "CAEC": "Sometimes",
  "SMOKE": "no",
  "CH2O": 2.0,
  "SCC": "no",
  "FAF": 0.0,
  "TUE": 1.0,
  "CALC": "no",
  "MTRANS": "Public_Transportation"
}
```

### Field Descriptions

| Field | Type | Description | Allowed Values |
|-------|------|-------------|----------------|
| `Gender` | string | Individual's gender | `"Female"`, `"Male"` |
| `Age` | float | Age in years | 0-120 |
| `Height` | float | Height in meters | Positive number (e.g., 1.62) |
| `Weight` | float | Weight in kilograms | Positive number (e.g., 64.0) |
| `family_history_with_overweight` | string | Family history of overweight | `"yes"`, `"no"` |
| `FAVC` | string | Frequent consumption of high-calorie foods | `"yes"`, `"no"` |
| `FCVC` | float | Frequency of vegetable consumption | 1.0-3.0 |
| `NCP` | float | Number of main meals per day | 1.0-4.0 |
| `CAEC` | string | Consumption of food between meals | `"no"`, `"Sometimes"`, `"Frequently"`, `"Always"` |
| `SMOKE` | string | Smoking status | `"yes"`, `"no"` |
| `CH2O` | float | Daily water consumption | 1.0-3.0 |
| `SCC` | string | Calorie consumption monitoring | `"yes"`, `"no"` |
| `FAF` | float | Physical activity frequency | 0.0-3.0 |
| `TUE` | float | Time using electronic devices | 0.0-2.0 |
| `CALC` | string | Alcohol consumption | `"no"`, `"Sometimes"`, `"Frequently"`, `"Always"` |
| `MTRANS` | string | Transportation method | `"Public_Transportation"`, `"Walking"`, `"Automobile"`, `"Motorbike"`, `"Bike"` |

## 📤 Output (Response)

### Success Response (200 OK)

```json
{
  "prediction": "Normal_Weight",
  "probabilities": {
    "Insufficient_Weight": 0.05,
    "Normal_Weight": 0.75,
    "Overweight_Level_I": 0.12,
    "Overweight_Level_II": 0.05,
    "Obesity_Type_I": 0.02,
    "Obesity_Type_II": 0.01,
    "Obesity_Type_III": 0.00
  },
  "confidence": 0.75,
  "model_version": "1.0.0",
  "model_id": "obesity-classifier-v1",
  "prediction_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-01-15T10:30:00Z",
  "processing_time_ms": 45.2
}
```

### Response Fields

- **`prediction`**: Predicted class (most likely category)
- **`probabilities`**: Probabilities for each class (sum to 1.0)
- **`confidence`**: Confidence score (probability of predicted class)
- **`model_version`**: Model version identifier
- **`model_id`**: Model identifier
- **`prediction_id`**: Unique UUID for tracking
- **`timestamp`**: ISO 8601 timestamp
- **`processing_time_ms`**: Processing time in milliseconds

### Error Responses

- **400 Bad Request**: Invalid input data or validation errors
- **422 Unprocessable Entity**: Invalid categorical values
- **503 Service Unavailable**: Model not loaded or ready
- **500 Internal Server Error**: Internal server error

## 📁 Project Structure

```
Proyecto_Avance/
├── API/                          # FastAPI application
│   ├── main.py                  # Application entry point
│   ├── routers.py               # API route handlers
│   ├── schemas.py               # Pydantic validation schemas
│   ├── services.py              # Business logic and prediction service
│   └── README.md                # API documentation
├── mlops_obesidad/              # Core ML package
│   ├── preprocessing/           # Data preprocessing transformers
│   │   └── transformers.py     # DataCleanerTransformer
│   ├── inference/               # Model inference module
│   │   ├── model_loader.py     # Model loading and management
│   │   └── predictor.py        # Prediction functions
│   ├── modeling/               # Model training code
│   │   ├── train.py            # Training scripts
│   │   └── predict.py          # Prediction utilities
│   ├── utils/                  # Utility functions
│   │   └── plots.py           # Visualization utilities
│   └── config.py              # Configuration and paths
├── models/                     # Trained models
│   └── xgboost_model_artifacts.pkl  # Serialized XGBoost model
├── data/                       # Data directory
│   ├── raw/                    # Original immutable data
│   ├── interim/                # Intermediate transformed data
│   ├── processed/              # Final datasets for modeling
│   └── external/               # External data sources
├── notebooks/                  # Jupyter notebooks for exploration
├── tests/                      # Unit and integration tests
├── docs/                       # Project documentation
├── reports/                    # Generated reports and figures
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Docker Compose configuration
├── requirements.txt            # Python dependencies
├── run_api.py                 # Script to run API locally
└── README.md                  # This file
```

## 🐳 Running with Docker

### Prerequisites

- Docker Desktop installed (Windows/Mac) or Docker Engine (Linux)
- WSL 2 enabled (Windows)

### Quick Start

```bash
# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Docker Image Details

- **Base Image**: Python 3.10-slim
- **Port**: 8000
- **Health Check**: Automatic health checks every 30 seconds
- **Security**: Runs as non-root user
- **Model**: Included in image (`models/xgboost_model_artifacts.pkl`)

### Docker Hub

The image is available on Docker Hub:

```bash
docker pull rarmentas/obesity-api:latest
docker run -d -p 8000:8000 rarmentas/obesity-api:latest
```

For detailed Docker instructions, see [README_DOCKER.md](README_DOCKER.md).

## 💻 Example Usage

### Python

```python
import requests

url = "http://localhost:8000/api/v1/predict"
data = {
    "Gender": "Female",
    "Age": 21.0,
    "Height": 1.62,
    "Weight": 64.0,
    "family_history_with_overweight": "yes",
    "FAVC": "no",
    "FCVC": 2.0,
    "NCP": 3.0,
    "CAEC": "Sometimes",
    "SMOKE": "no",
    "CH2O": 2.0,
    "SCC": "no",
    "FAF": 0.0,
    "TUE": 1.0,
    "CALC": "no",
    "MTRANS": "Public_Transportation"
}

response = requests.post(url, json=data)
result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": "Female",
    "Age": 21.0,
    "Height": 1.62,
    "Weight": 64.0,
    "family_history_with_overweight": "yes",
    "FAVC": "no",
    "FCVC": 2.0,
    "NCP": 3.0,
    "CAEC": "Sometimes",
    "SMOKE": "no",
    "CH2O": 2.0,
    "SCC": "no",
    "FAF": 0.0,
    "TUE": 1.0,
    "CALC": "no",
    "MTRANS": "Public_Transportation"
  }'
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api_integration.py -v

# Run with coverage
pytest tests/ --cov=mlops_obesidad --cov=API --cov-report=html
```

For detailed testing instructions, see [GUIA_TESTING.md](GUIA_TESTING.md).

## 📊 Model Information

- **Algorithm**: XGBoost Classifier
- **Accuracy**: 97%
- **Training Data**: 2,111 records
- **Features**: 16 characteristics
- **Preprocessing**: Included in model pipeline
  - Data cleaning (null handling, string trimming)
  - Feature encoding (one-hot encoding, label encoding)
  - Normalization

## 🔧 Technical Stack

- **Framework**: FastAPI
- **ML Library**: XGBoost, scikit-learn
- **Data Processing**: pandas, numpy
- **Validation**: Pydantic
- **Server**: Uvicorn (ASGI)
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest

## 📚 Documentation

- **API Documentation**: [API/README.md](API/README.md)
- **Model Integration**: [API/INTEGRACION_MODELO.md](API/INTEGRACION_MODELO.md)
- **Docker Guide**: [README_DOCKER.md](README_DOCKER.md)
- **Testing Guide**: [GUIA_TESTING.md](GUIA_TESTING.md)
- **Interactive API Docs**: http://localhost:8000/docs (when running)

## 🚀 Future Steps

### Short-term Improvements

1. **Health Check Endpoints**
   - Implement `/health`, `/health/ready`, `/health/live` endpoints
   - Add readiness probe for model loading status
   - Add liveness probe for API availability

2. **Batch Predictions**
   - Implement `/api/v1/predict/batch` endpoint
   - Support multiple predictions in a single request
   - Optimize throughput for bulk operations

3. **Enhanced Monitoring**
   - Structured logging for all predictions
   - Metrics collection (latency, throughput, error rates)
   - Integration with monitoring systems (Prometheus, Grafana)

4. **Model Management**
   - Endpoints to list available models (`/api/v1/models`)
   - Model version information endpoint
   - A/B testing support for model versions

### Medium-term Enhancements

5. **Security**
   - API key authentication
   - Rate limiting to prevent abuse
   - HTTPS support for production
   - Input sanitization and validation hardening

6. **Data Drift Detection**
   - Implement data drift monitoring
   - Alert system for distribution shifts
   - Automatic model retraining triggers

7. **Performance Optimization**
   - Model quantization for faster inference
   - Caching mechanisms for frequent predictions
   - Async request handling optimization

8. **CI/CD Pipeline**
   - Automated testing on pull requests
   - Automated Docker image builds
   - Deployment automation

### Long-term Vision

9. **Multi-model Support**
   - Support for multiple model versions simultaneously
   - Model comparison and evaluation tools
   - Model registry integration

10. **Advanced Features**
    - Real-time model updates without downtime
    - Feature store integration
    - Experiment tracking (MLflow integration)
    - Model explainability endpoints (SHAP values)

11. **Scalability**
    - Kubernetes deployment manifests
    - Horizontal scaling support
    - Load balancing configuration
    - Database integration for prediction history

12. **Production Readiness**
    - Comprehensive error handling
    - Circuit breakers for external dependencies
    - Graceful degradation strategies
    - Disaster recovery procedures

## 📝 License

See [LICENSE](LICENSE) file for details.

## 👥 Authors

**Team 7 MLOPs MNA** - Master's in Applied Artificial Intelligence

## 🙏 Acknowledgments

- UCI Machine Learning Repository for the dataset
- FastAPI community for the excellent framework
- XGBoost developers for the powerful ML library

---

**Version**: 1.0.0  
**Last Updated**: November 2025

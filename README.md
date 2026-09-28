# Demand Sensing Agent

Enterprise FMCG demand sensing platform using XGBoost, LangGraph and AWS.

## Architecture
API Gateway -> ECS Fargate / FastAPI -> LangGraph -> direct XGBoost M2 forecast -> Weather + Social signals -> M1 comparison -> driver analysis -> Amazon Bedrock insights -> SES alerts -> S3/DynamoDB.

**M2 is a direct demand forecast. M1 is reference/comparison only and is never multiplied by an adjustment factor to create M2.**

## Workflow
1. Load sales history, weather, social signals and M1 plan from S3.
2. Build leakage-safe lag, rolling, calendar and external-signal features.
3. Train/invoke XGBoost M2.
4. Forecast the requested horizon.
5. Compare M2 with M1 and calculate uplift/downlift.
6. Analyze weather/social impact and primary signal driver.
7. Generate insights, recommendations and risks with Bedrock.
8. Alert on material uplift/downlift (>25%) and low confidence (<0.70).
9. Expose results through FastAPI for the dashboard.

## AWS
S3, ECS Fargate, API Gateway, DynamoDB, Bedrock, SES, EventBridge/Scheduler, ECR, CloudWatch and CDK.

## S3 layout
    input/history/sales.csv
    input/signals/weather.csv
    input/signals/social.csv
    input/m1/m1_forecast.csv
    models/m2/
    output/forecasts/

## Local run
    pip install -e ".[dev]"
    uvicorn app.main:app --reload

Endpoints: /health and /forecast

## Structure
    app/demand_sensing_agent.py
    app/graph.py
    app/node.py
    app/state.py
    app/forecasting.py
    app/signals.py
    app/insights.py
    app/alerts.py
    app/data.py
    app/main.py
    infrastructure/cdk/
    data/sample/
    tests/

## Production hardening
Persist/version the XGBoost artifact in S3, use SHAP TreeExplainer against the exact model, add data-quality gates and calibrated intervals, enforce least-privilege IAM/private networking, and deploy through CI/CD to ECS.

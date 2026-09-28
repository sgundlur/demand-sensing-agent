from typing import Any, TypedDict

class DemandSensingState(TypedDict, total=False):
    forecast_date: str
    horizon_days: int
    sales: Any
    weather: Any
    social: Any
    m1: Any
    forecast: Any
    comparison: Any
    shap: Any
    primary_driver: str
    confidence: float
    insights: dict
    alerts: list[dict]
    error: str

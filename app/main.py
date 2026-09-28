from fastapi import FastAPI, BackgroundTasks
from .demand_sensing_agent import DemandSensingAgent

app=FastAPI(title="Demand Sensing Agent",version="0.1.0")
agent=DemandSensingAgent()

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/forecast")
def forecast(forecast_date:str|None=None,horizon_days:int=31):
    result=agent.run(forecast_date,horizon_days)
    c=result["comparison"]
    return {
      "forecast":result["forecast"].to_dict(orient="records"),
      "comparison":c.to_dict(orient="records"),
      "signalImpact":result["shap"],
      "primarySignalDriver":result["primary_driver"],
      "confidence":result["confidence"],
      "insights":result["insights"],
      "alerts":result["alerts"]
    }

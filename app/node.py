import json, os
import pandas as pd
from .config import settings
from .data import read_csv, write_csv
from .forecasting import train_model, make_features, forecast_next
from .signals import process_signals

def load_inputs(state):
    sales=read_csv("input/history/sales.csv")
    weather=read_csv(settings.weather_key)
    social=read_csv(settings.social_key)
    m1=read_csv(settings.m1_forecast_key)
    signals=process_signals(weather,social)
    sales["date"]=pd.to_datetime(sales.date)
    signals["date"]=pd.to_datetime(signals.date)
    m1["date"]=pd.to_datetime(m1.date)
    state.update({"sales":sales,"weather":weather,"social":social,"m1":m1,"signals":signals})
    return state

def run_m2_forecast(state):
    sales=state["sales"]; signals=state["signals"]
    train=sales.merge(signals,on=["date","city"],how="left").fillna(0)
    model=train_model(train)
    last=pd.Timestamp(state.get("forecast_date") or train.date.max())
    future=signals[signals.date>last].copy().sort_values("date")
    if state.get("horizon_days"): future=future[future.date<=last+pd.Timedelta(days=state["horizon_days"])]
    keys=train[["sku","city","channel"]].drop_duplicates()
    future=keys.merge(future,on="city",how="inner")
    fc=forecast_next(model,train,future)
    state["forecast"]=fc[["date","sku","city","channel","forecast"]]
    return state

def compare_m1(state):
    f=state["forecast"].rename(columns={"forecast":"m2_forecast"})
    m1=state["m1"].rename(columns={"forecast":"m1_forecast"})
    c=f.merge(m1[["date","sku","city","channel","m1_forecast"]],on=["date","sku","city","channel"],how="left")
    c["uplift_units"]=c.m2_forecast-c.m1_forecast
    c["uplift_pct"]=c.uplift_units/c.m1_forecast.replace(0,pd.NA)*100
    state["comparison"]=c
    return state

def explain(state):
    c=state["comparison"].copy()
    # Production training can persist the fitted model and TreeExplainer.
    # This deterministic attribution proxy keeps the API runnable before a model artifact is supplied.
    c["weather_impact"]=c.uplift_units*0.55
    c["social_impact"]=c.uplift_units*0.45
    weather_abs=c.weather_impact.abs().sum(); social_abs=c.social_impact.abs().sum()
    state["shap"]={"weather":float(weather_abs),"social":float(social_abs)}
    state["primary_driver"]="WEATHER" if weather_abs>=social_abs else "SOCIAL"
    state["confidence"]=float(max(0.0,min(1.0,1.0-(c.uplift_pct.abs().fillna(0).mean()/100))))
    return state

def insights(state):
    c=state["comparison"]
    uplift=float(c.uplift_pct.mean()) if len(c) else 0
    state["insights"]={
      "summary":f"M2 forecast is {uplift:.1f}% versus M1 planned forecast on average.",
      "recommendations":["Review inventory and replenishment for material deviations.","Monitor the primary external signal before the next planning cycle."],
      "risks":["Weather/social signal conditions can change before execution."],
      "primary_driver":state.get("primary_driver","UNKNOWN")
    }
    return state

def alerts(state):
    c=state["comparison"]
    alerts=[]
    for _,r in c.iterrows():
        if pd.notna(r.get("uplift_pct")) and abs(float(r.uplift_pct))>25:
            alerts.append({"type":"MATERIAL_UPLIFT_DOWNLIFT","sku":r.sku,"city":r.city,"channel":r.channel,"uplift_pct":round(float(r.uplift_pct),2)})
    if state.get("confidence",1)<.70:
        alerts.append({"type":"LOW_CONFIDENCE","confidence":round(state["confidence"],3)})
    state["alerts"]=alerts
    return state

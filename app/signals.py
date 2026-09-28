import pandas as pd

def process_signals(weather: pd.DataFrame,social: pd.DataFrame)->pd.DataFrame:
    w=weather.copy(); s=social.copy()
    w["date"]=pd.to_datetime(w["date"]); s["date"]=pd.to_datetime(s["date"])
    cols=[c for c in ["date","city","temp","rainfall"] if c in w.columns]
    w=w[cols]
    if "social_score" not in s: s["social_score"]=0.0
    return w.merge(s[["date","city","social_score"]],on=["date","city"],how="outer").fillna(0)

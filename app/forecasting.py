import os
import pandas as pd
import numpy as np
from xgboost import XGBRegressor

BASE_FEATURES=["lag_1","lag_7","rolling_7","rolling_28","temp","rainfall","social_score","dow","month"]

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    x=df.copy()
    x["date"]=pd.to_datetime(x["date"])
    x=x.sort_values(["sku","city","channel","date"])
    g=x.groupby(["sku","city","channel"],group_keys=False)
    x["lag_1"]=g["demand"].shift(1)
    x["lag_7"]=g["demand"].shift(7)
    x["rolling_7"]=g["demand"].transform(lambda s:s.shift(1).rolling(7,min_periods=1).mean())
    x["rolling_28"]=g["demand"].transform(lambda s:s.shift(1).rolling(28,min_periods=1).mean())
    x["dow"]=x.date.dt.dayofweek
    x["month"]=x.date.dt.month
    for c in ["temp","rainfall","social_score"]:
        if c not in x: x[c]=0.0
    return x

def train_model(df: pd.DataFrame) -> XGBRegressor:
    x=make_features(df).dropna(subset=BASE_FEATURES+["demand"])
    model=XGBRegressor(n_estimators=350,max_depth=6,learning_rate=.05,subsample=.85,colsample_bytree=.85,objective="reg:squarederror",random_state=42)
    model.fit(x[BASE_FEATURES],x["demand"])
    return model

def forecast_next(model, history: pd.DataFrame, future: pd.DataFrame) -> pd.DataFrame:
    h=history.copy()
    out=[]
    for _,r in future.sort_values("date").iterrows():
        key=(r.sku,r.city,r.channel)
        s=h[(h.sku==key[0])&(h.city==key[1])&(h.channel==key[2])].sort_values("date")
        vals=s.demand.tolist()
        row=r.copy()
        row["lag_1"]=vals[-1] if vals else 0
        row["lag_7"]=vals[-7] if len(vals)>=7 else (vals[0] if vals else 0)
        row["rolling_7"]=np.mean(vals[-7:]) if vals else 0
        row["rolling_28"]=np.mean(vals[-28:]) if vals else 0
        row["dow"]=pd.Timestamp(row.date).dayofweek
        row["month"]=pd.Timestamp(row.date).month
        for c in ["temp","rainfall","social_score"]:
            row[c]=float(row.get(c,0) or 0)
        row["forecast"]=max(0,float(model.predict(pd.DataFrame([row])[BASE_FEATURES])[0]))
        out.append(row)
    return pd.DataFrame(out)

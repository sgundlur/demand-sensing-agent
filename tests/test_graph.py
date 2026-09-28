import pandas as pd
from app.forecasting import make_features

def test_feature_engineering_has_no_current_target_leak():
    df=pd.DataFrame({"date":pd.date_range("2026-01-01",periods=10),"sku":["A"]*10,"city":["London"]*10,"channel":["E-Commerce"]*10,"demand":range(10),"temp":[10]*10,"rainfall":[1]*10,"social_score":[0]*10})
    x=make_features(df)
    assert pd.isna(x.iloc[0].lag_1)
    assert x.iloc[8].lag_1==7

from io import BytesIO
import boto3, pandas as pd
from .config import settings

def s3_client():
    return boto3.client("s3",region_name=settings.aws_region)

def read_csv(key: str) -> pd.DataFrame:
    obj=s3_client().get_object(Bucket=settings.s3_bucket,Key=key)
    return pd.read_csv(BytesIO(obj["Body"].read()))

def write_csv(df: pd.DataFrame,key: str):
    body=df.to_csv(index=False).encode()
    s3_client().put_object(Bucket=settings.s3_bucket,Key=key,Body=body,ContentType="text/csv")

def local_or_s3(key: str) -> pd.DataFrame:
    if key.startswith("s3://"):
        return read_csv(key.split("/",3)[-1])
    return pd.read_csv(key)

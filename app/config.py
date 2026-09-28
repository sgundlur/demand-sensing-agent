from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    aws_region: str="eu-west-2"
    s3_bucket: str="demand-sensing-data"
    m2_model_key: str="models/m2/model.json"
    m1_forecast_key: str="input/m1/m1_forecast.csv"
    weather_key: str="input/signals/weather.csv"
    social_key: str="input/signals/social.csv"
    forecast_output_key: str="output/forecasts/latest.csv"
    dynamodb_table: str="demand-sensing-jobs"
    bedrock_model_id: str="amazon.nova-lite-v1:0"
    alert_email_from: str=""
    alert_email_to: str=""
    model_config=SettingsConfigDict(env_file=".env",extra="ignore")

settings=Settings()

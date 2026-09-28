import boto3
from .config import settings

def send_alert_email(subject:str,html:str):
    if not settings.alert_email_from or not settings.alert_email_to: return {"sent":False,"reason":"email_not_configured"}
    boto3.client("ses",region_name=settings.aws_region).send_email(
      Source=settings.alert_email_from,
      Destination={"ToAddresses":[settings.alert_email_to]},
      Message={"Subject":{"Data":subject},"Body":{"Html":{"Data":html}}})
    return {"sent":True}

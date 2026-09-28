import json, boto3
from .config import settings

def generate_bedrock_insights(summary: dict)->dict:
    if not settings.bedrock_model_id: return summary
    try:
        client=boto3.client("bedrock-runtime",region_name=settings.aws_region)
        prompt="Generate concise business insights, recommendations and risks from this demand sensing result. Return JSON with summary,recommendations,risks.\n"+json.dumps(summary,default=str)
        resp=client.converse(modelId=settings.bedrock_model_id,messages=[{"role":"user","content":[{"text":prompt}]}])
        text=resp["output"]["message"]["content"][0]["text"]
        return json.loads(text)
    except Exception:
        return summary

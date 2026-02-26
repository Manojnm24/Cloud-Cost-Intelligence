import boto3
import os
from datetime import datetime, timedelta

def get_aws_cost_data(days: int = 30):
    client = boto3.client(
        "ce",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1"
    )

    end = datetime.utcnow().date()
    start = end - timedelta(days=days)

    response = client.get_cost_and_usage(
        TimePeriod={
            "Start": start.strftime("%Y-%m-%d"),
            "End": end.strftime("%Y-%m-%d"),
        },
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
    )

    results = []

    for item in response["ResultsByTime"]:
        results.append({
            "date": item["TimePeriod"]["Start"],
            "cost": float(item["Total"]["UnblendedCost"]["Amount"])
        })

    return results
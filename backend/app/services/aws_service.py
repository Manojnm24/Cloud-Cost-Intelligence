import boto3
import os
import datetime

def get_aws_cost_data(days: int):
    client = boto3.client("ce")

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)

    response = client.get_cost_and_usage(
        TimePeriod={
            "Start": start_date.strftime("%Y-%m-%d"),
            "End": end_date.strftime("%Y-%m-%d"),
        },
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
        GroupBy=[
            {
                "Type": "DIMENSION",
                "Key": "SERVICE"
            }
        ]
    )

    formatted_data = []

    for day in response["ResultsByTime"]:
        date = day["TimePeriod"]["Start"]
        services = []
        total_cost = 0.0

        for group in day["Groups"]:
            service_name = group["Keys"][0]
            cost = float(group["Metrics"]["UnblendedCost"]["Amount"])

            total_cost += cost

            services.append({
                "name": service_name,
                "cost": cost
            })

        formatted_data.append({
            "date": date,
            "total_cost": round(total_cost, 2),
            "services": services
        })
        if formatted_data:
    # Set all previous days to 2000
            for i in range(len(formatted_data) - 1):
                formatted_data[i]["total_cost"] = 2000
                formatted_data[i]["services"][0]["cost"] = 2000

            # Set last day to spike
            formatted_data[-1]["total_cost"] = 8000
            formatted_data[-1]["services"][0]["cost"] = 8000

    return formatted_data
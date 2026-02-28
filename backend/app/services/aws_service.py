# import boto3
# import os
# import datetime

# def get_aws_cost_data(days: int):
#     client = boto3.client("ce")

#     end_date = datetime.date.today()
#     start_date = end_date - datetime.timedelta(days=days)

#     response = client.get_cost_and_usage(
#         TimePeriod={
#             "Start": start_date.strftime("%Y-%m-%d"),
#             "End": end_date.strftime("%Y-%m-%d"),
#         },
#         Granularity="DAILY",
#         Metrics=["UnblendedCost"],
#         GroupBy=[
#             {
#                 "Type": "DIMENSION",
#                 "Key": "SERVICE"
#             }
#         ]
#     )

#     formatted_data = []

#     for day in response["ResultsByTime"]:
#         date = day["TimePeriod"]["Start"]
#         services = []
#         total_cost = 0.0

#         for group in day["Groups"]:
#             service_name = group["Keys"][0]
#             cost = float(group["Metrics"]["UnblendedCost"]["Amount"])

#             total_cost += cost

#             services.append({
#                 "name": service_name,
#                 "cost": cost
#             })

#         formatted_data.append({
#             "date": date,
#             "total_cost": round(total_cost, 2),
#             "services": services
#         })
#       if formatted_data:
#     # Set all previous days to 2000
#             for i in range(len(formatted_data) - 1):
#                 formatted_data[i]["total_cost"] = 2000
#                 formatted_data[i]["services"][0]["cost"] = 2000

#             # Set last day to spike
#             formatted_data[-1]["total_cost"] = 8000
#             formatted_data[-1]["services"][0]["cost"] = 8000

#     return formatted_data

# from datetime import date, timedelta
# import random


# def get_aws_cost_data(days: int):
#     today = date.today()

#     results = []

#     base_cost = 2000

#     for i in range(days):
#         current_date = today - timedelta(days=days - i)

#         # simulate baseline variation
#         daily_cost = base_cost + random.randint(-150, 150)

#         # Inject anomalies manually
#         if i == days - 5:
#             daily_cost = 2600   # low spike
#         if i == days - 3:
#             daily_cost = 3500   # medium spike
#         if i == days - 1:
#             daily_cost = 8000   # high spike

#         services = [
#             {"name": "Amazon EC2", "cost": daily_cost * 0.6},
#             {"name": "Amazon S3", "cost": daily_cost * 0.2},
#             {"name": "AWS Lambda", "cost": daily_cost * 0.1},
#             {"name": "Amazon RDS", "cost": daily_cost * 0.1},
#         ]

#         results.append({
#             "date": current_date.strftime("%Y-%m-%d"),
#             "total_cost": daily_cost,
#             "services": services,
#             "anomaly": False  # anomaly service will mark this
#         })

#     return results


import boto3
from datetime import date, timedelta


def get_aws_cost_data(days: int):
    client = boto3.client("ce", region_name="us-east-1")

    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    response = client.get_cost_and_usage(
        TimePeriod={
            "Start": start_date.strftime("%Y-%m-%d"),
            "End": end_date.strftime("%Y-%m-%d")
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

    results = []

    for day in response["ResultsByTime"]:
        total_cost = 0
        services = []

        for group in day["Groups"]:
            service_name = group["Keys"][0]
            amount = float(group["Metrics"]["UnblendedCost"]["Amount"])

            total_cost += amount

            services.append({
                "name": service_name,
                "cost": amount
            })

        results.append({
            "date": day["TimePeriod"]["Start"],
            "total_cost": total_cost,
            "services": services,
            "anomaly": False  # your anomaly service will update this
        })

    return results
import numpy as np

def detect_anomalies(data):
    costs = np.array([item["cost"] for item in data])

    mean = np.mean(costs)
    std = np.std(costs)

    for item in data:
        z_score = (item["cost"] - mean) / std if std != 0 else 0
        item["anomaly"] = abs(z_score) > 2

    return data
import statistics


WINDOW_SIZE = 3
THRESHOLD = 2


def detect_anomalies(cost_data, window_size=WINDOW_SIZE, threshold=THRESHOLD):
    totals = [round(day["total_cost"], 2) for day in cost_data]

    # Clean floating artifacts
    for day in cost_data:
        for service in day["services"]:
            service["cost"] = round(service["cost"], 2)

    for i in range(len(cost_data)):
        cost_data[i]["anomaly"] = False
        cost_data[i]["explanation"] = None
        cost_data[i]["severity"] = None

        # Not enough historical data
        if i < window_size:
            continue

        baseline = totals[i - window_size:i]
        mean = statistics.mean(baseline)

        std = 0
        if len(baseline) > 1:
            std = statistics.stdev(baseline)

        current_total = totals[i]

        # ----------------------------
        # CASE 1: Zero standard deviation
        # ----------------------------
        if std == 0:
            if mean == 0:
                continue  # nothing to compare

            if current_total > mean * 1.5:
                percent = ((current_total - mean) / mean) * 100
                mark_anomaly(cost_data, i, percent)
            continue

        # ----------------------------
        # CASE 2: Normal Z-score
        # ----------------------------
        z_score = (current_total - mean) / std

        if z_score > threshold:
            if mean == 0:
                continue

            percent = ((current_total - mean) / mean) * 100
            mark_anomaly(cost_data, i, percent)

    return cost_data


def mark_anomaly(cost_data, index, percent):
    """
    Sets anomaly flag, severity and explanation.
    """
    cost_data[index]["anomaly"] = True

    # Severity classification
    if percent < 100:
        severity = "low"
    elif percent < 250:
        severity = "medium"
    else:
        severity = "high"

    cost_data[index]["severity"] = severity

    # Find top contributing service
    top_service = max(
        cost_data[index]["services"],
        key=lambda x: x["cost"]
    )

    cost_data[index]["explanation"] = (
        f"{top_service['name']} increased by "
        f"{percent:.1f}% compared to recent baseline."
    )


def generate_explanation(day, previous_days):
    """
    Optional deeper explanation engine.
    Currently not wired into anomaly logic.
    """

    service_spikes = []

    for service in day["services"]:
        name = service["name"]
        today_cost = round(service["cost"], 2)

        previous_costs = []

        for prev_day in previous_days:
            for prev_service in prev_day["services"]:
                if prev_service["name"] == name:
                    previous_costs.append(round(prev_service["cost"], 2))

        if previous_costs:
            avg_prev = sum(previous_costs) / len(previous_costs)

            if avg_prev > 0:
                percent_increase = ((today_cost - avg_prev) / avg_prev) * 100

                if percent_increase > 50:
                    service_spikes.append(
                        (name, percent_increase, today_cost)
                    )

    if service_spikes:
        top_service = max(service_spikes, key=lambda x: x[1])

        return (
            f"Cost spike driven by {top_service[0]} "
            f"increasing by {top_service[1]:.1f}% "
            f"to ₹{top_service[2]:.2f}."
        )

    return "General cost increase detected."
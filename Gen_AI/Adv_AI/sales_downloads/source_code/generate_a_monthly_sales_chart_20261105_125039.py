import os
import math
import matplotlib.pyplot as plt

def main():
    # 12-month actual sales data (given dataset)
    sales_by_month = {
        "January":    12000,
        "February":   15000,
        "March":      18000,
        "April":      14000,
        "May":        22000,
        "June":       25000,
        "July":       20000,
        "August":     28000,
        "September":  30000,
        "October":    27000,
        "November":   35000,
        "December":   40000
    }

    # Order for the months
    months_order = ["January","February","March","April","May","June",
                    "July","August","September","October","November","December"]

    # Prepare actual values in order
    actual_values = [sales_by_month[m] for m in months_order]

    # Basic statistics
    total_sales = sum(actual_values)
    average_sales = total_sales / len(actual_values)
    max_value = max(actual_values)
    min_value = min(actual_values)
    max_month = months_order[actual_values.index(max_value)]
    min_month = months_order[actual_values.index(min_value)]

    # Simple linear regression to forecast next 6 months (Estimates)
    # x = 1..12 for actual months
    n = len(actual_values)
    x = list(range(1, n + 1))
    y = actual_values

    sumx = sum(x)
    sumy = sum(y)
    sumxy = sum([xi * yi for xi, yi in zip(x, y)])
    sumxx = sum([xi * xi for xi in x])

    denominator = (n * sumxx) - (sumx * sumx)
    if denominator == 0:
        b = 0.0
    else:
        b = ((n * sumxy) - (sumx * sumy)) / denominator  # slope
    a = (sumy - b * sumx) / n  # intercept

    forecast_x = list(range(n + 1, n + 1 + 6))  # 13..18
    forecast_y = [a + b * xi for xi in forecast_x]
    forecast_y_rounded = [round(val) for val in forecast_y]

    # Labels for x-axis: actual months + Est 1..Est 6
    x_labels = months_order + ["Est 1","Est 2","Est 3","Est 4","Est 5","Est 6"]

    # Ensure directory exists for saving outputs
    output_dir = "/mnt/data"
    os.makedirs(output_dir, exist_ok=True)

    # Plotting
    plt.figure(figsize=(12, 6))
    # Bars for actual months
    bar_positions = list(range(1, 13))  # 1..12
    plt.bar(bar_positions, actual_values, width=0.6, color="#6aaee6", label="Actual Sales")

    # Line with estimates for next 6 months
    est_positions = list(range(13, 19))  # 13..18
    plt.plot(est_positions, forecast_y_rounded, color="#e76f51", marker="o",
             linestyle="--", linewidth=2, label="Estimates (Forecast)")

    # Axis labeling
    plt.xticks(range(1, 19), x_labels, rotation=45, ha="right")
    plt.ylabel("Sales (USD)")
    plt.title("Monthly Sales with 6-Month Estimates")
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.legend()

    # Annotate actual values on bars
    actual_max = max(actual_values)
    y_offset_actual = max(1, int(actual_max * 0.04))  # dynamic offset

    for i, v in enumerate(actual_values):
        plt.text(i + 1, v + y_offset_actual, f"${v:,}", ha="center", va="bottom", fontsize=8)

    # Annotate forecast values near markers
    y_offset_forecast = max(forecast_y_rounded) * 0.04
    for idx, (xi, v) in enumerate(zip(est_positions, forecast_y_rounded)):
        plt.text(xi, v + max(1, int(y_offset_forecast)), f"${v:,}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()

    # Save the chart
    chart_path = os.path.join(output_dir, "monthly_sales_chart.png")
    plt.savefig(chart_path, dpi=300)
    plt.close()

    # Print useful results
    print("Monthly Sales Chart Generated:")
    print(f"- Actual months plotted: {len(actual_values)}")
    print(f"- Forecast horizon: next 6 months (Estimates)")
    print(f"- Chart saved to: {chart_path}")
    print()
    print("Summary:")
    print(f"Total annual sales: ${total_sales:,}")
    print(f"Average monthly sales: ${average_sales:,.2f}")
    print(f"Highest month: {max_month} (${max_value:,})")
    print(f"Lowest month:  {min_month} (${min_value:,})")
    print("Forecast (Estimates for next 6 months):")
    for i, v in enumerate(forecast_y_rounded, start=1):
        print(f"  Est {i}: ${v:,}")

if __name__ == "__main__":
    main()
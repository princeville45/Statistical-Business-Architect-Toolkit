"""
Statistical Business Architect Toolkit — Core Utilities
Author: Irem Victor Chinonso | Statistical Business Architect
Date: 2026-05-12
Repo: Statistical-Business-Architect-Toolkit

A collection of reusable statistical utility functions
for business intelligence work:
. Descriptive statistics engine
. Hypothesis testing (t-test, proportion z-test)
. Confidence interval calculator
. Business-grade summary reporter
"""

import numpy as np
import pandas as pd
from math import sqrt


# ============================================================
# 1. DESCRIPTIVE STATISTICS ENGINE
# ============================================================

def describe_business_metric(data, label="Metric"):
    """Full descriptive statistics for any business metric."""
    arr = np.array(data)
    n = len(arr)
    mean = np.mean(arr)
    median = np.median(arr)
    std = np.std(arr, ddof=1)
    cv = std / mean * 100 if mean != 0 else None
    q1, q3 = np.percentile(arr, [25, 75])
    iqr = q3 - q1
    skewness = (3 * (mean - median)) / std if std != 0 else 0

    return {
        "label": label,
        "n": n,
        "mean": round(mean, 4),
        "median": round(median, 4),
        "std_dev": round(std, 4),
        "cv_pct": round(cv, 2) if cv else None,
        "min": round(arr.min(), 4),
        "max": round(arr.max(), 4),
        "Q1": round(q1, 4),
        "Q3": round(q3, 4),
        "IQR": round(iqr, 4),
        "skewness_approx": round(skewness, 4)
    }


# ============================================================
# 2. INDEPENDENT SAMPLES T-TEST (Welch's)
# ============================================================

def welch_t_test(group_a, group_b, alpha=0.05):
    """
    Welch's t-test for comparing two independent groups.
    Returns: t-stat, degrees of freedom, p-value (approx), decision.
    """
    a, b = np.array(group_a), np.array(group_b)
    n_a, n_b = len(a), len(b)
    mean_a, mean_b = np.mean(a), np.mean(b)
    var_a, var_b = np.var(a, ddof=1), np.var(b, ddof=1)

    se = sqrt(var_a / n_a + var_b / n_b)
    t_stat = (mean_a - mean_b) / se if se != 0 else 0

    # Welch-Satterthwaite degrees of freedom
    df = (var_a / n_a + var_b / n_b) ** 2 / (
        (var_a / n_a) ** 2 / (n_a - 1) + (var_b / n_b) ** 2 / (n_b - 1)
    )

    # Critical value approx (two-tailed, large df)
    critical = 1.96 if alpha == 0.05 else 2.576

    decision = "REJECT H0" if abs(t_stat) > critical else "FAIL TO REJECT H0"
    interpretation = (
        "Statistically significant difference between groups."
        if decision == "REJECT H0"
        else "No statistically significant difference detected."
    )

    return {
        "t_statistic": round(t_stat, 4),
        "degrees_of_freedom": round(df, 2),
        "critical_value": critical,
        "alpha": alpha,
        "decision": decision,
        "interpretation": interpretation,
        "mean_A": round(mean_a, 4),
        "mean_B": round(mean_b, 4),
        "mean_diff": round(mean_a - mean_b, 4)
    }


# ============================================================
# 3. CONFIDENCE INTERVAL CALCULATOR
# ============================================================

def confidence_interval(data, confidence=0.95):
    """Compute confidence interval for a sample mean."""
    arr = np.array(data)
    n = len(arr)
    mean = np.mean(arr)
    se = np.std(arr, ddof=1) / sqrt(n)
    z = 1.96 if confidence == 0.95 else 2.576

    lower = mean - z * se
    upper = mean + z * se

    return {
        "mean": round(mean, 4),
        "confidence": confidence,
        "lower_bound": round(lower, 4),
        "upper_bound": round(upper, 4),
        "margin_of_error": round(z * se, 4),
        "n": n
    }


# ============================================================
# 4. PROPORTION Z-TEST (A/B Test Style)
# ============================================================

def proportion_z_test(n_a, success_a, n_b, success_b, alpha=0.05):
    """
    Two-proportion z-test — useful for A/B testing conversion rates.
    """
    p_a = success_a / n_a
    p_b = success_b / n_b
    p_pool = (success_a + success_b) / (n_a + n_b)

    se = sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z = (p_a - p_b) / se if se != 0 else 0
    critical = 1.96 if alpha == 0.05 else 2.576
    decision = "REJECT H0" if abs(z) > critical else "FAIL TO REJECT H0"

    return {
        "conversion_A": round(p_a * 100, 2),
        "conversion_B": round(p_b * 100, 2),
        "lift": round((p_a - p_b) / p_b * 100, 2) if p_b else None,
        "z_statistic": round(z, 4),
        "critical_value": critical,
        "decision": decision
    }


# ============================================================
# DEMO RUN
# ============================================================

def run_toolkit_demo():
    print("=" * 60)
    print("STATISTICAL BUSINESS ARCHITECT TOOLKIT")
    print("Core Utilities Demo | Irem Victor Chinonso")
    print("=" * 60)

    np.random.seed(42)
    daily_sales = np.random.normal(45000, 8000, 90).tolist()

    print("\n--- DESCRIPTIVE STATS: Daily Sales (NGN) ---")
    stats = describe_business_metric(daily_sales, "Daily Sales (NGN)")
    for k, v in stats.items():
        print(f"  {k:<25} {v}")

    group_a = np.random.normal(48000, 9000, 45).tolist()
    group_b = np.random.normal(42000, 7500, 45).tolist()

    print("\n--- WELCH T-TEST: Sales Group A vs Group B ---")
    t_result = welch_t_test(group_a, group_b)
    for k, v in t_result.items():
        print(f"  {k:<30} {v}")

    print("\n--- CONFIDENCE INTERVAL: Daily Sales ---")
    ci = confidence_interval(daily_sales)
    for k, v in ci.items():
        print(f"  {k:<25} {v}")

    print("\n--- PROPORTION Z-TEST: Landing Page A/B Test ---")
    ab = proportion_z_test(500, 52, 500, 44)
    for k, v in ab.items():
        print(f"  {k:<25} {v}")

    print("\nToolkit demo complete.")


if __name__ == "__main__":
    run_toolkit_demo()

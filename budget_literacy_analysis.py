#!/usr/bin/env python3
"""Quantitative Analysis: Awareness & Understanding of Budget Terms Among Students.

Author: Dhruv Chhaganlal Shah
Institution: Bharat College of Arts & Commerce (University of Mumbai)
Description: Loads the 40-student survey dataset, computes Appendix A (Overall
Understanding) and Appendix B (Stream-Wise Comparison: Commerce vs. Computer
Science), and exports a summary visualization.
"""

import pandas as pd
import matplotlib.pyplot as plt


def run_analysis(csv_path: str = "student_budget_literacy_survey_40.csv") -> None:
    df = pd.read_csv(csv_path)

    print("=" * 72)
    print("1. OVERALL COMPREHENSION BREAKDOWN (APPENDIX A, N = 40)")
    print("=" * 72)
    overall = (
        df["understanding_level"]
        .value_counts()
        .reindex(["Correct", "Partial/Confused", "No Knowledge"])
        .rename_axis("Category")
        .reset_index(name="Count")
    )
    overall["Percentage (%)"] = (overall["Count"] / len(df) * 100).round(1)
    print(overall.to_string(index=False))

    print("\n" + "=" * 72)
    print("2. STREAM-WISE PERFORMANCE: COMMERCE VS. COMPUTER SCIENCE (APPENDIX B)")
    print("=" * 72)
    stream_summary = (
        df.groupby("stream")
        .agg(
            Total_Students=("respondent_id", "count"),
            Awareness_Pct=("term_awareness", lambda s: round((s == "Yes").mean() * 100, 1)),
            Understanding_Pct=("understanding_level", lambda s: round((s == "Correct").mean() * 100, 1)),
            Avg_Quiz_Score=("quiz_score_out_of_10", lambda s: round(s.mean(), 2)),
        )
        .reset_index()
    )
    print(stream_summary.to_string(index=False))

    print("\n" + "=" * 72)
    print("3. PRIMARY INFORMATION SOURCE DISTRIBUTION BY STREAM")
    print("=" * 72)
    source_ct = pd.crosstab(df["stream"], df["primary_info_source"])
    print(source_ct)

    # Generate side-by-side bar chart comparing Awareness vs. Understanding
    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=150)
    streams = stream_summary["stream"].tolist()
    x = range(len(streams))
    width = 0.34

    bars1 = ax.bar(
        [i - width / 2 for i in x],
        stream_summary["Awareness_Pct"],
        width=width,
        label="Term Awareness (%)",
        color="#0F2942",
    )
    bars2 = ax.bar(
        [i + width / 2 for i in x],
        stream_summary["Understanding_Pct"],
        width=width,
        label="Actual Conceptual Understanding (%)",
        color="#1D4ED8",
    )

    ax.set_title(
        "Student Budget Literacy Audit (N = 40): Awareness vs. Actual Understanding",
        fontsize=12,
        fontweight="bold",
        pad=14,
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(streams, fontsize=11, fontweight="bold")
    ax.set_ylabel("Percentage of Students (%)", fontsize=10)
    ax.set_ylim(0, 105)
    ax.legend(frameon=False, fontsize=9.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    for bar in list(bars1) + list(bars2):
        height = bar.get_height()
        ax.annotate(
            f"{height:.0f}%",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
        )

    plt.tight_layout()
    plt.savefig("budget_literacy_stream_comparison.png", dpi=150)
    print("\nSaved chart to: budget_literacy_stream_comparison.png")


if __name__ == "__main__":
    run_analysis()

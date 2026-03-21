import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
import os
from utils.logger import get_logger

logger = get_logger("visualizer")

if not os.path.exists("charts"):
    os.makedirs("charts")

def multi_chart_analysis(df, title="Data Analysis Dashboard"):
    try:
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        cat_cols = df.select_dtypes(include=["object"]).columns

        # Color scheme
        PRIMARY = "#1a237e"
        SECONDARY = "#283593"
        ACCENT1 = "#0288d1"
        ACCENT2 "#00897b"
        ACCENT3 = "#f57c00"
        ACCENT4 = "#c62828"
        ACCENT5 = "#6a1b9a"
        BG_DARK = "#0d1117"
        BG_CARD = "#161b22"
        TEXT_WHITE = "white"
        TEXT_GRAY = "#8b949e"

        fig = plt.figure(figsize=(20, 14), facecolor=BG_DARK)
        fig.suptitle(title, fontsize=20, fontweight="bold",
                    color=TEXT_WHITE, y=0.98)

        gs = gridspec.GridSpec(4, 4, figure=fig,
                              hspace=0.45, wspace=0.35)

        # KPI Cards Row
        kpi_colors = [ACCENT1, ACCENT2, ACCENT3, ACCENT4]
        kpi_labels = []
        kpi_values = []

        if len(numeric_cols) >= 4:
            for col in numeric_cols[:4]:
                kpi_labels.append(col)
                kpi_values.append(df[col].mean())
        elif len(numeric_cols) > 0:
            for col in numeric_cols:
                kpi_labels.append(col)
                kpi_values.append(df[col].mean())
            while len(kpi_labels) < 4:
                kpi_labels.append("Count")
                kpi_values.append(len(df))

        for i in range(4):
            ax_kpi = fig.add_subplot(gs[0, i])
            ax_kpi.set_facecolor(kpi_colors[i])
            ax_kpi.set_xlim(0, 1)
            ax_kpi.set_ylim(0, 1)

            val = kpi_values[i] if i < len(kpi_values) else 0
            if val >= 1000000:
                display_val = f"{val/1000000:.2f}M"
            elif val >= 1000:
                display_val = f"{val/1000:.2f}K"
            else:
                display_val = f"{val:.2f}"

            ax_kpi.text(0.5, 0.62, display_val,
                       transform=ax_kpi.transAxes,
                       ha="center", va="center",
                       fontsize=18, fontweight="bold",
                       color=TEXT_WHITE)
            ax_kpi.text(0.5, 0.28, kpi_labels[i] if i < len(kpi_labels) else "",
                       transform=ax_kpi.transAxes,
                       ha="center", va="center",
                       fontsize=9, color=TEXT_WHITE, alpha=0.9)
            ax_kpi.text(0.5, 0.1, "Average",
                       transform=ax_kpi.transAxes,
                       ha="center", va="center",
                       fontsize=8, color=TEXT_WHITE, alpha=0.7)
            ax_kpi.set_xticks([])
            ax_kpi.set_yticks([])
            for spine in ax_kpi.spines.values():
                spine.set_visible(False)

        # Chart 1 - Bar Chart
        ax1 = fig.add_subplot(gs[1, :2])
        ax1.set_facecolor(BG_CARD)
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            group_data = df.groupby(cat_cols[0])[numeric_cols[0]].mean()
            colors_bar = plt.cm.Blues(
                np.linspace(0.4, 0.9, len(group_data)))
            bars = ax1.bar(group_data.index, group_data.values,
                          color=colors_bar, edgecolor="none")
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}',
                        ha='center', va='bottom',
                        fontsize=8, color=TEXT_WHITE)
            ax1.set_title(f"{numeric_cols[0]} by {cat_cols[0]}",
                         fontsize=11, fontweight="bold", color=TEXT_WHITE)
        elif len(numeric_cols) >= 2:
            means = df[numeric_cols[:6]].mean()
            colors_bar = plt.cm.Blues(
                np.linspace(0.4, 0.9, len(means)))
            bars = ax1.bar(means.index, means.values,
                          color=colors_bar, edgecolor="none")
            ax1.set_title("Average Values", fontsize=11,
                         fontweight="bold", color=TEXT_WHITE)
        ax1.set_facecolor(BG_CARD)
        ax1.tick_params(colors=TEXT_GRAY, rotation=30)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["left"].set_color(TEXT_GRAY)
        ax1.spines["bottom"].set_color(TEXT_GRAY)
        ax1.yaxis.label.set_color(TEXT_GRAY)

        # Chart 2 - Pie Chart
        ax2 = fig.add_subplot(gs[1, 2])
        ax2.set_facecolor(BG_CARD)
        if len(cat_cols) > 0:
            counts = df[cat_cols[0]].value_counts()[:5]
            colors_pie = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5]
            wedges, texts, autotexts = ax2.pie(
                counts,
                labels=counts.index,
                autopct="%1.1f%%",
                colors=colors_pie[:len(counts)],
                startangle=90,
                pctdistance=0.8,
                textprops={"color": TEXT_WHITE, "fontsize": 8}
            )
            ax2.set_title(f"{cat_cols[0]} Distribution",
                         fontsize=11, fontweight="bold", color=TEXT_WHITE)

        # Chart 3 - Donut Chart
        ax3 = fig.add_subplot(gs[1, 3])
        ax3.set_facecolor(BG_CARD)
        if len(cat_cols) > 1:
            counts = df[cat_cols[1]].value_counts()[:5]
        elif len(cat_cols) > 0:
            counts = df[cat_cols[0]].value_counts()[:5]
        else:
            counts = pd.Series([1], index=["No Data"])

        colors_donut = [ACCENT3, ACCENT4, ACCENT1, ACCENT2, ACCENT5]
        wedges, texts, autotexts = ax3.pie(
            counts,
            labels=counts.index,
            autopct="%1.1f%%",
            colors=colors_donut[:len(counts)],
            startangle=90,
            pctdistance=0.8,
            wedgeprops=dict(width=0.55),
            textprops={"color": TEXT_WHITE, "fontsize": 8}
        )
        col_name = cat_cols[1] if len(cat_cols) > 1 else cat_cols[0] if len(cat_cols) > 0 else "Data"
        ax3.set_title(f"{col_name} Donut",
                     fontsize=11, fontweight="bold", color=TEXT_WHITE)

        # Chart 4 - Line Chart
        ax4 = fig.add_subplot(gs[2, :2])
        ax4.set_facecolor(BG_CARD)
        if len(numeric_cols) > 0:
            data_line = df[numeric_cols[0]].dropna()[:100]
            x_vals = range(len(data_line))
            ax4.plot(x_vals, data_line.values,
                    color=ACCENT1, linewidth=2, alpha=0.9)
            ax4.fill_between(x_vals, data_line.values,
                            alpha=0.15, color=ACCENT1)
            mean_val = data_line.mean()
            ax4.axhline(mean_val, color=ACCENT3, linestyle="--",
                       linewidth=1.5, label=f"Mean: {mean_val:.1f}")
            ax4.legend(fontsize=8, facecolor=BG_CARD,
                      labelcolor=TEXT_WHITE)
            ax4.set_title(f"{numeric_cols[0]} Trend",
                         fontsize=11, fontweight="bold", color=TEXT_WHITE)
        ax4.tick_params(colors=TEXT_GRAY)
        ax4.spines["top"].set_visible(False)
        ax4.spines["right"].set_visible(False)
        ax4.spines["left"].set_color(TEXT_GRAY)
        ax4.spines["bottom"].set_color(TEXT_GRAY)

        # Chart 5 - Histogram
        ax5 = fig.add_subplot(gs[2, 2:])
        ax5.set_facecolor(BG_CARD)
        if len(numeric_cols) > 0:
            data_hist = df[numeric_cols[0]].dropna()
            n, bins, patches = ax5.hist(data_hist, bins=20,
                                        color=ACCENT2,
                                        edgecolor="none", alpha=0.8)
            for i, patch in enumerate(patches):
                patch.set_facecolor(
                    plt.cm.Blues(0.3 + 0.7 * i / len(patches)))
            mean_val = data_hist.mean()
            ax5.axvline(mean_val, color=ACCENT3, linestyle="--",
                       linewidth=2, label=f"Mean: {mean_val:.1f}")
            ax5.legend(fontsize=8, facecolor=BG_CARD,
                      labelcolor=TEXT_WHITE)
            ax5.set_title(f"{numeric_cols[0]} Distribution",
                         fontsize=11, fontweight="bold", color=TEXT_WHITE)
        ax5.tick_params(colors=TEXT_GRAY)
        ax5.spines["top"].set_visible(False)
        ax5.spines["right"].set_visible(False)
        ax5.spines["left"].set_color(TEXT_GRAY)
        ax5.spines["bottom"].set_color(TEXT_GRAY)

        # Chart 6 - Summary Stats Box
        ax6 = fig.add_subplot(gs[3, :2])
        ax6.set_facecolor(BG_CARD)
        summary_text = (
            f"  DATASET SUMMARY\n\n"
            f"  Total Rows         : {df.shape[0]}\n"
            f"  Total Columns      : {df.shape[1]}\n"
            f"  Numeric Columns    : {len(numeric_cols)}\n"
            f"  Categorical Cols   : {len(cat_cols)}\n"
            f"  Missing Values     : {df.isnull().sum().sum()}\n"
            f"  Duplicate Rows     : {df.duplicated().sum()}"
        )
        ax6.text(0.05, 0.5, summary_text,
                transform=ax6.transAxes,
                ha="left", va="center",
                fontsize=11, color=TEXT_WHITE,
                fontfamily="monospace",
                bbox=dict(boxstyle="round,pad=0.5",
                         facecolor=PRIMARY, alpha=0.8))
        ax6.axis("off")
        ax6.set_title("Dataset Summary",
                     fontsize=11, fontweight="bold", color=TEXT_WHITE)

        # Chart 7 - Horizontal Bar Chart
        ax7 = fig.add_subplot(gs[3, 2:])
        ax7.set_facecolor(BG_CARD)
        if len(cat_cols) > 0:
            counts = df[cat_cols[0]].value_counts()[:6]
            colors_h = plt.cm.Blues(
                np.linspace(0.4, 0.9, len(counts)))
            bars = ax7.barh(counts.index, counts.values,
                           color=colors_h, edgecolor="none")
            for bar in bars:
                width = bar.get_width()
                ax7.text(width, bar.get_y() + bar.get_height()/2.,
                        f' {width}',
                        ha='left', va='center',
                        fontsize=8, color=TEXT_WHITE)
            ax7.set_title(f"Count by {cat_cols[0]}",
                         fontsize=11, fontweight="bold", color=TEXT_WHITE)
        ax7.tick_params(colors=TEXT_GRAY)
        ax7.spines["top"].set_visible(False)
        ax7.spines["right"].set_visible(False)
        ax7.spines["left"].set_color(TEXT_GRAY)
        ax7.spines["bottom"].set_color(TEXT_GRAY)

        # Set all axes background
        for ax in fig.get_axes():
            ax.set_facecolor(BG_CARD)
            ax.tick_params(colors=TEXT_GRAY)

        plt.savefig("charts/result.png", dpi=150,
                   bbox_inches="tight", facecolor=BG_DARK)
        plt.close()
        logger.info("Attractive dashboard created successfully!")
        return "charts/result.png"

    except Exception as e:
        logger.error(f"Error creating dashboard: {e}")
        return None

def bar_chart(df, x_col, y_col, title="Bar Chart"):
    return multi_chart_analysis(df, title)

def pie_chart(df, col, title="Pie Chart"):
    return multi_chart_analysis(df, title)

def donut_chart(df, col, title="Donut Chart"):
    return multi_chart_analysis(df, title)

def line_chart(df, x_col, y_col, title="Line Chart"):
    return multi_chart_analysis(df, title)

def histogram(df, col, title="Histogram"):
    return multi_chart_analysis(df, title)

def kpi_dashboard(df, title="KPI Dashboard"):
    return multi_chart_analysis(df, title)
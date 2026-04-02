import matplotlib.pyplot as plt
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

        # White background + dark bold colors
        BG_MAIN   = "#ffffff"
        BG_CARD   = "#ffffff"
        BG_HEADER = "#1a237e"
        COLOR1    = "#1a237e"   # dark navy blue
        COLOR2    = "#1b5e20"   # dark green
        COLOR3    = "#bf360c"   # dark orange red
        COLOR4    = "#880e4f"   # dark pink
        COLOR5    = "#4a148c"   # dark purple
        COLOR6    = "#006064"   # dark teal
        TEXT_DARK = "#212121"
        TEXT_GRAY = "#616161"
        TEXT_WHITE = "#ffffff"
        GRID_COLOR = "#eeeeee"

        CHART_COLORS = [COLOR1, COLOR2, COLOR3,
                        COLOR4, COLOR5, COLOR6]

        fig = plt.figure(figsize=(22, 15), facecolor=BG_MAIN)

        # Title banner
        fig.text(0.5, 0.97, title,
                 ha="center", va="top",
                 fontsize=22, fontweight="bold",
                 color=TEXT_WHITE,
                 bbox=dict(boxstyle="round,pad=0.4",
                           facecolor=BG_HEADER,
                           alpha=1.0))

        gs = gridspec.GridSpec(4, 4, figure=fig,
                               hspace=0.5, wspace=0.35,
                               top=0.92, bottom=0.04,
                               left=0.05, right=0.97)

        # ── KPI CARDS ──────────────────────────────────────────
        kpi_colors = [COLOR1, COLOR2, COLOR3, COLOR4]
        kpi_labels, kpi_values = [], []

        if len(numeric_cols) >= 4:
            for col in numeric_cols[:4]:
                kpi_labels.append(col)
                kpi_values.append(df[col].mean())
        elif len(numeric_cols) > 0:
            for col in numeric_cols:
                kpi_labels.append(col)
                kpi_values.append(df[col].mean())
            while len(kpi_labels) < 4:
                kpi_labels.append("Total Rows")
                kpi_values.append(len(df))
        else:
            kpi_labels = ["Total Rows", "Columns",
                          "Missing", "Duplicates"]
            kpi_values = [len(df), df.shape[1],
                          df.isnull().sum().sum(),
                          df.duplicated().sum()]

        for i in range(4):
            ax_k = fig.add_subplot(gs[0, i])
            ax_k.set_facecolor(BG_CARD)
            ax_k.set_xlim(0, 1)
            ax_k.set_ylim(0, 1)

            val = kpi_values[i]
            if val >= 1_000_000:
                dv = f"{val/1_000_000:.2f}M"
            elif val >= 1_000:
                dv = f"{val/1_000:.2f}K"
            else:
                dv = f"{val:.2f}"

            # colored top bar
            ax_k.axhspan(0.75, 1.0,
                         facecolor=kpi_colors[i],
                         alpha=1.0)
            ax_k.text(0.5, 0.87, kpi_labels[i],
                      transform=ax_k.transAxes,
                      ha="center", va="center",
                      fontsize=9, fontweight="bold",
                      color=TEXT_WHITE)
            ax_k.text(0.5, 0.47, dv,
                      transform=ax_k.transAxes,
                      ha="center", va="center",
                      fontsize=22, fontweight="bold",
                      color=kpi_colors[i])
            ax_k.text(0.5, 0.15, "Average",
                      transform=ax_k.transAxes,
                      ha="center", va="center",
                      fontsize=8, color=TEXT_GRAY)
            ax_k.set_xticks([])
            ax_k.set_yticks([])
            for sp in ax_k.spines.values():
                sp.set_edgecolor(kpi_colors[i])
                sp.set_linewidth(2)

        # ── BAR CHART ──────────────────────────────────────────
        ax1 = fig.add_subplot(gs[1, :2])
        ax1.set_facecolor(BG_CARD)
        if len(numeric_cols) > 0 and len(cat_cols) > 0:
            gd = df.groupby(
                cat_cols[0])[numeric_cols[0]].mean()
            bar_colors = [CHART_COLORS[i % len(CHART_COLORS)]
                          for i in range(len(gd))]
            bars = ax1.bar(gd.index, gd.values,
                           color=bar_colors,
                           edgecolor="white",
                           width=0.6)
            for b in bars:
                h = b.get_height()
                ax1.text(b.get_x() + b.get_width()/2, h,
                         f"{h:.1f}",
                         ha="center", va="bottom",
                         fontsize=8, color=TEXT_DARK,
                         fontweight="bold")
            ax1.set_title(
                f"{numeric_cols[0]} by {cat_cols[0]}",
                fontsize=11, fontweight="bold",
                color=TEXT_DARK, pad=8)
        elif len(numeric_cols) >= 2:
            means = df[numeric_cols[:6]].mean()
            bar_colors = [CHART_COLORS[i % len(CHART_COLORS)]
                          for i in range(len(means))]
            ax1.bar(means.index, means.values,
                    color=bar_colors, edgecolor="white")
            ax1.set_title("Average Values by Column",
                          fontsize=11, fontweight="bold",
                          color=TEXT_DARK, pad=8)
        ax1.tick_params(colors=TEXT_GRAY, rotation=30,
                        labelsize=8)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["left"].set_color(GRID_COLOR)
        ax1.spines["bottom"].set_color(GRID_COLOR)
        ax1.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
        ax1.set_axisbelow(True)

        # ── PIE CHART ──────────────────────────────────────────
        ax2 = fig.add_subplot(gs[1, 2])
        ax2.set_facecolor(BG_CARD)
        if len(cat_cols) > 0:
            counts = df[cat_cols[0]].value_counts()[:5]
            ax2.pie(
                counts,
                labels=counts.index,
                autopct="%1.1f%%",
                colors=CHART_COLORS[:len(counts)],
                startangle=90,
                pctdistance=0.78,
                wedgeprops=dict(edgecolor="white",
                                linewidth=2),
                textprops={"color": TEXT_DARK,
                           "fontsize": 8,
                           "fontweight": "bold"}
            )
            ax2.set_title(f"{cat_cols[0]} — Pie",
                          fontsize=11, fontweight="bold",
                          color=TEXT_DARK, pad=8)

        # ── DONUT CHART ────────────────────────────────────────
        ax3 = fig.add_subplot(gs[1, 3])
        ax3.set_facecolor(BG_CARD)
        src_col = cat_cols[1] if len(cat_cols) > 1 else \
                  cat_cols[0] if len(cat_cols) > 0 else None
        counts = df[src_col].value_counts()[:5] \
            if src_col else pd.Series([len(df)], index=["All"])
        ax3.pie(
            counts,
            labels=counts.index,
            autopct="%1.1f%%",
            colors=CHART_COLORS[:len(counts)],
            startangle=90,
            pctdistance=0.78,
            wedgeprops=dict(width=0.52,
                            edgecolor="white",
                            linewidth=2),
            textprops={"color": TEXT_DARK,
                       "fontsize": 8,
                       "fontweight": "bold"}
        )
        ax3.set_title(f"{src_col or 'Data'} — Donut",
                      fontsize=11, fontweight="bold",
                      color=TEXT_DARK, pad=8)

        # ── LINE CHART ─────────────────────────────────────────
        ax4 = fig.add_subplot(gs[2, :2])
        ax4.set_facecolor(BG_CARD)
        if len(numeric_cols) > 0:
            dl = df[numeric_cols[0]].dropna()[:100]
            xv = range(len(dl))
            ax4.plot(xv, dl.values,
                     color=COLOR1, linewidth=2.5)
            ax4.fill_between(xv, dl.values,
                             alpha=0.08, color=COLOR1)
            mv = dl.mean()
            ax4.axhline(mv, color=COLOR3,
                        linestyle="--", linewidth=1.5,
                        label=f"Mean: {mv:.1f}")
            ax4.legend(fontsize=8, facecolor=BG_CARD,
                       labelcolor=TEXT_DARK,
                       edgecolor=GRID_COLOR)
            ax4.set_title(f"{numeric_cols[0]} — Trend",
                          fontsize=11, fontweight="bold",
                          color=TEXT_DARK, pad=8)
        ax4.tick_params(colors=TEXT_GRAY, labelsize=8)
        ax4.spines["top"].set_visible(False)
        ax4.spines["right"].set_visible(False)
        ax4.spines["left"].set_color(GRID_COLOR)
        ax4.spines["bottom"].set_color(GRID_COLOR)
        ax4.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
        ax4.set_axisbelow(True)

        # ── HISTOGRAM ──────────────────────────────────────────
        ax5 = fig.add_subplot(gs[2, 2:])
        ax5.set_facecolor(BG_CARD)
        if len(numeric_cols) > 0:
            dh = df[numeric_cols[0]].dropna()
            n, bins, patches = ax5.hist(
                dh, bins=20,
                edgecolor="white",
                linewidth=0.8)
            for idx, patch in enumerate(patches):
                patch.set_facecolor(
                    CHART_COLORS[idx % len(CHART_COLORS)])
            mv = dh.mean()
            ax5.axvline(mv, color=COLOR3,
                        linestyle="--", linewidth=2,
                        label=f"Mean: {mv:.1f}")
            ax5.legend(fontsize=8, facecolor=BG_CARD,
                       labelcolor=TEXT_DARK,
                       edgecolor=GRID_COLOR)
            ax5.set_title(
                f"{numeric_cols[0]} — Histogram",
                fontsize=11, fontweight="bold",
                color=TEXT_DARK, pad=8)
        ax5.tick_params(colors=TEXT_GRAY, labelsize=8)
        ax5.spines["top"].set_visible(False)
        ax5.spines["right"].set_visible(False)
        ax5.spines["left"].set_color(GRID_COLOR)
        ax5.spines["bottom"].set_color(GRID_COLOR)
        ax5.yaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
        ax5.set_axisbelow(True)

        # ── SUMMARY BOX ────────────────────────────────────────
        ax6 = fig.add_subplot(gs[3, :2])
        ax6.set_facecolor(BG_CARD)
        summary = (
            f"  DATASET SUMMARY\n\n"
            f"  Total Rows         :  {df.shape[0]}\n"
            f"  Total Columns      :  {df.shape[1]}\n"
            f"  Numeric Columns    :  {len(numeric_cols)}\n"
            f"  Categorical Cols   :  {len(cat_cols)}\n"
            f"  Missing Values     :  {df.isnull().sum().sum()}\n"
            f"  Duplicate Rows     :  {df.duplicated().sum()}"
        )
        ax6.text(0.05, 0.5, summary,
                 transform=ax6.transAxes,
                 ha="left", va="center",
                 fontsize=11, color=TEXT_DARK,
                 fontfamily="monospace",
                 bbox=dict(boxstyle="round,pad=0.6",
                           facecolor="#e8eaf6",
                           edgecolor=COLOR1,
                           linewidth=2))
        ax6.axis("off")
        ax6.set_title("Dataset Summary",
                      fontsize=11, fontweight="bold",
                      color=TEXT_DARK, pad=8)

        # ── HORIZONTAL BAR ─────────────────────────────────────
        ax7 = fig.add_subplot(gs[3, 2:])
        ax7.set_facecolor(BG_CARD)
        if len(cat_cols) > 0:
            counts = df[cat_cols[0]].value_counts()[:6]
            hb_colors = [CHART_COLORS[i % len(CHART_COLORS)]
                         for i in range(len(counts))]
            bars = ax7.barh(counts.index, counts.values,
                            color=hb_colors,
                            edgecolor="white",
                            height=0.6)
            for b in bars:
                w = b.get_width()
                ax7.text(w, b.get_y() + b.get_height()/2,
                         f" {w}",
                         ha="left", va="center",
                         fontsize=8, color=TEXT_DARK,
                         fontweight="bold")
            ax7.set_title(f"Count by {cat_cols[0]}",
                          fontsize=11, fontweight="bold",
                          color=TEXT_DARK, pad=8)
        ax7.tick_params(colors=TEXT_GRAY, labelsize=8)
        ax7.spines["top"].set_visible(False)
        ax7.spines["right"].set_visible(False)
        ax7.spines["left"].set_color(GRID_COLOR)
        ax7.spines["bottom"].set_color(GRID_COLOR)
        ax7.xaxis.grid(True, color=GRID_COLOR, linewidth=0.8)
        ax7.set_axisbelow(True)

        plt.savefig("charts/result.png", dpi=150,
                    bbox_inches="tight",
                    facecolor=BG_MAIN)
        plt.close()
        logger.info("White dashboard created!")
        return "charts/result.png"

    except Exception as e:
        logger.error(f"Dashboard error: {e}")
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
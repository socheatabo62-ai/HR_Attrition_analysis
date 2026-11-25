"""Reusable chart and table builders."""
import pandas as pd
import plotly.express as px

STATUS_COLORS = {"Current": "#4c78a8", "Left": "#d62728"}


def _tidy(fig, title=None):
    fig.update_layout(margin=dict(l=10, r=10, t=50, b=10), legend_title_text="",
                      title=title)
    return fig


def rate_table(df, by, order=None):
    """Employees, leavers and attrition rate for each value of `by`."""
    g = (df.groupby(by).agg(Employees=("Left", "size"), Left=("Left", "sum"))
         .reset_index())
    g["Attrition rate (%)"] = g["Left"] / g["Employees"] * 100
    if order:
        pos = {v: i for i, v in enumerate(order)}
        g = g.sort_values(by, key=lambda s: s.map(pos))
    elif pd.api.types.is_numeric_dtype(g[by]):
        g = g.sort_values(by)
    else:
        g = g.sort_values("Attrition rate (%)", ascending=False)
    return g.reset_index(drop=True)


def rate_bar(df, by, title, order=None):
    g = rate_table(df, by, order)
    overall = df["Left"].mean() * 100
    fig = px.bar(g, x=by, y="Attrition rate (%)",
                 text=g["Attrition rate (%)"].round(1).astype(str) + "%",
                 hover_data=["Employees", "Left"],
                 color_discrete_sequence=["#d62728"])
    fig.update_xaxes(type="category", categoryorder="array",
                     categoryarray=[str(v) for v in g[by]], title=None)
    fig.add_hline(y=overall, line_dash="dash", line_color="grey",
                  annotation_text=f"Overall {overall:.1f}%")
    fig.update_traces(textposition="outside")
    return _tidy(fig, title), g


def headcount_bar(df, by, title):
    g = df.groupby([by, "Status"]).size().reset_index(name="Employees")
    fig = px.bar(g, x=by, y="Employees", color="Status", barmode="stack",
                 color_discrete_map=STATUS_COLORS)
    fig.update_xaxes(title=None)
    return _tidy(fig, title)


def histogram(df, col, title, nbins=30):
    fig = px.histogram(df, x=col, color="Status", barmode="overlay", opacity=0.65,
                       nbins=nbins, color_discrete_map=STATUS_COLORS)
    return _tidy(fig, title)

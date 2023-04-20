from util import *
from typing import Tuple
import plotly.express as px
import polars as pl

def normalize_data(df: pl.LazyFrame) -> pl.LazyFrame:
    benchmark_start = df.select(pl.col("timestamp").min() / 1_000).collect()
    return df.select([
        pl.col("topic"),
        pl.col("key"),
        # milliseconds to seconds
        pl.col("timestamp") / 1_000,
        # Unix time in seconds
        pl.col("first_timestamp").flatten().arr.get(1).cast(pl.Float64)
    ]).select([
        pl.all(),
        (pl.col("timestamp") - pl.col("first_timestamp")).alias("difference"),
        (pl.col("timestamp") - benchmark_start).alias("timestamp_relative")
    ])

def get_basic_stats(df: pl.DataFrame) -> pl.DataFrame:
    return df.groupby("topic").agg([
        pl.col("difference").max().alias("max"),
        pl.col("difference").min().alias("min"),
        pl.col("difference").mean().alias("avg"),
        pl.col("difference").median().alias("median"),
        pl.col("difference").std().alias("std"),
        pl.col("topic").count().alias("samples"),
    ])

def plot_stats(stats: pl.DataFrame):
    df = stats.to_pandas()  # Expensive operation, but simplifies code a lot
    fig = px.bar(
        df,
        x="topic", y=["max", "avg", "median", "std","min"],
        barmode='group',
        labels={
            "value": "Latency (in seconds)",
            "topic": "Kafka topic"
        }
    )
    return fig
def divide_by_topics(df: pl.DataFrame) -> Tuple[pl.DataFrame, pl.DataFrame, pl.DataFrame]:
    edge = df.filter(pl.col("topic").str.ends_with("edge-output"))
    fog = df.filter(pl.col("topic").str.ends_with("fog-output"))
    cloud = df.filter(pl.col("topic").str.ends_with("cloud-output"))
    return edge, fog, cloud


def plot_latency_on_topics_over_time(edge: pl.DataFrame, fog: pl.DataFrame, cloud: pl.DataFrame):
    fig = px.scatter()
    fig.add_scatter(
        name="edge",
        x=edge["timestamp_relative"],
        y=edge["difference"],
    ).add_scatter(
        name="fog",
        x=fog["timestamp_relative"],
        y=fog["difference"],
    ).add_scatter(
        name="cloud",
        x=cloud["timestamp_relative"],
        y=cloud["difference"],
    )

    fig.update_layout(
        xaxis_title="Seconds since the start of the benchmark",
        yaxis_title="Response time latency (in seconds)"
    )
    return fig


def plot_performance_comparison_box(openfaas: pl.DataFrame, fission: pl.DataFrame):
    fig = px.box()
    fig.add_box(y=openfaas["difference"], name="openfaas")
    fig.add_box(y=fission["difference"], name="fission")
    fig.update_layout(
        xaxis_title="Serverless platforms",
        yaxis_title="Response time (in seconds)"
    )
    return fig


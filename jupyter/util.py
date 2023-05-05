from typing import Dict

import plotly.express as px
import polars as pl


def normalize_data(df: pl.LazyFrame) -> pl.LazyFrame:
    benchmark_start = df.select(pl.col("timestamp").min() / 1_000).collect()
    return df.select([
        pl.col("topic"),
        pl.col("key"),
        # Message written on output topic. Milliseconds to seconds
        pl.col("timestamp") / 1_000,
        # When the message was first sent to Kafka. Unix time in seconds
        pl.col("first_timestamp").flatten().arr.get(1).cast(pl.Float64)
    ]).select([
        pl.all(),
        # Time elapsed between sending the request and receiving the result
        (pl.col("timestamp") - pl.col("first_timestamp")).alias("difference"),
        # Seconds since the start of the benchmark
        (pl.col("timestamp") - benchmark_start).alias("timestamp_relative")
    ])


def normalize_data_kafkaml(df: pl.LazyFrame, benchmark_start: float, clients=1) -> pl.LazyFrame:
    # Get approximated values
    values = []
    last = 0
    for stage in range(1, 5):
        for message in range(100):
            last = last + (1 / stage) # + .012 # TODO simulated latency between messages
            for client in range(clients):
                values.append(last)
    base = pl.DataFrame({"first_timestamp": values}) + benchmark_start

    return (
        df.with_column((pl.col("timestamp") / 1_000))
        .sort("timestamp")
        .with_row_count("indx")
        .join(base.lazy().with_row_count("indx"), on="indx")
        .with_column((pl.col("timestamp") - pl.col("timestamp").min()).alias("timestamp_relative"))
        # Time elapsed between sending the request and receiving the result
        .with_column((pl.col("timestamp") - pl.col("first_timestamp")).alias("difference"))
        .with_column(pl.col("difference") - pl.col("difference").min())
    )


def elapsed(df: pl.DataFrame) -> float:
    return df.select(pl.col("timestamp").max() - pl.col("timestamp").min()).item()


def get_stats(df: pl.DataFrame) -> pl.DataFrame:
    return df.groupby("topic").agg([
        pl.col("difference").max().alias("max"),
        pl.col("difference").min().alias("min"),
        pl.col("difference").mean().alias("avg"),
        pl.col("difference").median().alias("median"),
        pl.col("difference").std().alias("std"),
        pl.col("topic").count().alias("samples"),
    ])


def divide_by_topics(df: pl.DataFrame) -> dict[str, pl.DataFrame]:
    edge = df.filter(pl.col("topic").str.contains("edge"))
    fog = df.filter(pl.col("topic").str.contains("fog"))
    cloud = df.filter(pl.col("topic").str.contains("cloud"))
    return {"edge": edge, "fog": fog, "cloud": cloud}


def plot_request_latency(values: Dict[str, pl.DataFrame]):
    fig = px.scatter()
    for k, df in values.items():
        fig.add_scatter(
            name=k,
            x=df["timestamp_relative"],
            y=df["difference"],
        )
    fig.update_layout(
        xaxis_title="Seconds since the start of the benchmark",
        yaxis_title="Response time latency (in seconds)",
    )
    return fig


def plot_latency_box(values: Dict[str, pl.DataFrame]):
    fig = px.box()
    for k, df in values.items():
        fig.add_box(y=df["difference"], name=k)
    fig.update_layout(
        xaxis_title="Serverless platform layer",
        yaxis_title="Response time (in seconds)",
        showlegend=False,
    )
    return fig

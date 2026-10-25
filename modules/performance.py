
import time
import pandas as pd


def benchmark_processing(df):

    sample_sizes = [1000, 5000, 10000, 25000, 50000]

    results = []

    for size in sample_sizes:

        sample = df.head(size).copy()

        start = time.perf_counter()

        # Example analytics operations
        sample = sample.drop_duplicates()

        summary = sample.groupby(
            "proto"
        )["sbytes"].agg(
            ["count", "mean", "sum"]
        )

        duration = time.perf_counter() - start

        results.append({
            "Records": len(sample),
            "Processing Time (seconds)": round(
                duration, 6
            )
        })

    return pd.DataFrame(results)


import pandas as pd


def prepare_stream(df, sample_size=2000):
    """
    Create a reproducible event replay sample.
    This is simulated order, not actual timestamps.
    """
    sample_size = min(sample_size, len(df))

    stream = df.sample(
        n=sample_size,
        random_state=42
    ).reset_index(drop=True)

    stream["event_number"] = range(
        1, len(stream) + 1
    )

    return stream


def get_stream_metrics(events):
    """
    Calculate metrics for events processed so far.
    """
    total = len(events)

    if total == 0:
        return {
            "total": 0,
            "suspicious": 0,
            "high": 0,
            "normal": 0,
            "flag_rate": 0.0
        }

    suspicious = int(events["suspicious"].sum())

    high = int(
        (events["risk_level"] == "High").sum()
    )

    return {
        "total": total,
        "suspicious": suspicious,
        "high": high,
        "normal": total - suspicious,
        "flag_rate": suspicious / total * 100
    }


def get_activity_data(events, batch_size=25):
    """
    Group replayed events into batches
    for the activity chart.
    """
    if events.empty:
        return pd.DataFrame(
            columns=[
                "Batch",
                "Total Events",
                "Flagged Events"
            ]
        )

    data = events.copy()

    data["Batch"] = (
        data.index // batch_size
    ) + 1

    activity = data.groupby(
        "Batch", as_index=False
    ).agg(
        **{
            "Total Events": (
                "event_number", "count"
            ),
            "Flagged Events": (
                "suspicious", "sum"
            )
        }
    )

    return activity


import streamlit as st
import plotly.express as px

from modules.preprocessing import (
    load_data,
    preprocess_data
)
from modules.threat_detection import detect_threats
from modules.stream_simulator import (
    prepare_stream,
    get_stream_metrics,
    get_activity_data
)

from modules.ui_components import (
    apply_custom_style,
    page_header,
    show_sidebar_info
)

st.set_page_config(
    page_title="Live Simulation | CyberWatch",
    page_icon="📡",
    layout="wide"
)

apply_custom_style()
show_sidebar_info()

page_header(
    title="Live Threat Monitoring",
    subtitle=(
        "Observe incoming simulated network events "
        "and automatically generated security alerts."
    ),
    section="CYBERWATCH / LIVE OPERATIONS"
)

st.info(
    "This page replays historical records in a "
    "randomized order. It does not monitor live "
    "network traffic."
)


@st.cache_data(show_spinner="Preparing event stream...")
def load_stream():
    df = preprocess_data(load_data())

    detected_df, thresholds = detect_threats(df)

    stream = prepare_stream(
        detected_df,
        sample_size=2000
    )

    return stream


try:
    stream = load_stream()

except Exception as error:
    st.error(f"Failed to load data: {error}")
    st.stop()


# Initialize session variables
if "cw_position" not in st.session_state:
    st.session_state.cw_position = 0

if "cw_running" not in st.session_state:
    st.session_state.cw_running = False


@st.fragment(run_every="1s")
def live_monitor():

    st.subheader("Simulation Controls")

    col1, col2, col3, col4 = st.columns(
        [1, 1, 1, 2]
    )

    with col1:
        if st.button(
            "▶ Start",
            use_container_width=True
        ):
            if st.session_state.cw_position >= len(stream):
                st.session_state.cw_position = 0

            st.session_state.cw_running = True

    with col2:
        if st.button(
            "⏸ Pause",
            use_container_width=True
        ):
            st.session_state.cw_running = False

    with col3:
        if st.button(
            "↻ Reset",
            use_container_width=True
        ):
            st.session_state.cw_running = False
            st.session_state.cw_position = 0

    with col4:
        speed = st.select_slider(
            "Events per update",
            options=[5, 10, 20, 50, 100],
            value=20
        )

    # Process next batch while running
    if st.session_state.cw_running:

        new_position = (
            st.session_state.cw_position + speed
        )

        st.session_state.cw_position = min(
            new_position,
            len(stream)
        )

        if st.session_state.cw_position >= len(stream):
            st.session_state.cw_running = False

    position = st.session_state.cw_position

    # Only show processed events
    processed = stream.iloc[:position].copy()

    metrics = get_stream_metrics(processed)

    # Simulation status
    if st.session_state.cw_running:
        st.success("🟢 Event stream running")

    elif position >= len(stream):
        st.success("✅ Simulation completed")

    else:
        st.warning("🟡 Simulation paused")

    st.progress(
        position / len(stream),
        text=f"Processed {position:,} of "
             f"{len(stream):,} events"
    )

    st.divider()

    # Live counters
    st.subheader("Live Network Monitoring")

    a, b, c, d = st.columns(4)

    a.metric(
        "Processed Events",
        f"{metrics['total']:,}"
    )

    b.metric(
        "Unflagged Events",
        f"{metrics['normal']:,}"
    )

    c.metric(
        "Suspicious Events",
        f"{metrics['suspicious']:,}"
    )

    d.metric(
        "High Risk Events",
        f"{metrics['high']:,}"
    )

    st.divider()

    # Activity chart
    st.subheader("Live Network Activity")

    if not processed.empty:

        activity = get_activity_data(processed)

        fig = px.line(
            activity,
            x="Batch",
            y=[
                "Total Events",
                "Flagged Events"
            ],
            markers=True,
            title="Event Activity by Replay Batch"
        )

        fig.update_layout(
            xaxis_title="Replay Batch",
            yaxis_title="Number of Events",
            legend_title="Event Category"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.info(
            "Press Start to begin receiving "
            "simulated network events."
        )

    st.divider()

    # Security alerts
    st.subheader("🚨 Security Alerts")

    if not processed.empty:

        alerts = processed[
            processed["suspicious"]
        ].tail(5).iloc[::-1]

        if alerts.empty:
            st.success(
                "No suspicious activity detected "
                "in processed events."
            )

        else:
            for _, event in alerts.iterrows():

                risk = event["risk_level"]
                reason = event["alert_reason"]
                event_id = event["event_number"]

                if risk == "High":
                    st.error(
                        f"🔴 HIGH RISK | Event #{event_id} "
                        f"| {reason}"
                    )

                else:
                    st.warning(
                        f"🟠 MEDIUM RISK | Event #{event_id} "
                        f"| {reason}"
                    )

    st.divider()

    # Latest events
    st.subheader("Recent Network Events")

    if not processed.empty:

        columns = [
            "event_number",
            "proto",
            "service",
            "sbytes",
            "dur",
            "rate",
            "risk_level",
            "alert_reason"
        ]

        recent = (
            processed[columns]
            .tail(15)
            .iloc[::-1]
        )

        st.dataframe(
            recent,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No events processed yet.")


live_monitor()

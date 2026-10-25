
import streamlit as st
import plotly.express as px

from modules.preprocessing import (
    load_data,
    preprocess_data
)
from modules.threat_detection import detect_threats

from modules.ui_components import (
    apply_custom_style,
    page_header,
    show_sidebar_info
)


st.set_page_config(
    page_title="Threat Detection | CyberWatch",
    page_icon="🚨",
    layout="wide"
)

apply_custom_style()
show_sidebar_info()

page_header(
    title="Threat Detection Center",
    subtitle=(
        "Identify suspicious network activity "
        "using statistical detection rules."
    ),
    section="CYBERWATCH / THREAT INTELLIGENCE"
)


@st.cache_data
def get_threat_data():
    df = preprocess_data(load_data())
    return detect_threats(df)


try:
    with st.spinner("Analyzing network traffic..."):
        df, thresholds = get_threat_data()

    # Overall metrics
    total_events = len(df)
    suspicious_count = int(df["suspicious"].sum())
    high_risk_count = int(
        (df["risk_level"] == "High").sum()
    )

    detection_rate = (
        suspicious_count / total_events * 100
        if total_events else 0
    )

    st.subheader("Threat Monitoring Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Events",
        f"{total_events:,}"
    )

    col2.metric(
        "Flagged Events",
        f"{suspicious_count:,}"
    )

    col3.metric(
        "High Risk Events",
        f"{high_risk_count:,}"
    )

    col4.metric(
        "Flagged Event Rate",
        f"{detection_rate:.2f}%"
    )

    st.divider()

    # Visualization section
    left, right = st.columns(2)

    with left:
        st.subheader("Risk Level Distribution")

        risk_counts = (
            df["risk_level"]
            .value_counts()
            .reindex(
                ["Low", "Medium", "High"],
                fill_value=0
            )
            .reset_index()
        )

        risk_counts.columns = [
            "Risk Level", "Count"
        ]

        fig = px.pie(
            risk_counts,
            names="Risk Level",
            values="Count",
            color="Risk Level",
            color_discrete_map={
                "Low": "#22c55e",
                "Medium": "#f59e0b",
                "High": "#ef4444"
            },
            hole=0.55
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:
        st.subheader("Triggered Detection Rules")

        rule_counts = {
            "High Traffic Volume": int(
                df["high_bytes"].sum()
            ),
            "Long Duration": int(
                df["long_duration"].sum()
            ),
            "High Traffic Rate": int(
                df["high_rate"].sum()
            )
        }

        fig = px.bar(
            x=list(rule_counts.keys()),
            y=list(rule_counts.values()),
            labels={
                "x": "Detection Rule",
                "y": "Events Flagged"
            },
            color=list(rule_counts.keys()),
            title="Rule Trigger Frequency"
        )
        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # Show calculated thresholds
    with st.expander("View Statistical Thresholds"):
        st.write(
            "Reference thresholds calculated "
            "from normal-labeled traffic "
            "using the 99th percentile."
        )

        st.json(thresholds)

    st.subheader("Security Alert Investigation")

    risk_filter = st.selectbox(
        "Filter events by risk level",
        ["All", "Low", "Medium", "High"]
    )

    filtered = df.copy()

    if risk_filter != "All":
        filtered = filtered[
            filtered["risk_level"] == risk_filter
        ]

    display_columns = [
        "id",
        "proto",
        "service",
        "dur",
        "sbytes",
        "rate",
        "risk_score",
        "risk_level",
        "alert_reason",
        "attack_cat",
        "label"
    ]

    available_columns = [
        col for col in display_columns
        if col in filtered.columns
    ]

    st.dataframe(
        filtered[available_columns].head(500),
        use_container_width=True
    )

    # Export filtered results
    csv_data = filtered[
        available_columns
    ].to_csv(index=False)

    st.download_button(
        label="⬇️ Download Investigation Results",
        data=csv_data,
        file_name="cyberwatch_alerts.csv",
        mime="text/csv"
    )

    st.success(
        "Threat detection analysis completed!"
    )

except Exception as error:
    st.error(f"Error: {error}")

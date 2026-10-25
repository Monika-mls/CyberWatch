
import streamlit as st
import plotly.express as px

from modules.preprocessing import (
    load_data,
    preprocess_data
)

from modules.ui_components import (
    apply_custom_style,
    page_header,
    section_title,
    show_sidebar_info
)

def style_chart(fig, height=420):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E293B",
        plot_bgcolor="#1E293B",
        font=dict(
            family="Arial",
            size=14,
            color="#F8FAFC"
        ),
        title_font=dict(
            size=18,
            color="#FFFFFF"
        ),
        height=height,
        margin=dict(l=35, r=35, t=70, b=60)
    )

    fig.update_xaxes(
        tickfont=dict(color="#E2E8F0"),
        gridcolor="#334155"
    )

    fig.update_yaxes(
        tickfont=dict(color="#E2E8F0"),
        gridcolor="#334155"
    )

    return fig

st.set_page_config(
    page_title="CyberWatch | Security Overview",
    page_icon="🛡️",
    layout="wide"
)

apply_custom_style()
show_sidebar_info()

page_header(
    title="Security Operations Overview",
    subtitle=(
        "Explore network traffic, attack patterns, "
        "and security intelligence."
    ),
    section="CYBERWATCH / COMMAND CENTER"
)


@st.cache_data
def get_data():
    df = load_data()
    return preprocess_data(df)


try:
    df = get_data()

except Exception as error:
    st.error(f"Could not load dataset: {error}")
    st.stop()


# Calculate dataset metrics
total_events = len(df)
attack_events = int((df["label"] == 1).sum())
normal_events = int((df["label"] == 0).sum())

attack_rate = (
    attack_events / total_events * 100
    if total_events else 0
)

unique_categories = (
    df.loc[df["label"] == 1, "attack_cat"]
    .nunique()
)


# -----------------------------
# METRIC CARDS
# -----------------------------

section_title(
    "Network Intelligence",
    "Overview of the loaded UNSW-NB15 dataset"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Network Events",
    f"{total_events:,}"
)

col2.metric(
    "Attack-Labeled Events",
    f"{attack_events:,}"
)

col3.metric(
    "Normal Events",
    f"{normal_events:,}"
)

col4.metric(
    "Attack Proportion",
    f"{attack_rate:.2f}%"
)

st.divider()


# -----------------------------
# ATTACK ANALYSIS
# -----------------------------

section_title(
    "Threat Landscape",
    "Distribution of known attack categories"
)

attack_df = df[df["label"] == 1]

attack_counts = (
    attack_df["attack_cat"]
    .value_counts()
    .reset_index()
)

attack_counts.columns = [
    "Attack Category",
    "Event Count"
]

left, right = st.columns([3, 2])


with left:
    chart_data = attack_counts.sort_values(
        "Event Count",
        ascending=True
    )

    fig = px.bar(
        chart_data,
        x="Event Count",
        y="Attack Category",
        orientation="h",
        color="Event Count",
        color_continuous_scale=[
            "#155E75",
            "#0891B2",
            "#67E8F9"
        ],
        title="Attack Categories"
    )

    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False
    )

    fig = style_chart(fig, height=480)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with right:
    fig = px.pie(
        names=["Normal", "Attack"],
        values=[normal_events, attack_events],
        hole=0.65,
        color=["Normal", "Attack"],
        color_discrete_map={
            "Normal": "#00D4FF",
            "Attack": "#EF4444"
        },
        title="Normal vs Attack Traffic"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#121D30",
        font_color="#CBD5E1"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# -----------------------------
# DATA EXPLORATION
# -----------------------------

st.divider()

section_title(
    "Network Event Explorer",
    "Filter and inspect the collected records"
)

filter_options = [
    "All"
] + sorted(df["attack_cat"].dropna().unique().tolist())

selected_category = st.selectbox(
    "Select Attack Category",
    filter_options
)

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["attack_cat"] == selected_category
    ]

st.caption(
    f"Showing {len(filtered_df):,} matching records"
)

st.dataframe(
    filtered_df.head(250),
    use_container_width=True,
    hide_index=True
)


# -----------------------------
# DOWNLOAD
# -----------------------------

st.download_button(
    "⬇️ Export Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="cyberwatch_network_events.csv",
    mime="text/csv"
)

st.divider()

st.caption(
    "CyberWatch | Big Data Analytics CBP | "
    "Source: UNSW-NB15 research dataset"
)

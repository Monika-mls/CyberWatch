
import streamlit as st

from modules.preprocessing import (
    load_data,
    preprocess_data
)

from modules.ui_components import (
    apply_custom_style,
    show_sidebar_info
)


# ==========================================
# CYBERWATCH HOME PAGE
# ==========================================

apply_custom_style()
show_sidebar_info()


# ==========================================
# LOAD DATASET STATISTICS
# ==========================================

@st.cache_data(show_spinner=False)
def get_home_metrics():

    df = preprocess_data(load_data())

    total_events = len(df)

    attack_events = int(
        (df["label"] == 1).sum()
    )

    normal_events = int(
        (df["label"] == 0).sum()
    )

    attack_categories = int(
        df.loc[
            df["label"] == 1,
            "attack_cat"
        ].nunique()
    )

    return (
        total_events,
        attack_events,
        normal_events,
        attack_categories
    )


# ==========================================
# WELCOME SECTION
# ==========================================

st.caption(
    "🛡️ CYBERWATCH / SECURITY INTELLIGENCE PLATFORM"
)

st.title("Welcome to CyberWatch")

st.markdown(
    """
    ### Intelligent Cybersecurity Monitoring
    Powered by Big Data Analytics

    CyberWatch is an interactive cybersecurity
    analytics platform designed to explore network
    traffic, detect suspicious behavior, simulate
    security events, and evaluate threat detection
    performance using statistical techniques.
    """
)

st.info(
    "SYSTEM MODE: Historical Cybersecurity Data "
    "+ Simulated Real-Time Monitoring"
)

st.divider()


# ==========================================
# PLATFORM STATISTICS
# ==========================================

st.subheader("📊 Platform Overview")

st.caption(
    "Statistics obtained from the UNSW-NB15 "
    "cybersecurity dataset."
)

try:

    total, attacks, normal, categories = (
        get_home_metrics()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Network Events",
            f"{total:,}"
        )

    with col2:
        st.metric(
            "Attack-Labeled Events",
            f"{attacks:,}"
        )

    with col3:
        st.metric(
            "Normal Events",
            f"{normal:,}"
        )

    with col4:
        st.metric(
            "Attack Categories",
            categories
        )

except Exception as error:

    st.warning(
        "Unable to load dataset statistics: "
        f"{error}"
    )


st.divider()


# ==========================================
# MODULE NAVIGATION
# ==========================================

st.subheader("🚀 Explore CyberWatch")

st.caption(
    "Navigate through the different modules "
    "of the cybersecurity analytics platform."
)


# ROW 1

col1, col2 = st.columns(2)

with col1:

    with st.container(border=True):

        st.subheader("📊 Security Overview")

        st.write(
            "Explore network traffic statistics, "
            "attack categories, traffic distributions, "
            "and interactive cybersecurity charts."
        )

        st.page_link(
            "pages/0_Security_Overview.py",
            label="Open Security Overview",
            icon="📊",
            use_container_width=True
        )


with col2:

    with st.container(border=True):

        st.subheader("🚨 Threat Detection")

        st.write(
            "Detect potentially suspicious network "
            "activities using statistical thresholds, "
            "risk scores, and explainable security alerts."
        )

        st.page_link(
            "pages/1_Threat_Detection.py",
            label="Open Threat Detection",
            icon="🚨",
            use_container_width=True
        )


# ROW 2

col3, col4 = st.columns(2)

with col3:

    with st.container(border=True):

        st.subheader("📡 Live Threat Simulation")

        st.write(
            "Simulate incoming network events, "
            "monitor changing security metrics, "
            "and observe dynamically generated alerts."
        )

        st.page_link(
            "pages/2_Live_Simulation.py",
            label="Open Live Simulation",
            icon="📡",
            use_container_width=True
        )


with col4:

    with st.container(border=True):

        st.subheader("📈 Detection Evaluation")

        st.write(
            "Evaluate rule-based threat detection "
            "using accuracy, precision, recall, "
            "F1-score, and a confusion matrix "
            "on the independent testing dataset."
        )

        st.page_link(
            "pages/3_Detection_Evaluation.py",
            label="Open Detection Evaluation",
            icon="📈",
            use_container_width=True
        )


st.divider()


# ==========================================
# PROJECT WORKFLOW
# ==========================================

st.subheader("⚙️ How CyberWatch Works")

st.caption(
    "CyberWatch follows a structured "
    "Big Data Analytics workflow."
)


with st.container(border=True):

    st.markdown(
        """
        **1. Data Collection**

        Network traffic records are obtained from
        the UNSW-NB15 cybersecurity dataset.

        **2. Data Preprocessing**

        Data is cleaned by handling missing values,
        duplicate records, and invalid entries.

        **3. Statistical Analysis**

        Traffic characteristics are analyzed using
        distributions, averages, and percentile
        calculations.

        **4. Threat Detection**

        Rule-based methods identify potentially
        suspicious activity and assign risk levels.

        **5. Live Event Simulation**

        Historical records are replayed in batches
        to demonstrate streaming analytics.

        **6. Performance Evaluation**

        Detection results are compared with known
        labels using accuracy, precision, recall,
        F1-score, and confusion matrix analysis.
        """
    )


with st.container(border=True):

    st.subheader("🗂️ Data Management & Reports")

    st.write(
        "Inspect dataset quality, review preprocessing "
        "results, analyze statistical data, and generate "
        "downloadable cybersecurity reports."
    )

    st.page_link(
        "pages/4_Data_Management.py",
        label="Open Data Management",
        icon="🗂️",
        use_container_width=True
    )

st.divider()


# ==========================================
# TECHNOLOGY STACK
# ==========================================

st.subheader("💻 Technology Stack")

st.caption(
    "Technologies used to build and operate CyberWatch."
)

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:
    with st.container(border=True):
        st.markdown("### 🐍 Python")
        st.caption("Core Programming")

with tech2:
    with st.container(border=True):
        st.markdown("### 📊 Streamlit")
        st.caption("Web Application")

with tech3:
    with st.container(border=True):
        st.markdown("### 📁 Pandas")
        st.caption("Data Processing")

with tech4:
    with st.container(border=True):
        st.markdown("### 📈 Plotly")
        st.caption("Data Visualization")


st.divider()


# ==========================================
# PROJECT INFORMATION
# ==========================================

st.subheader("ℹ️ About the Project")

with st.expander("View Project Information"):

    st.markdown(
        """
        **Project Title:** CyberWatch: A Stream-Based
        Cybersecurity Threat Analytics and
        Visualization Platform

        **Course:** Big Data Analytics

        **Project Type:** Course-Based Project (CBP)

        **Dataset:** UNSW-NB15

        **Programming Language:** Python

        **Application Framework:** Streamlit

        **Core Concepts:**
        - Data Collection and Preprocessing
        - Statistical Data Analysis
        - Stream Data Simulation
        - Rule-Based Anomaly Detection
        - Interactive Data Visualization
        - Detection Performance Evaluation

        **Objective:**

        To develop an interactive cybersecurity
        analytics platform capable of identifying
        unusual network traffic patterns and
        visualizing security insights through
        statistical analysis and simulated
        real-time monitoring.
        """
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "🛡️ CyberWatch | Big Data Analytics "
    "Course-Based Project"
)

st.caption(
    "UNSW-NB15 Research Dataset | "
    "Statistical Threat Analytics | "
    "Simulated Event Monitoring"
)

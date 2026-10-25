
import streamlit as st

st.set_page_config(
    page_title="CyberWatch",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

pages = {
    "CyberWatch": [
        st.Page(
            "app.py",
            title="Home",
            icon="🏠",
            default=True
        ),

        st.Page(
            "pages/0_Security_Overview.py",
            title="Security Overview",
            icon="📊"
        ),

        st.Page(
            "pages/1_Threat_Detection.py",
            title="Threat Detection",
            icon="🚨"
        ),

        st.Page(
            "pages/2_Live_Simulation.py",
            title="Live Simulation",
            icon="📡"
        ),

        st.Page(
            "pages/3_Detection_Evaluation.py",
            title="Detection Evaluation",
            icon="📈"
        ),

        st.Page(
            "pages/4_Data_Management.py",
            title="Data Management & Reports",
            icon="🗂️"
        ),
        st.Page(
            "pages/5_Performance_Analysis.py",
            title="Performance Analysis",
            icon="⏱️"
        )
    ]
}

pg = st.navigation(pages)
pg.run()

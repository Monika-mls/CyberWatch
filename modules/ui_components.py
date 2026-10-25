
import streamlit as st


# ==========================================
# GLOBAL CYBERWATCH STYLING
# ==========================================

def apply_custom_style():

    st.markdown(
        """
<style>

/* MAIN APPLICATION BACKGROUND */

.stApp {
    background:
        radial-gradient(
            circle at top left,
            rgba(0, 180, 255, 0.10),
            transparent 28%
        ),
        radial-gradient(
            circle at top right,
            rgba(0, 140, 255, 0.07),
            transparent 25%
        ),
        linear-gradient(
            180deg,
            #020817 0%,
            #061225 50%,
            #030B18 100%
        );

    color: #EAF4FF;
}


/* MAIN PAGE SPACING */

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 2.5rem;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #071120,
        #0A1628
    );

    border-right: 1px solid #203954;
}


/* HEADINGS */

h1, h2, h3, h4 {
    color: #F8FBFF;
}


/* ==========================================
   NATIVE HEADER CONTAINER STYLING
========================================== */

/*
   We use Streamlit's native container instead
   of injecting HTML for the header.
*/

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px;
}


/* ==========================================
   METRIC CARDS
========================================== */

div[data-testid="stMetric"] {
    background: linear-gradient(
        180deg,
        #0C1B30 0%,
        #091526 100%
    );

    border: 1px solid rgba(
        0, 212, 255, 0.22
    );

    border-radius: 15px;
    padding: 20px;

    min-height: 120px;

    box-shadow:
        0 0 15px rgba(0, 180, 255, 0.06);
}


div[data-testid="stMetricLabel"] {
    color: #B4CBE2;
    font-size: 14px;
    font-weight: 500;
}


div[data-testid="stMetricValue"] {
    color: #FFFFFF;
    font-size: 29px;
    font-weight: 700;
}


/* ==========================================
   DATA TABLES
========================================== */

div[data-testid="stDataFrame"] {
    border: 1px solid #245371;
    border-radius: 12px;
    overflow: hidden;
}


/* ==========================================
   BUTTONS
========================================== */

div.stButton > button {
    background: #102840;
    color: #FFFFFF;

    border: 1px solid #245371;
    border-radius: 10px;

    font-weight: 600;
}


div.stButton > button:hover {
    background: #123550;
    border-color: #22D3EE;
    color: #FFFFFF;
}


/* DOWNLOAD BUTTONS */

div[data-testid="stDownloadButton"] > button {
    background: #102840;
    color: #FFFFFF;

    border: 1px solid #245371;
    border-radius: 10px;
}


/* ==========================================
   INPUTS AND DROPDOWNS
========================================== */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #0B1C30 !important;

    border: 1px solid #2A4B66 !important;
    border-radius: 9px !important;

    color: #FFFFFF !important;
}


/* ==========================================
   ALERTS
========================================== */

div[data-testid="stAlert"] {
    border-radius: 12px;
}


/* ==========================================
   DIVIDERS
========================================== */

hr {
    border-color: #203954;
}

</style>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# PAGE HEADER
# NO CUSTOM HTML USED
# ==========================================

def page_header(
    title,
    subtitle,
    section="CYBERWATCH"
):

    # Native Streamlit bordered container
    with st.container(border=True):

        left, right = st.columns(
            [4, 1],
            vertical_alignment="top"
        )

        with left:

            st.caption(
                f"🛡️ {section}"
            )

            st.markdown(
                f"## {title}"
            )

            st.write(subtitle)

        with right:

            st.success(
                "● SYSTEM ONLINE"
            )

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption(
                "◈ UNSW-NB15 Dataset"
            )

        with col2:
            st.caption(
                "◈ Threat Analytics Enabled"
            )

        with col3:
            st.caption(
                "◈ Simulation Mode"
            )


# ==========================================
# SECTION TITLE
# ==========================================

def section_title(
    title,
    description=None
):

    st.subheader(title)

    if description:
        st.caption(description)


# ==========================================
# SIDEBAR INFORMATION
# ==========================================

def show_sidebar_info():

    with st.sidebar:

        st.markdown(
            "## 🛡️ CyberWatch"
        )

        st.caption(
            "Cybersecurity Threat Monitoring "
            "and Analytics Platform"
        )

        st.divider()

        st.markdown(
            "**SYSTEM INFORMATION**"
        )

        st.info(
            "Historical Dataset + "
            "Simulated Event Monitoring"
        )

        st.divider()

        st.markdown(
            "**DATA SOURCE**"
        )

        st.caption(
            "UNSW-NB15 Network Dataset"
        )

        st.divider()

        st.caption(
            "Big Data Analytics CBP"
        )

        st.caption(
            "Python • Streamlit • Plotly"
        )

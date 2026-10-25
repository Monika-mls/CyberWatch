
import io
from datetime import datetime

import pandas as pd
import streamlit as st
import plotly.express as px

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

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


# ==========================================
# PAGE DESIGN
# ==========================================

apply_custom_style()
show_sidebar_info()

page_header(
    title="Data Management & Reports",
    subtitle=(
        "Explore dataset quality, inspect records, "
        "and generate cybersecurity analytics reports."
    ),
    section="CYBERWATCH / DATA INTELLIGENCE"
)


# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data(show_spinner=False)
def get_management_data():

    raw_df = load_data()

    clean_df = preprocess_data(raw_df)

    analyzed_df, thresholds = detect_threats(
        clean_df
    )

    return (
        raw_df,
        clean_df,
        analyzed_df,
        thresholds
    )


try:
    with st.spinner("Loading cybersecurity dataset..."):

        raw_df, clean_df, analyzed_df, thresholds = (
            get_management_data()
        )

except Exception as error:
    st.error(f"Dataset loading failed: {error}")
    st.stop()


# ==========================================
# DATASET OVERVIEW
# ==========================================

st.subheader("📁 Dataset Overview")

total_records = len(raw_df)
total_columns = len(raw_df.columns)

missing_values = int(
    raw_df.isnull().sum().sum()
)

duplicate_records = int(
    raw_df.duplicated().sum()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Records",
    f"{total_records:,}"
)

col2.metric(
    "Total Columns",
    total_columns
)

col3.metric(
    "Missing Values",
    f"{missing_values:,}"
)

col4.metric(
    "Duplicate Records",
    f"{duplicate_records:,}"
)

st.divider()


# ==========================================
# DATA PREPROCESSING SUMMARY
# ==========================================

st.subheader("🧹 Data Preprocessing")

st.caption(
    "Compare the original dataset with "
    "the cleaned dataset."
)

summary = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Total Columns",
        "Missing Values",
        "Duplicate Records"
    ],

    "Before Cleaning": [
        len(raw_df),
        len(raw_df.columns),
        int(raw_df.isnull().sum().sum()),
        int(raw_df.duplicated().sum())
    ],

    "After Cleaning": [
        len(clean_df),
        len(clean_df.columns),
        int(clean_df.isnull().sum().sum()),
        int(clean_df.duplicated().sum())
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)

removed_records = len(raw_df) - len(clean_df)

st.info(
    f"Preprocessing removed {removed_records:,} "
    "duplicate records. Missing numerical values "
    "were handled using the existing preprocessing "
    "rules."
)

st.divider()


# ==========================================
# MISSING VALUE ANALYSIS
# ==========================================

st.subheader("🔎 Missing Value Analysis")

missing_df = (
    raw_df.isnull()
    .sum()
    .reset_index()
)

missing_df.columns = [
    "Column",
    "Missing Count"
]

missing_df = missing_df[
    missing_df["Missing Count"] > 0
]

if missing_df.empty:

    st.success(
        "No missing values detected "
        "in the original dataset."
    )

else:

    fig = px.bar(
        missing_df,
        x="Column",
        y="Missing Count",
        title="Missing Values by Column"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        missing_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ==========================================
# DATA TYPES AND STATISTICS
# ==========================================

st.subheader("📊 Data Exploration")

tab1, tab2, tab3 = st.tabs([
    "Dataset Preview",
    "Data Types",
    "Summary Statistics"
])

with tab1:

    st.dataframe(
        clean_df.head(250),
        use_container_width=True,
        hide_index=True
    )

with tab2:

    types_df = pd.DataFrame({
        "Column": clean_df.columns,
        "Data Type": clean_df.dtypes.astype(str)
    })

    st.dataframe(
        types_df,
        use_container_width=True,
        hide_index=True
    )

with tab3:

    numeric_df = clean_df.select_dtypes(
        include="number"
    )

    st.dataframe(
        numeric_df.describe().transpose(),
        use_container_width=True
    )


st.divider()


# ==========================================
# THREAT ANALYSIS SUMMARY
# ==========================================

st.subheader("🚨 Security Analysis Summary")

flagged_events = int(
    analyzed_df["suspicious"].sum()
)

high_risk = int(
    (
        analyzed_df["risk_level"] == "High"
    ).sum()
)

medium_risk = int(
    (
        analyzed_df["risk_level"] == "Medium"
    ).sum()
)

low_risk = int(
    (
        analyzed_df["risk_level"] == "Low"
    ).sum()
)

a, b, c, d = st.columns(4)

a.metric("Flagged Events", f"{flagged_events:,}")
b.metric("High Risk", f"{high_risk:,}")
c.metric("Medium Risk", f"{medium_risk:,}")
d.metric("Low Risk", f"{low_risk:,}")

st.caption(
    "These risk levels are produced by "
    "CyberWatch's statistical detection rules. "
    "They do not represent confirmed attack severity."
)

st.divider()


# ==========================================
# CSV EXPORT
# ==========================================

st.subheader("📥 Export Processed Data")

st.write(
    "Download a sample of the processed "
    "network traffic records for further analysis."
)

export_limit = st.selectbox(
    "Number of records to export",
    [1000, 5000, 10000, 25000, 50000],
    index=2
)

export_df = analyzed_df.head(export_limit)

st.download_button(
    label="⬇️ Download Processed CSV",
    data=export_df.to_csv(index=False),
    file_name="cyberwatch_processed_data.csv",
    mime="text/csv"
)

st.caption(
    f"Export contains {len(export_df):,} records. "
    "The dataset stored in the application "
    "remains unchanged."
)

st.divider()


# ==========================================
# PDF REPORT GENERATION
# ==========================================

def generate_pdf_report():

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "CyberWatch Security Analytics Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 14))

    generated_at = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    elements.append(
        Paragraph(
            f"Generated on: {generated_at}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "1. Dataset Overview",
            styles["Heading2"]
        )
    )

    dataset_data = [
        ["Metric", "Value"],
        ["Total Records", f"{total_records:,}"],
        ["Total Columns", str(total_columns)],
        ["Missing Values", f"{missing_values:,}"],
        ["Duplicate Records", f"{duplicate_records:,}"],
        ["Cleaned Records", f"{len(clean_df):,}"]
    ]

    dataset_table = Table(
        dataset_data,
        colWidths=[240, 180]
    )

    dataset_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102840")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#EEF4F8")
        ]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 9)
    ]))

    elements.append(dataset_table)
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "2. Threat Detection Summary",
            styles["Heading2"]
        )
    )

    threat_data = [
        ["Risk Category", "Count"],
        ["Flagged Events", f"{flagged_events:,}"],
        ["High Risk", f"{high_risk:,}"],
        ["Medium Risk", f"{medium_risk:,}"],
        ["Low Risk", f"{low_risk:,}"]
    ]

    threat_table = Table(
        threat_data,
        colWidths=[240, 180]
    )

    threat_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102840")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#EEF4F8")
        ]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 9)
    ]))

    elements.append(threat_table)
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "3. Statistical Detection Thresholds",
            styles["Heading2"]
        )
    )

    threshold_data = [
        ["Feature", "Threshold"]
    ]

    for feature, value in thresholds.items():
        threshold_data.append([
            str(feature),
            f"{value:,.4f}"
        ])

    threshold_table = Table(
        threshold_data,
        colWidths=[240, 180]
    )

    threshold_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102840")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 9)
    ]))

    elements.append(threshold_table)
    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "4. Analysis Notes",
            styles["Heading2"]
        )
    )

    elements.append(
        Paragraph(
            "CyberWatch performs statistical analysis "
            "on the UNSW-NB15 training dataset. "
            "It flags unusual traffic using percentile-based "
            "thresholds for source bytes, connection duration, "
            "and traffic rate. "
            "These alerts indicate anomalies rather than "
            "verified security incidents.",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 15))

    elements.append(
        Paragraph(
            "Dataset: UNSW-NB15 | "
            "Monitoring Mode: Historical Data Analysis",
            styles["Normal"]
        )
    )

    doc.build(elements)

    buffer.seek(0)

    return buffer.getvalue()


# ==========================================
# REPORT DOWNLOAD
# ==========================================

st.subheader("📄 Generate Security Report")

st.write(
    "Generate a PDF containing the dataset "
    "overview, data quality information, "
    "threat detection summary, and thresholds."
)

if st.button("Generate PDF Report"):

    with st.spinner("Preparing security report..."):

        pdf_bytes = generate_pdf_report()

        st.session_state["cw_pdf_report"] = pdf_bytes

if "cw_pdf_report" in st.session_state:

    st.download_button(
        label="⬇️ Download PDF Report",
        data=st.session_state["cw_pdf_report"],
        file_name="CyberWatch_Security_Report.pdf",
        mime="application/pdf"
    )

    st.success("PDF report generated successfully!")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "CyberWatch | Data Management and "
    "Security Analytics Reporting"
)

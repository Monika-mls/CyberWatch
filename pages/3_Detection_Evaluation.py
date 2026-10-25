
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from modules.evaluation import (
    evaluate_detection,
    evaluate_decision_tree
)

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
    title="Detection Performance Evaluation",
    subtitle=(
        "Measure rule-based threat detection "
        "performance on unseen testing records."
    ),
    section="CYBERWATCH / ANALYTICS EVALUATION"
)


# ==========================================
# LOAD EVALUATION RESULTS
# ==========================================

@st.cache_data(show_spinner=False)
def get_results():
    return evaluate_detection()


try:
    with st.spinner(
        "Evaluating cybersecurity detection rules..."
    ):
        df, metrics, matrix, report, thresholds = (
            get_results()
        )

except FileNotFoundError as error:
    st.error(str(error))
    st.info(
        "Download UNSW_NB15_testing-set.csv "
        "and place it inside data/raw/."
    )
    st.stop()

except Exception as error:
    st.error(f"Evaluation failed: {error}")
    st.stop()


# ==========================================
# PERFORMANCE METRICS
# ==========================================

st.subheader("📊 Detection Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Accuracy",
    f"{metrics['accuracy'] * 100:.2f}%"
)

col2.metric(
    "Precision",
    f"{metrics['precision'] * 100:.2f}%"
)

col3.metric(
    "Recall",
    f"{metrics['recall'] * 100:.2f}%"
)

col4.metric(
    "F1-Score",
    f"{metrics['f1'] * 100:.2f}%"
)

st.caption(
    "Evaluation uses the separate UNSW-NB15 "
    "testing partition and fixed thresholds "
    "calculated from training data."
)

st.divider()


# ==========================================
# CONFUSION MATRIX
# ==========================================

st.subheader("🔍 Confusion Matrix")

left, right = st.columns([3, 2])

with left:

    fig = go.Figure(
        data=go.Heatmap(
            z=matrix,
            x=[
                "Predicted Normal",
                "Predicted Attack"
            ],
            y=[
                "Actual Normal",
                "Actual Attack"
            ],
            colorscale="Blues",
            showscale=True,
            text=matrix,
            texttemplate="%{text}",
            textfont={"size": 18}
        )
    )

    fig.update_layout(
        title="Rule-Based Detection Results",
        xaxis_title="Predicted Class",
        yaxis_title="Actual Class",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with right:

    tn, fp, fn, tp = matrix.ravel()

    st.metric("True Positives", f"{tp:,}")
    st.metric("True Negatives", f"{tn:,}")
    st.metric("False Positives", f"{fp:,}")
    st.metric("False Negatives", f"{fn:,}")


st.divider()


# ==========================================
# CLASSIFICATION REPORT
# ==========================================

st.subheader("📋 Classification Report")

report_df = pd.DataFrame(report).transpose()

st.dataframe(
    report_df,
    use_container_width=True
)


# ==========================================
# THRESHOLDS
# ==========================================

with st.expander("View Training-Based Thresholds"):

    st.write(
        "These thresholds were calculated "
        "from normal-labeled training records "
        "using the 99th percentile."
    )

    threshold_df = pd.DataFrame(
        [
            {
                "Feature": feature,
                "Threshold": value
            }
            for feature, value in thresholds.items()
        ]
    )

    st.dataframe(
        threshold_df,
        use_container_width=True
    )


# ==========================================
# EXPORT RESULTS
# ==========================================

st.divider()

st.subheader("📥 Export Evaluation Results")

export_columns = [
    "label",
    "predicted_label",
    "risk_score",
    "sbytes",
    "dur",
    "rate"
]

export_df = df[export_columns]

st.download_button(
    label="Download Test Predictions",
    data=export_df.to_csv(index=False),
    file_name="cyberwatch_evaluation.csv",
    mime="text/csv"
)

st.success(
    "Independent test evaluation completed."
)


st.divider()

st.subheader("Statistical Rules vs Decision Tree")

st.write(
    "Compare our statistical threshold-based "
    "detector with a supervised Decision Tree "
    "trained on network traffic features."
)

@st.cache_data(show_spinner=False)
def get_tree_results():
    return evaluate_decision_tree()


if st.button("Compare Detection Methods"):

    with st.spinner("Training and evaluating Decision Tree..."):

        tree_metrics, tree_matrix = get_tree_results()
        
        # ==========================================
        # DECISION TREE CONFUSION MATRIX
        # ==========================================

        st.divider()

        st.subheader("Decision Tree Confusion Matrix")

        st.write(
            "This matrix shows how many normal and "
            "attack records were correctly or "
            "incorrectly classified by the Decision Tree."
        )

        import plotly.graph_objects as go

        fig_matrix = go.Figure(
            data=go.Heatmap(
                z=tree_matrix,
                x=["Predicted Normal", "Predicted Attack"],
                y=["Actual Normal", "Actual Attack"],
                colorscale="Blues",
                text=tree_matrix,
                texttemplate="%{text}",
                textfont=dict(size=20),
                showscale=True
            )
        )

        fig_matrix.update_layout(
            title="Decision Tree Classification Results",
            xaxis_title="Predicted Class",
            yaxis_title="Actual Class",
            height=450,
            template="plotly_dark"
        )

        st.plotly_chart(
            fig_matrix,
            use_container_width=True
        )

        tn, fp, fn, tp = tree_matrix.ravel()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("True Positives", f"{tp:,}")
        c2.metric("True Negatives", f"{tn:,}")
        c3.metric("False Positives", f"{fp:,}")
        c4.metric("False Negatives", f"{fn:,}")

        st.info(
            "True Positives represent correctly detected "
            "attacks. False Negatives represent actual "
            "attacks that the model failed to detect."
        )

    comparison = pd.DataFrame({
        "Metric": [
            "Accuracy",
            "Precision",
            "Recall",
            "F1-Score"
        ],
        "Statistical Rules": [
            metrics["accuracy"],
            metrics["precision"],
            metrics["recall"],
            metrics["f1"]
        ],
        "Decision Tree": [
            tree_metrics["accuracy"],
            tree_metrics["precision"],
            tree_metrics["recall"],
            tree_metrics["f1"]
        ]
    })

    st.dataframe(
        comparison.style.format({
            "Statistical Rules": "{:.2%}",
            "Decision Tree": "{:.2%}"
        }),
        use_container_width=True,
        hide_index=True
    )

    comparison_plot = comparison.melt(
        id_vars="Metric",
        var_name="Method",
        value_name="Score"
    )

    import plotly.express as px

    fig = px.bar(
        comparison_plot,
        x="Metric",
        y="Score",
        color="Method",
        barmode="group",
        title="Detection Method Comparison"
    )

    fig.update_yaxes(
        tickformat=".0%",
        range=[0, 1]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Both approaches are evaluated on the "
        "separate UNSW-NB15 testing partition."
    )

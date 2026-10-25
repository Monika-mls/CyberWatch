
import streamlit as st
import plotly.express as px

from modules.preprocessing import load_data
from modules.performance import benchmark_processing
from modules.ui_components import (
    apply_custom_style,
    page_header,
    show_sidebar_info
)

apply_custom_style()
show_sidebar_info()

page_header(
    "Data Processing Performance",
    "Measure analytics processing time "
    "across different dataset sizes.",
    "CYBERWATCH / BIG DATA PERFORMANCE"
)

st.subheader("Processing Scalability Analysis")

st.write(
    "This experiment evaluates the execution "
    "time of basic data cleaning and aggregation "
    "operations across increasing record counts."
)

if st.button("Run Performance Benchmark"):

    df = load_data()

    with st.spinner("Running benchmark..."):
        results = benchmark_processing(df)

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )

    fig = px.line(
        results,
        x="Records",
        y="Processing Time (seconds)",
        markers=True,
        title="Processing Time vs Dataset Size"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "Results represent local Pandas execution "
        "times and may vary between runs."
    )

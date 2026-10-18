import streamlit as st
import pandas as pd

st.set_page_config(page_title="Nassau Candy Factory Optimizer", layout="wide")
st.title("Nassau Candy Factory Optimization Simulator")

sim = pd.read_csv("data/processed/simulation_table.csv", index_col=0)
rec = pd.read_csv("data/processed/recommendations.csv")

product = st.selectbox("Select a product", sim.index)

st.subheader("Predicted lead time by factory (days)")
import altair as alt

plot_df = sim.loc[product].reset_index()
plot_df.columns = ["Factory", "Lead Time"]
lo = plot_df["Lead Time"].min() - 0.05
hi = plot_df["Lead Time"].max() + 0.05

chart = alt.Chart(plot_df).mark_bar(clip=True).encode(
    x=alt.X("Factory", sort="y", title=None),
    y=alt.Y("Lead Time", scale=alt.Scale(domain=[lo, hi]), title="Predicted days"),
    tooltip=["Factory", "Lead Time"],
)
st.altair_chart(chart, use_container_width=True)
st.caption("The axis is zoomed in to show small differences. Factory gaps are usually under 0.1 days.")

row = rec[rec["Product"] == product].iloc[0]
c1, c2, c3 = st.columns(3)
c1.metric("Current factory", row["Current Factory"])
c2.metric("Best factory", row["Best Factory"])
c3.metric("Lead time reduction", f"{row['Reduction %']:.2f}%")
st.info(f"Verdict: {row['Verdict']}")
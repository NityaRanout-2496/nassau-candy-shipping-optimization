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
st.divider()
st.header("Recommendation Dashboard")
st.caption("All products ranked by predicted lead time reduction, with a risk verdict for each.")

show = rec[["Product", "Current Factory", "Best Factory", "Reduction %",
            "Distance Change %", "Orders", "Verdict"]]
st.dataframe(show, use_container_width=True, hide_index=True)
st.divider()
st.header("Risk & Impact Panel")

counts = rec["Verdict"].value_counts()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Recommend", int(counts.get("Recommend", 0)))
c2.metric("High risk", int(counts.get("High risk: farther distance", 0)))
c3.metric("Low confidence", int(counts.get("Low confidence: few orders", 0)))
c4.metric("Keep current", int(counts.get("Keep current", 0)))

for _, r in rec[rec["Verdict"].str.startswith("High risk")].iterrows():
    st.warning(
        f"{r['Product']}: moving to {r['Best Factory']} would increase shipping distance by "
        f"{r['Distance Change %']:.0f}% for only a {r['Reduction %']:.2f}% lead time gain."
    )
st.divider()
st.header("What-If Scenario Analysis")

wi_product = st.selectbox("Product to test", sim.index, key="wi_product")
wi_current = rec.loc[rec["Product"] == wi_product, "Current Factory"].iloc[0]
wi_options = [f for f in sim.columns if f != wi_current]
wi_factory = st.selectbox("Move it to", wi_options, key="wi_factory")

cur_val = sim.loc[wi_product, wi_current]
new_val = sim.loc[wi_product, wi_factory]
change = new_val - cur_val

c1, c2, c3 = st.columns(3)
c1.metric(f"Current ({wi_current})", f"{cur_val:.2f} days")
c2.metric(f"If moved to {wi_factory}", f"{new_val:.2f} days",
          delta=f"{change:+.2f} days", delta_color="inverse")
c3.metric("Change", f"{change / cur_val * 100:+.2f}%")    
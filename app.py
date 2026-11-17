import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Olist E-commerce Analysis", layout="wide")
st.title("Olist E-commerce: SQL Analysis Dashboard")

@st.cache_data
def q(file):
    conn = sqlite3.connect("olist.db")
    return pd.read_sql(open(f"sql/{file}", encoding="utf-8-sig").read(), conn)

rev = q("01_monthly_revenue.sql")
cat = q("02_top_categories.sql")
dlv = q("03_delivery_vs_review.sql")
rep = q("04_repeat_customers.sql")
coh = q("05_cohorts.sql")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Customers", f"{int(rep.customers[0]):,}")
c2.metric("Repeat rate", f"{rep.repeat_rate_pct[0]}%")
late = dlv.loc[dlv.delivery_status == "late", "avg_review"].iloc[0]
ontime = dlv.loc[dlv.delivery_status == "on_time", "avg_review"].iloc[0]
c3.metric("Review (on time)", ontime)
c4.metric("Review (late)", late, delta=round(late - ontime, 2))

st.subheader("Monthly revenue")
rev = rev[rev.month >= "2017-01"]
st.plotly_chart(px.line(rev, x="month", y="revenue", markers=True), use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Top categories by revenue")
    st.plotly_chart(px.bar(cat, x="revenue", y="category", orientation="h")
                    .update_yaxes(autorange="reversed"), use_container_width=True)
with right:
    st.subheader("Late delivery vs review score")
    st.plotly_chart(px.bar(dlv, x="delivery_status", y="avg_review", text="avg_review"),
                    use_container_width=True)

st.subheader("Cohort retention (% of cohort active)")
coh["cohort_idx"] = pd.to_datetime(coh.cohort_month + "-01")
coh["active_idx"] = pd.to_datetime(coh.active_month + "-01")
coh["month_n"] = (coh.active_idx.dt.year - coh.cohort_idx.dt.year) * 12 + (coh.active_idx.dt.month - coh.cohort_idx.dt.month)
piv = coh.pivot_table(index="cohort_month", columns="month_n", values="customers")
ret = (piv.div(piv[0], axis=0) * 100).round(2)
ret = ret[(ret.index >= "2017-01") & (ret.index <= "2018-03")].iloc[:, :12]
st.plotly_chart(px.imshow(ret, text_auto=True, aspect="auto",
                          labels=dict(x="Months since first order", y="Cohort", color="%")),
                use_container_width=True)

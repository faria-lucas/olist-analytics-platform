import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd

# Page configuration
st.set_page_config(page_title="Olist Analytics Dashboard", layout="wide")

# Function to connect to the database
def get_data(query):
    with duckdb.connect('./data/olist.duckdb', read_only=True) as con:
        return con.execute(query).df()

st.title("Olist Business Intelligence")
st.markdown("Sales and logistics performance analysis based on the dbt Marts layer.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
states = get_data("SELECT DISTINCT state FROM dim_customers ORDER BY 1")
selected_state = st.sidebar.multiselect("Select States", states['state'].unique())

# --- DATA LOADING ---
query_base = """
    SELECT 
        f.*, 
        c.state,
        c.city_upper
    FROM fct_orders f
    LEFT JOIN dim_customers c ON f.customer_id = c.customer_id
    WHERE 1=1
"""

if selected_state:
    query_base += f" AND c.state IN {tuple(selected_state) if len(selected_state) > 1 else f'({repr(selected_state[0])})'}"

df_orders = get_data(query_base)

# --- KEY METRICS (KPIs) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_revenue = df_orders['total_order_amount'].sum()
    st.metric("Total Revenue", f"R$ {total_revenue:,.2f}")

with col2:
    total_orders = df_orders['order_id'].nunique()
    st.metric("Total Orders", f"{total_orders:,}")

with col3:
    avg_ticket = total_revenue / total_orders if total_orders > 0 else 0
    st.metric("Average Ticket", f"R$ {avg_ticket:,.2f}")

with col4:
    avg_delivery = df_orders['actual_delivery_days'].mean()
    st.metric("Average Delivery Time", f"{avg_delivery:.1f} dias")

# --- CHARTS ---
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("Sales by State")
    sales_by_state = df_orders.groupby('state')['total_order_amount'].sum().reset_index().sort_values('total_order_amount', ascending=False)
    fig_state = px.bar(sales_by_state, x='state', y='total_order_amount', color='total_order_amount', template="plotly_dark")
    st.plotly_chart(fig_state, width="stretch")

with c2:
    st.subheader("Status Distribution")
    status_counts = df_orders['order_status'].value_counts().reset_index()
    fig_status = px.pie(status_counts, names='order_status', values='count', hole=0.4, template="plotly_dark")
    st.plotly_chart(fig_status, width="stretch")

st.divider()
st.subheader("Sample of Transformed Data (Marts)")
st.dataframe(df_orders.head(100), width="stretch")
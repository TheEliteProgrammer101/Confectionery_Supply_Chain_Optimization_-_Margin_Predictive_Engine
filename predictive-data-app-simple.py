import streamlit as st
import pandas as pd
import numpy as np

# 1. Page Canvas Framing & Aesthetic Theme
st.set_page_config(page_title="Candy Control Tower", layout="wide", page_icon="🍬")
st.title("🍬 Candy Control Tower: Comprehensive Enterprise Engine")
st.write("Complete executive operational workspace mapping multi-category target attainment, logistics velocity, and margins.")
st.markdown("---")

# 2. Automated Relational Data Engineering Pipeline
@st.cache_data
def pipeline_load_data():
    try:
        # Load raw files with matching local filenames
        sales = pd.read_csv("Candy_Sales.csv")
        products = pd.read_csv("Candy_Products.csv")
        factories = pd.read_csv("Candy_Factories.csv")
        targets = pd.read_csv("Candy_Targets.csv") 
        
        # Eliminate whitespace bugs globally from columns
        sales.columns = sales.columns.str.strip()
        products.columns = products.columns.str.strip()
        factories.columns = factories.columns.str.strip()
        targets.columns = targets.columns.str.strip()
        
        # STABILIZATION FIX: Force lowercase mappings to guarantee robust relational merges
        products_clean = products.copy()
        if "Product ID" in products_clean.columns:
            products_clean["product id"] = products_clean["Product ID"]
        if "Division" in products_clean.columns:
            products_clean["division"] = products_clean["Division"]
            
        sales_clean = sales.copy()
        if "Product ID" in sales_clean.columns:
            sales_clean["product id"] = sales_clean["Product ID"]
            
        targets_clean = targets.copy()
        if "Division" in targets_clean.columns:
            targets_clean["division"] = targets_clean["Division"]

        # Execute structural table merges mimicking Power BI Model View keys
        master = pd.merge(sales_clean, products_clean, on="product id", how="left", suffixes=('', '_prod'))
        master = pd.merge(master, factories, on="Factory", how="left")
        
        # Convert objects to structural datetime types for timeline math
        master['Order Date'] = pd.to_datetime(master['Order Date'], errors='coerce')
        master['Ship Date'] = pd.to_datetime(master['Ship Date'], errors='coerce')
        master = master.dropna(subset=['Order Date', 'Ship Date'])
        
        # Conditional Calendar Timeline Repair Workflow
        order_years = master['Order Date'].dt.year
        order_months = master['Order Date'].dt.month
        ship_months = master['Ship Date'].dt.month
        ship_days = master['Ship Date'].dt.day
        
        corrected_years = np.where(order_months > ship_months, order_years + 1, order_years)
        
        corrected_dates = []
        for yr, mo, dy in zip(corrected_years, ship_months, ship_days):
            try:
                corrected_dates.append(pd.Timestamp(year=yr, month=mo, day=dy))
            except ValueError:
                if mo == 2 and dy == 29:
                    corrected_dates.append(pd.Timestamp(year=yr, month=2, day=28))
                else:
                    corrected_dates.append(pd.NaT)
                    
        master['Corrected_Ship_Date'] = corrected_dates
        master['Fulfillment_Days'] = (master['Corrected_Ship_Date'] - master['Order Date']).dt.days
        master['Profit_Margin_%'] = (master['Gross Profit'] / master['Sales']) * 100
        
        return master, targets_clean, products_clean
    except FileNotFoundError:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df, df_targets, df_products = pipeline_load_data()

if df.empty or df_targets.empty:
    st.warning("⚠️ Data systems offline. Place your CSV data files inside your project working directory.")
else:
    # 3. Dynamic Column Keys Initialization
    prod_col = "Product Name" if "Product Name" in df.columns else "Product ID"

    # 4. Global Interactive Sidebar Filter Slicers Panel
    st.sidebar.header("🕹️ Global Filter Controls")
    st.sidebar.write("*Select options or click 'X' to filter rows.*")
    
    # Slicer 1: Division Multiselect
    all_divisions = sorted(df_products["division"].dropna().unique().tolist())
    selected_divisions = st.sidebar.multiselect("Filter by Product Divisions:", options=all_divisions, default=all_divisions)
    
    # Slicer 2: Product Name/Line Multiselect
    all_products = sorted(df[prod_col].dropna().unique().tolist())
    selected_products = st.sidebar.multiselect("Filter by Specific Products:", options=all_products, default=all_products)
    
    # Slicer 3: Manufacturing Factory Multiselect
    all_factories = sorted(df["Factory"].dropna().unique().tolist())
    selected_factories = st.sidebar.multiselect("Filter by Production Factories:", options=all_factories, default=all_factories)
    
    # Slicer 4: Shipping Freight Mode Multiselect
    all_modes = sorted(df["Ship Mode"].dropna().unique().tolist())
    selected_modes = st.sidebar.multiselect("Filter by Shipping Freight Modes:", options=all_modes, default=all_modes)
    
    # Slicer 5: Customer State/Province Location Multiselect
    all_states = sorted(df["State/Province"].dropna().unique().tolist())
    selected_states = st.sidebar.multiselect("Filter by Destination States:", options=all_states, default=all_states)

    # 5. Core Dynamic Filtration Engine (Pandas Masking Array)
    filtered_df = df[
        (df["division"].isin(selected_divisions)) &
        (df[prod_col].isin(selected_products)) &
        (df["Factory"].isin(selected_factories)) &
        (df["Ship Mode"].isin(selected_modes)) &
        (df["State/Province"].isin(selected_states))
    ]
    
    filtered_targets = df_targets[df_targets["division"].isin(selected_divisions)]

    # 6. High-Density Executive KPI Scorecards Matrix (Arranged in a single neat row)
    if not filtered_df.empty:
        total_sales_val = filtered_df['Sales'].sum()
        total_profit_val = filtered_df['Gross Profit'].sum()
        avg_margin_val = filtered_df['Profit_Margin_%'].mean()
        avg_lead_val = filtered_df['Fulfillment_Days'].mean()
        
        total_target_val = filtered_targets['Target'].sum() if not filtered_targets.empty else 1
        attainment_pct = (total_sales_val / total_target_val) * 100
        attainment_delta = attainment_pct - 100

        # Building a 5-column layout matrix grid at the top
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
        with kpi1:
            st.metric(label="Total Earned Revenue", value=f"${total_sales_val:,.2f}")
        with kpi2:
            st.metric(label="Net Sourcing Profit", value=f"${total_profit_val:,.2f}")
        with kpi3:
            st.metric(label="Avg Cohort Margin", value=f"{avg_margin_val:.1f}%")
        with kpi4:
            st.metric(
                label="Target Attainment %", 
                value=f"{attainment_pct:.1f}%",
                delta=f"{attainment_delta:+.1f}% vs Goal"
            )
        with kpi5:
            st.metric(label="Avg Delivery Lead-Time", value=f"{avg_lead_val:.1f} Days")
            
        st.markdown("---")

        # 7. Dual Comparison Visualizations Section
        col_chart_left, col_chart_right = st.columns(2)
        
        with col_chart_left:
            st.subheader("🎯 Division Comparison: Actual Sales vs. Targets")
            st.write("*Are our candy divisions successfully hitting corporate goals?*")
            
            # Aggregate actual sales and targets dynamically
            sales_agg = filtered_df.groupby("Division")["Sales"].sum().reset_index() if "Division" in filtered_df.columns else filtered_df.groupby("division")["Sales"].sum().reset_index()
            sales_agg.columns = ["Division", "Sales"]
            
            target_agg = filtered_targets.groupby("Division")["Target"].sum().reset_index() if "Division" in filtered_targets.columns else filtered_targets.groupby("division")["Target"].sum().reset_index()
            target_agg.columns = ["Division", "Target"]
            
            comparison_df = pd.merge(sales_agg, target_agg, on="Division", how="outer").fillna(0)
            
            # Melt the structure to display side-by-side clustered columns natively
            chart_melted = comparison_df.melt(id_vars="Division", value_vars=["Sales", "Target"], 
                                             var_name="Metric", value_name="Amount")
            
            st.bar_chart(data=chart_melted, x="Division", y="Amount", color="Metric", use_container_width=True)
            
        with col_chart_right:
            st.subheader("🚚 Freight Fulfillment Velocity Matrix")
            st.write("*Which shipping mode presents the highest delivery lead times?*")
            shipping_chart_data = filtered_df.groupby("Ship Mode")["Fulfillment_Days"].mean().reset_index()
            st.bar_chart(data=shipping_chart_data, x="Ship Mode", y="Fulfillment_Days", use_container_width=True)

        st.markdown("---")

        # 8. Multi-Customer Live Transaction Ledger Grid
        st.subheader("📋 Filtered Carrier Transaction Manifest")
        st.write("Click on any column header below to sort active rows instantly.")
        
        ledger_display_df = filtered_df[["Order ID", "Customer ID", "State/Province", "Factory", "Ship Mode", prod_col, "Units", "Sales", "Fulfillment_Days"]]
        st.dataframe(ledger_display_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ No records found matching the active slicer bounds. Please add more filter criteria categories.")

    # 9. DATA SCIENCE INTEGRATION: Machine Learning Predictive Model
st.markdown("---")
st.subheader("🔮 Data Science Module: Predictive Gross Profit Estimator")
st.write("This module runs a live Linear Regression Machine Learning model trained on your active sales rows.")

from sklearn.linear_model import LinearRegression

# Ensure we have data to train on
if not filtered_df.empty and len(filtered_df) > 10:
    # Step 1: Isolate our Features (X) and Target variable (y)
    X = filtered_df[['Units', 'Fulfillment_Days']].fillna(0)
    y = filtered_df['Gross Profit'].fillna(0)
    
    # Step 2: Initialize and Train (Fit) the Machine Learning Model
    ml_model = LinearRegression()
    ml_model.fit(X, y)
    
    # Step 3: Create Interactive Sliders for User Inputs in the Browser
    st.write("🤖 **Simulate a New Incoming Shipment Order Below:**")
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        sim_units = st.slider("Simulated Order Units Quantity:", min_value=1, max_value=200, value=25)
    with input_col2:
        sim_days = st.slider("Simulated Route Delivery Days:", min_value=1, max_value=30, value=5)
        
    # Step 4: Run the inputs through the trained model to get a live prediction
    user_features = np.array([[sim_units, sim_days]])
    predicted_profit = ml_model.predict(user_features)[0]
    
    # Step 5: Render the output scorecard
    st.metric(label="📊 Model Predicted Gross Profit Return ($)", value=f"${predicted_profit:,.2f}")
else:
    st.info("Please expand your filter selections to load enough row data for training the ML model pipeline.")

### 🛢️ Phase 1: Database Extraction & Timeline Repair (SQL)
To ensure the pipeline sat on bulletproof data, I wrote a comprehensive SQL optimization script using **Common Table Expressions (CTEs)** to fix a major built-in date corruption anomaly where shipping dates were erroneously logged 5 years into the future. 
* **The Logic:** Built conditional `CASE WHEN` date parameters to dynamically realign the timeline back into valid single-digit transit indices (e.g., 2.4 days vs 2,005 days).
* **The Code:** Saved under `candy_database_queries.sql`.

### 📊 Phase 2: Strategic Dashboard Interface (Power BI)
Designed a high-density, dark-themed **2-Page Executive Analytics Suite** connected directly via an optimized relational **Master Calendar Table** model view to prevent data mismatches.

#### Page 1: Executive Financial Summary Hub
* Captures high-level financial health across 4 key metrics: **\$142K Total Revenue**, **\$93K Total Profit**, a strong **65.9% Avg Profit Margin**, and a **315.1% Target Attainment**.
* Includes a dynamic **Top 5 Revenue-Generating Customers** leaderboard and volume tracking visuals to cross-examine customer spend velocity across geographical regions.

Link to your local image asset:
![Executive Financial Dashboard](images/page1_financials.png)

#### Page 2: Supply Chain & Logistics Diagnostics
* Implements an interactive **Route Performance Heatmap** matrix table plotting *Factory* vs. *State/Province*.
* Uses conditional cell formatting to highlight logistics failures in bright red, immediately exposing that routes out of *Secret Factory* and *Wicked Choccy's* are violating delivery targets.

Link to your local image asset:
![Supply Chain Diagnostics Matrix](images/page2_logistics.png)

### 🐍 Phase 3: Operational Freight Dispatch App (Python & Streamlit)
While Power BI looks backward at historical executive trends, I coded a **Predictive Control Tower App** inside Python for ground-level warehouse operators to use at the loading dock.
* **Multi-Category Slicers:** Replicated Power BI slicers using native `st.multiselect` components for responsive cross-filtering across Division, Product, and Factory.
* **Machine Learning Pipeline:** Integrated a live **Scikit-Learn Linear Regression model** trained on the data rows to instantly estimate the projected Gross Profit return of a simulated shipment based on custom units and transit thresholds.

Link to your local image asset:
![Streamlit Machine Learning Data Product](images/data_app_ml.png)

---

## 🧠 Core Business Discoveries & Consulting Actions

### 1. The "Kazookles" Margin Collapse
* **The Data Insight:** While **Everlasting Gobstoppers** led structural profitability at an incredible **80.0% gross margin** and **Hair Toffee** sat at **78.0%**, the **Kazookles** segment dropped to an unprofitable **8.4% margin profile**.
* **Prescriptive Recommendation:** Discontinue the Kazookles product line entirely or immediately renegotiate raw ingredient contract agreements to protect company financial health.

### 2. Geopolitical Sourcing Mismatch
* **The Data Insight:** The logistics matrix revealed that `The Other Factory` experienced its worst shipping delays when fulfilling orders to California compared to North Carolina.
* **Prescriptive Recommendation:** Enforce a strict **300-mile regional fulfillment cap**. Strip West Coast volume away from remote, struggling facilities and reassign those high-value contracts to closer production hubs to eliminate transit overhead.

---

## 🛠️ Complete Technical Tool Stack
* **Sourcing & Architecture:** SQL (PostgreSQL), CTEs, Window Functions (`DENSE_RANK`).
* **Business Intelligence:** Power BI Desktop, DAX Modeling, Conditional Matrix Formatting.
* **Data Product Software:** Python 3.13, Pandas Dataframe Merges, Streamlit UI, Numpy.
* **Advanced Analytics:** Scikit-Learn (Linear Regression Modeling).
* **Workflow Automation:** Git, Version Control, Streamlit Community Cloud Hosting.

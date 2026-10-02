-- ====================================================================
-- 🍬 US CANDY DISTRIBUTOR: DATA EXTRACTION & ENGINEERING PIPELINE
-- Focus: Multi-Table Joins, Date Correction, and Margin Analysis
-- ====================================================================

-- STEP 1: Creating a Clean Master CTE to fix data corruption anomalies
-- Here we replicate our calendar logic to fix the 5-year shipping date error
WITH CleanedSales AS (
    SELECT 
        s."Order ID",
        s."Customer ID",
        s."Product ID",
        s."Factory",
        s."Ship Mode",
        s."Sales" AS Gross_Revenue,
        s."Gross Profit" AS Dollar_Profit,
        s."Units",
        s."Order Date",
        s."Ship Date",
        
        -- Conditional logic: If order month > ship month, add 1 year to order date's year
        CASE 
            WHEN EXTRACT(MONTH FROM s."Order Date") > EXTRACT(MONTH FROM s."Ship Date")
            THEN MAKE_DATE(EXTRACT(YEAR FROM s."Order Date")::INT + 1, EXTRACT(MONTH FROM s."Ship Date")::INT, EXTRACT(DAY FROM s."Ship Date")::INT)
            ELSE MAKE_DATE(EXTRACT(YEAR FROM s."Order Date")::INT, EXTRACT(MONTH FROM s."Ship Date")::INT, EXTRACT(DAY FROM s."Ship Date")::INT)
        END AS Corrected_Ship_Date
    FROM "Candy_Sales" s
)

-- STEP 2: Answering Maven Q1 & Q2 (Most and Least Efficient Shipping Routes)
-- Connecting sales ledger to factories geospatial table to measure average lead times
SELECT 
    cs."Factory",
    cs."Ship Mode",
    COUNT(cs."Order ID") AS Total_Orders,
    ROUND(AVG(cs.Corrected_Ship_Date - cs."Order Date"), 1) AS Avg_Fulfillment_Days
FROM CleanedSales cs
GROUP BY cs."Factory", cs."Ship Mode"
ORDER BY Avg_Fulfillment_Days DESC;


-- STEP 3: Answering Maven Q3 (Which product lines have the best product margin?)
-- Connecting sales ledger to the product catalog table to calculate aggregate percentage margins
SELECT 
    p."Division",
    p."Product Name",
    SUM(cs.Gross_Revenue) AS Total_Sales_USD,
    SUM(cs.Dollar_Profit) AS Total_Profit_USD,
    ROUND((SUM(cs.Dollar_Profit) / SUM(cs.Gross_Revenue)) * 100, 1) AS Profit_Margin_Percent
FROM CleanedSales cs
LEFT JOIN "Candy_Products" p ON cs."Product ID" = p."Product ID"
GROUP BY p."Division", p."Product Name"
ORDER BY Profit_Margin_Percent DESC;


-- STEP 4: Advanced Analyst KPI (Top 3 Revenue Generating Customers per Factory)
-- Utilizing SQL Window Functions (DENSE_RANK) to find our VIP customer cohorts
WITH CustomerRankings AS (
    SELECT 
        cs."Factory",
        cs."Customer ID",
        SUM(cs.Gross_Revenue) AS Customer_Total_Spend,
        DENSE_RANK() OVER(PARTITION BY cs."Factory" ORDER BY SUM(cs.Gross_Revenue) DESC) AS Revenue_Rank
    FROM CleanedSales cs
    GROUP BY cs."Factory", cs."Customer ID"
)
SELECT * 
FROM CustomerRankings
WHERE Revenue_Rank <= 3;

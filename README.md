# Cart2Insights — Olist E-Commerce Analytics

## Project Overview

Cart2Insights is an e-commerce data analytics project based on the Olist Brazilian marketplace dataset.

The project converts raw e-commerce data into useful business insights by performing data cleaning, SQL analysis, feature engineering, exploratory data analysis, and dashboard development.

## Project Objective

The main objective is to understand:

* Sales performance
* Customer behavior
* Seller and product performance
* Delivery performance
* Payment preferences
* Customer satisfaction

## Project Workflow

### Step 1: Understand the Data

Load the raw CSV files and examine their structure, columns, rows, and data types.

### Step 2: Check Data Quality

Identify missing values, duplicate records, incorrect data types, and unusual values.

### Step 3: Clean the Data

Clean the datasets by handling missing values, removing duplicates, fixing date columns, and standardizing text data.

### Step 4: Load Data into MySQL

Store the cleaned datasets in a MySQL database and establish relationships between the tables.

### Step 5: Feature Engineering

Create useful business metrics such as:

* Total Order Value
* Delivery Days
* Delivery Delay
* Customer Spending
* Average Order Value
* Seller Revenue
* Repeat Customer Indicator

### Step 6: Exploratory Data Analysis

Analyze the data using visualizations to identify trends, patterns, and relationships.

### Step 7: Dashboard Development

Present the analysis through an interactive Streamlit dashboard.

## Final Findings

Format: **Observation → Interpretation → Business Impact**

### 1. Marketplace overall relies on high single-purchase customer volume

- **Observation:** The marketplace is dominated by individual one-time buyers, with more than 90,000 new customers compared with only a very small proportion of repeat customers.

- **Interpretation:** The platform behaves primarily as a transaction-driven customer acquisition marketplace rather than a business with strong recurring purchasing behavior. This creates a high dependency on continuously attracting new customers.

- **Business Impact:** Improving Customer Lifetime Value (LTV) should become an important growth strategy. Automated post-purchase communication, personalized product recommendations, and cross-category promotions can encourage existing customers to purchase again without depending entirely on additional customer acquisition.

### 2. Geographic order density dictates operational bottleneck severity

- **Observation:** Order volume and revenue are strongly concentrated in Southeast states such as São Paulo (SP), Rio de Janeiro (RJ), and Minas Gerais (MG). In contrast, remote states such as Acre (AC), Amapá (AP), and Roraima (RR) have substantially lower order volumes and weaker delivery-time performance.

- **Interpretation:** High-density urban markets benefit from stronger logistics networks, while long-distance deliveries to remote regions face greater transportation and last-mile challenges.

- **Business Impact:** Delivery estimates should be adapted according to geographic conditions. More realistic delivery windows for remote regions can improve expectation management and potentially reduce negative customer feedback caused by missed delivery estimates.

### 3. Review score distribution is heavily polarized

- **Observation:** Customer reviews are strongly concentrated around 5-star ratings, with approximately 60,000 high-rating reviews, while 1-star reviews form a significant secondary group of roughly 12,000 reviews. Middle ratings such as 2 and 3 stars represent a much smaller share.

- **Interpretation:** Customer feedback appears to be driven strongly by the overall experience. Customers tend to leave very high ratings when their experience is satisfactory, while poor experiences can result in strongly negative ratings.

- **Business Impact:** Proactive customer communication can help reduce dissatisfaction. Delay notifications, order-status updates, and early intervention when an order is at risk can give customers better visibility and potentially prevent avoidable low ratings.

### 4. Category volume and unit value create different revenue drivers

- **Observation:** `bed_bath_table` records the highest product/order volume, with more than 11,000 orders, while categories such as `health_beauty` and `watches_gifts` generate strong monetary revenue despite having lower or comparable order volumes.

- **Interpretation:** High-volume categories generate substantial transaction and logistics activity, whereas categories with stronger monetary value per order contribute significantly to overall revenue efficiency.

- **Business Impact:** Product merchandising can combine high-volume products with higher-value complementary products. Cross-selling and checkout recommendations can increase Average Order Value (AOV) while making better use of every shipment.

### 5. Historical sales growth shows strong seasonal concentration

- **Observation:** Revenue increases from late 2016 through 2017, with a major sales peak around November 2017 reaching approximately R$1.2M. Revenue subsequently maintains a relatively high plateau before the dataset reaches its cutoff period.

- **Interpretation:** Marketplace demand is influenced by strong seasonal and promotional periods, with major sales events creating significant increases in transaction activity.

- **Business Impact:** Sellers, logistics partners, and marketplace operations should prepare inventory, fulfillment capacity, and infrastructure well ahead of major seasonal periods. Better peak-season planning can help capture additional demand while reducing the risk of delivery delays.

## Technology Stack

* **Python** — Data analysis and processing
* **Pandas** — Data cleaning and manipulation
* **Jupyter Notebook** — Analysis workflow
* **MySQL** — Database management
* **SQLAlchemy** — Database connection
* **PyMySQL** — MySQL connectivity
* **Matplotlib** — Data visualization
* **Streamlit** — Interactive dashboard
* **Python-dotenv** — Environment configuration

## Streamlit Dashboard

The dashboard contains six sections:

1. **Business Overview** — Key business metrics
2. **Sales Analysis** — Revenue and category performance
3. **Customer Analysis** — Customer distribution and spending
4. **Seller & Product Analysis** — Seller and category performance
5. **Delivery Analysis** — Delivery time and delays
6. **Customer Experience** — Reviews and delivery satisfaction

## Project Structure

```text
Cart2Insights/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_quality_analysis.ipynb
│   ├── 03_data_cleaning.ipynb
│   ├── 04_sql_analysis.ipynb
│   ├── 05_feature_engineering.ipynb
│   └── 06_eda.ipynb
│
├── streamlit/
│   ├── app.py
│   ├── database.py
│   ├── queries.py
│   ├── utils.py
│   └── requirements.txt
│
├── sql/
│   └── schema.sql
│
├── figures/
├── .env.example
├── .gitignore
└── README.md
```

## Setup

### 1. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r streamlit/requirements.txt
```

### 3. Configure Database

Create a MySQL database and add your database credentials to a local `.env` file.

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=olist_ecommerce
```

Do not upload the `.env` file to GitHub.

### 4. Add Dataset

Place the raw Olist CSV files inside:

```text
data/raw/
```

### 5. Run the Notebooks

Run the notebooks in this order:

```text
01 → 02 → 03 → 04 → 05 → 06
```

### 6. Run the Dashboard

```bash
streamlit run streamlit/app.py
```

## Database

The project uses MySQL to store the cleaned and processed e-commerce data.

Main tables:

```text
customers
orders
order_items
products
sellers
payments
reviews
```

The tables are connected using primary and foreign key relationships.

## Output

The project produces:

* Cleaned datasets
* MySQL database tables
* Business metrics
* EDA visualizations
* Business insights
* Interactive Streamlit dashboard

## Conclusion

Cart2Insights provides an end-to-end e-commerce analytics workflow, starting from raw data and ending with an interactive business intelligence dashboard.

The project demonstrates how data cleaning, SQL, feature engineering, visualization, and dashboard development can be combined to generate meaningful business insights.

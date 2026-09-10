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

**Format: Observation → Interpretation → Business Impact**

### 1. Marketplace overall relies on high single-purchase customer volume

* **Observation:** The marketplace is dominated by one-time buyers, with more than 90,000 customers making only a single purchase and only a small proportion returning for additional purchases.
* **Interpretation:** The platform currently depends heavily on continuously acquiring new customers rather than generating strong recurring purchasing behavior from existing customers.
* **Business Impact:** Improving Customer Lifetime Value (LTV) should be a key growth strategy. Personalized product recommendations, post-purchase communication, and targeted cross-category promotions can encourage existing customers to make repeat purchases.

### 2. Repeat customers demonstrate significantly higher spending value

* **Observation:** Repeat customers have an average spending value of approximately R$307.65, compared with around R$160.28 for first-time customers, meaning repeat customers spend nearly twice as much.
* **Interpretation:** Customers who return to the marketplace demonstrate higher purchasing value and represent an important revenue opportunity.
* **Business Impact:** Converting a portion of one-time buyers into repeat customers can increase revenue without relying entirely on acquiring new customers. Loyalty programs, personalized recommendations, and targeted offers can support this conversion.

### 3. Delivery performance has a strong relationship with customer satisfaction

* **Observation:** Orders delivered on time receive an average review score of approximately 4.29, while delayed orders receive an average score of around 2.27.
* **Interpretation:** Delivery reliability has a strong relationship with customer satisfaction. Delays can significantly reduce the likelihood of customers giving positive reviews.
* **Business Impact:** Improving delivery reliability should be treated as a customer-experience priority. Better delivery tracking, proactive delay notifications, and improved fulfillment planning can help reduce negative customer feedback.

### 4. Geographic concentration creates different operational requirements

* **Observation:** Order volume and revenue are strongly concentrated in Southeast states such as São Paulo (SP), Rio de Janeiro (RJ), and Minas Gerais (MG), while remote states have substantially lower order volumes and weaker delivery-time performance.
* **Interpretation:** High-density regions benefit from stronger logistics networks, while long-distance deliveries to remote regions face greater transportation and last-mile challenges.
* **Business Impact:** Logistics and fulfillment resources can be prioritized according to regional demand. Delivery estimates can also be adapted for remote locations to provide more realistic customer expectations.

### 5. A small group of top sellers contributes significantly to marketplace revenue

* **Observation:** The top 10 sellers, representing only around 0.3% of active sellers, contribute approximately 13.1% of total marketplace revenue.
* **Interpretation:** Marketplace revenue is concentrated among a relatively small group of high-performing sellers, while the majority of sellers contribute smaller individual revenue amounts.
* **Business Impact:** Retaining and supporting high-performing sellers can help protect a significant portion of marketplace revenue. Dedicated seller support and performance-based programs can strengthen long-term seller relationships.

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

### **Run the Script**

1. Use the following command to install all dependencies:

```bash
pip install -r requirements.txt
```

2. Need to create a database in MySQL Workbench
3. Replace the password of the MySQL Workbench and the database name in the following code of the script

```python
db_url = "mysql+pymysql://root:password@localhost:3306/db_name"
```

4. Run the following command on the terminal:

```bash
python etl.py
```

# **Retail Orders Data Analysis**

The **Retail Orders Data Analysis** project focuses on building an efficient ETL pipeline to process, analyze, and store retail transaction data. This pipeline extracts raw data, cleans and transforms it to ensure consistency, and calculates essential business metrics like revenue, profit, and discounts. The processed data is loaded into a MySQL database, enabling scalable storage and easy access for advanced analysis. By leveraging Python and key libraries like `pandas` and `sqlalchemy`, this project provides a streamlined solution for understanding retail performance across categories, regions, and customer segments.

---

### **Project Description**

This project involves building an **ETL (Extract, Transform, Load)** pipeline to process and analyze retail orders data. The dataset contains transaction details such as order dates, ship modes, customer segments, product categories, pricing details, and geographical information. The pipeline is designed to extract raw data, clean and transform it, and load the processed data into a **MySQL database** for efficient storage and further analysis.

---

### **Key Objectives**

1. **Extract**: Automate the retrieval of raw retail data from a Kaggle dataset and handle compressed files efficiently.
2. **Transform**:
   - Clean the dataset by handling missing values, removing duplicates, and ensuring consistency in column names and values.
   - Perform feature engineering to derive key metrics like discounts, revenue, and profit.
   - Validate data to ensure it meets analytical requirements, such as handling invalid values and checking for outliers.
3. **Load**: Store the cleaned and transformed data in a structured format within a MySQL database, enabling downstream analytics and reporting.

---

### **Features of the Pipeline**

- **Automated Extraction**: Simplifies downloading and extracting data for streamlined processing.
- **Data Cleaning**: Handles missing values, removes duplicates, and ensures categorical values are consistent.
- **Feature Engineering**: Generates new insights by calculating metrics like revenue, profit, and discounts.
- **Database Integration**: Seamlessly loads processed data into a relational database for scalable and efficient querying.

---

### **Technologies Used**

- **Python Libraries**:
  - `pandas` and `numpy` for data manipulation and analysis.
  - `sqlalchemy` for database interactions.
  - `zipfile` for handling compressed files.
- **Database**: MySQL for storing the processed data.
- **Data Source**: Kaggle dataset for retail orders.

---

### **Project Outcomes**

- A robust ETL pipeline capable of processing retail orders data in an automated and efficient manner.
- A clean, well-structured database ready for advanced analytics and business intelligence reporting.
- Enhanced understanding of retail performance metrics like revenue, profit, and discounts across categories and regions.

---

## Python ETL Code Documentation

This documentation provides a step-by-step explanation of the Python code used for an ETL (Extract, Transform, Load) process on retail orders data.

---

### **1. Import Necessary Libraries**

The script begins with importing essential libraries:

```python
import kaggle
import pandas as pd
import numpy as np
import sqlalchemy as sal
import zipfile
```

These libraries are used for:

- Accessing Kaggle datasets.
- Data manipulation (`pandas`, `numpy`).
- Database operations (`sqlalchemy`).
- Handling compressed files (`zipfile`).

---

```python
#################### Important ##########################
# run on terminal -> kaggle datasets download ankitbansal06/retail-orders -f orders.csv
#########################################################
```

---

### **2. Extract Data**

The retail orders dataset is downloaded from Kaggle and extracted:

```python
zip_ref = zipfile.ZipFile('orders.csv.zip')
zip_ref.extractall()  # Extract file to directory
zip_ref.close()  # Close the file
```

This step extracts `orders.csv` for further processing.

---

### **3. Load Data**

The CSV file is read into a pandas DataFrame:

```python
df = pd.read_csv('orders.csv')
print(df.head())
print(f"Data Shape:\n{df.shape}\n")
```

This provides an initial look at the dataset, including its shape and structure.

---

### **4. Data Cleaning**

#### Convert `Order Date` to datetime:

```python
df['Order Date'] = pd.to_datetime(df['Order Date'], format="%Y-%m-%d")
```

#### Handle missing values:

```python
df = df.dropna().reset_index(drop=True)
```

This removes rows with null values as they are minimal.

#### Check for duplicates:

```python
df.duplicated().sum()
```

Duplicates are checked and skipped since there are none.

---

### **5. Handle Categorical Columns**

#### Check unique values:

```python
cat_cols = ['Ship Mode', 'Segment', 'Country', 'Region', 'Category', 'Sub Category']
for col in cat_cols:
  print(f"Unique Values of '{col}':\n{df[col].unique()}\n")
```

#### Standardize `Ship Mode` values:

```python
df['Ship Mode'] = df['Ship Mode'].replace({'unknown': 'Unknown', 'Same Day': 'Unknown'})
```

---

### **6. Validate Numerical Columns**

Check for outliers or invalid values in numerical columns:

```python
df.describe()
```

For example, ensure `quantity` is not negative.

---

### **7. Rename Columns**

Standardize column names for consistency:

```python
df.columns = df.columns.str.lower().str.replace(' ', '_')
```

---

### **8. Feature Engineering**

Derive new columns for analysis:

- **Discount**:
  ```python
  df['discount'] = df['list_price'] * (df['discount_percent'] * 0.01)
  ```
- **Revenue**:
  ```python
  df['revenue'] = df['list_price'] - df['discount']
  ```
- **Profit**:
  ```python
  df['profit'] = np.round(df['revenue'] - df['cost_price'], 2)
  ```

Drop unnecessary columns to optimize the dataset:

```python
df = df.drop(columns=['list_price', 'cost_price', 'discount_percent'])
```

---

### **9. Load Data to MySQL Database**

Define a function to load the cleaned DataFrame into a MySQL database:

```python
def load_data_to_database(df, table_name, db_url):
    try:
    print("Data Loading to the Database Starting..........")
    # Create the SQLAlchemy engine
    engine = sal.create_engine(db_url)
    # Connect to the database
    conn = engine.connect()
    # Load the DataFrame into the database
    # Writes the DataFrame `df` to the SQL table `table_name`, replacing the table if it exists, without including the DataFrame index.
    df.to_sql(table_name, con=conn, index=False, if_exists='replace')
    print(f"Data successfully loaded into the '{table_name}' table.")
  except Exception as e:
    print("Error occurred while loading data to the database:", e)
  finally:
    try:
      conn.close()
      print("Database connection closed.")
    except NameError:
      print("Connection not established, nothing to close.")
```

- Uses `sqlalchemy` to connect to the database.
- Loads data into a specified table using `pandas.DataFrame.to_sql`.
- Includes error handling for robust operation.

#### Example Usage:

```python
db_url = "mysql+pymysql://root:password@localhost:3306/db_name"  # have to give the password and db_name (database name)
load_data_to_database(df, "orders_data", db_url)
```

---

### **Output Verification**

After running the script:

1. Data is cleaned, transformed, and loaded into the MySQL database.
2. Key outputs (like summary statistics, unique values) are printed for validation.

---

## SQL Code Documentation

This documentation provides a detailed explanation of five SQL queries solved using MySQL, each addressing specific business questions related to sales and revenue analysis.

---

### 1. Find the Top 10 Highest Revenue-Generating Products

#### Query:

```sql
select product_id, round(sum(revenue), 2) as revenue
from orders_data
group by product_id
order by revenue desc
limit 10;
```

#### Explanation:

- **Objective**: Identify the top 10 products that generated the highest revenue.
- **Key Steps**:
  1. Aggregate revenue for each `product_id` using `SUM(revenue)`.
  2. Use `ROUND()` to format revenue to two decimal places.
  3. Sort the results in descending order of revenue.
  4. Limit the output to the top 10 results.

---

### 2. Find Top 5 Highest-Selling Products in Each Region

#### Query:

```sql
with cte1 as (
select region, product_id, round(sum(revenue), 2) as sales_price
from orders_data
group by 1, 2
),

cte2 as (
select *,
       row_number() over(partition by region order by sales_price desc) as rn
from cte1
)

select region, product_id, sales_price
from cte2
where rn < 6;
```

#### Explanation:

- **Objective**: Determine the top 5 highest-selling products within each region.
- **Key Steps**:
  1. Use a Common Table Expression (CTE) `cte1` to calculate total sales (`sales_price`) per `region` and `product_id`.
  2. Apply `ROW_NUMBER()` in `cte2` to rank products within each region by their `sales_price`.
  3. Filter results to include only the top 5 products (`rn < 6`) for each region.

---

### 3. Find Month-over-Month (MoM) Growth for 2022 and 2023 Sales

#### Query:

```sql
with cte1 as (
select date_format(order_date, '%Y-%m-01') as month,
       year(order_date) as year,
       round(sum(revenue), 2) as current_year_sales
from orders_data
group by 1, 2
order by 1, 2
),

cte2 as (
select *,
       lag(current_year_sales) over(partition by month(month) order by year) as previous_year_sales
from cte1
),

cte3 as (
select *,
       case when current_year_sales is not null then
                 round((current_year_sales - previous_year_sales) / previous_year_sales * 100, 2)
            else null
       end as mom_sales_growth_percentage
from cte2)

select *
from cte3
where previous_year_sales is not null;
```

#### Explanation:

- **Objective**: Compare sales growth for the same month across 2022 and 2023.
- **Key Steps**:
  1. Use `cte1` to calculate monthly sales aggregated by `year`.
  2. Use `LAG()` in `cte2` to fetch sales for the same month in the previous year.
  3. Compute MoM growth percentage in `cte3` using:
     ```sql
     (current_year_sales - previous_year_sales) / previous_year_sales * 100
     ```
  4. Filter out rows where `previous_year_sales` is NULL.

---

### 4. For Each Category, Identify the Month with the Highest Sales

#### Query:

```sql
with cte1 as (
select category, order_date, round(sum(revenue), 2) as sales
from orders_data
group by 1, 2
),

cte2 as (
select *,
       row_number() over(partition by category order by sales desc) as rn
from cte1
)

select category, order_date, sales
from cte2
where rn = 1;
```

#### Explanation:

- **Objective**: Find the month with the highest sales for each `category`.
- **Key Steps**:
  1. Use `cte1` to calculate monthly sales for each `category`.
  2. Apply `ROW_NUMBER()` in `cte2` to rank months by sales within each category.
  3. Filter results to include only the top-ranked (`rn = 1`) month for each category.

---

### 5. Identify the Sub-Category with the Highest Growth in 2023 Compared to 2022

### Query:

```sql
with cte1 as (
select date_format(order_date, '%Y-%m-01') as month,
       year(order_date) as year,
       sub_category,
       round(sum(revenue), 2) as current_year_sales
from orders_data
group by 1, 2, 3
order by 1, 2
),

cte2 as (
select *,
       lag(current_year_sales) over(partition by sub_category order by year, month) as previous_year_sales
from cte1
),

cte3 as (
select *,
       case when previous_year_sales > 0 then
                 round((current_year_sales - previous_year_sales) / previous_year_sales * 100, 2)
            else null
       end as mom_sales_growth_percentage
from cte2
),

cte4 as (
select *,
       row_number() over(partition by sub_category order by mom_sales_growth_percentage desc) as rn
from cte3
where previous_year_sales is not null
)

select sub_category, mom_sales_growth_percentage as best_growth, month as best_growth_month
from cte4
where rn = 1
order by best_growth desc
limit 1;
```

#### Explanation:

- **Objective**: Determine the sub-category with the highest growth in 2023 compared to 2022.
- **Key Steps**:
  1. Use `cte1` to calculate monthly sales for each `sub_category` and `year`.
  2. Use `LAG()` in `cte2` to fetch sales for the previous year for the same sub-category and month.
  3. Compute MoM growth percentage in `cte3` for valid comparisons where `previous_year_sales > 0`.
  4. Use `ROW_NUMBER()` in `cte4` to rank sub-categories by their highest growth.
  5. Filter to include only the sub-category with the highest growth (`rn = 1`) and limit the result to the top sub-category.

---

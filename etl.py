# Import necessary libraries
# import kaggle
import pandas as pd
import numpy as np
import sqlalchemy as sal

# import os
# print('Get current working directory : ', os.getcwd())

#################### Important ##########################
# run on terminal -> kaggle datasets download ankitbansal06/retail-orders -f orders.csv
#########################################################


#extract file from zip file
import zipfile
zip_ref = zipfile.ZipFile('orders.csv.zip') 
zip_ref.extractall() # extract file to dir
zip_ref.close() # close file


# Load the data
df = pd.read_csv('orders.csv')
print(df.head())
print(f"Data Shape:\n{df.shape}\n")

print(f"Data Types:\n{df.dtypes}\n")
# Convert Order Date to Datetime
df['Order Date'] = pd.to_datetime(df['Order Date'], format="%Y-%m-%d")
print(f"Data Types after Convertion:\n{df.dtypes}\n")

print(f"Checking Nulls:\n{df.isna().sum()}\n")
# There is 1 null value which is very low so drop them
df = df.dropna().reset_index(drop = True)
print(f"Verifyling Zero Nulls:\n{df.isna().sum()}\n")

print(f"Checking Duplicates:\n{df.duplicated().sum()}\n")
# There is no duplicates
print(f"Data Shape after Cleaning:\n{df.shape}\n")
print(df.head())

# Check unique values of the categorical columns to see whether there is any unwanted levels
cat_cols = ['Ship Mode', 'Segment', 'Country', 'Region', 'Category', 'Sub Category']
for col in cat_cols:
  print(f"""Unique Values of '{col}' column are:\n{df[col].unique()}\n""")
  
# In Ship Mode, convert 'Same Day' and 'unknown' to 'Unknown'
df['Ship Mode'] = df['Ship Mode'].replace({'unknown': 'Unknown', 'Same Day': 'Unknown'})

# Again check the unique values
for col in cat_cols:
  print(f"""After Convertion\nUnique Values of '{col}' column are:\n{df[col].unique()}\n""")

# Check summary of the numeric columns to see whether there is any impossible values i.e., quantity < 0
print(f"Summary Statistics: \n{df.describe()}\n")


# Rename columns names ..make them lower case and replace space with underscore
df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
print(df.head())
print("\n")

# Derive discount, sales_price and profit
# Discount = List Price x Percentage of Discount
df['discount'] = df['list_price']*(df['discount_percent']*0.01) # Percentage so, (1/100=0.01)

# Sales/Revenue = List Price - Discount
df['revenue'] = df['list_price'] - df['discount']

# Profit = Revenue - Cost
df['profit'] = np.round(df['revenue'] - df['cost_price'], 2)

# Drop unnecessary columns
df = df.drop(columns=['list_price','cost_price','discount_percent'])

print(f"Data after deriving discount, sales_price & profit, and dropping 'list_price','cost_price','discount_percent':\n{df.head()}\n")


# Load the data to the MySQL database
def load_data_to_database(df, table_name, db_url):
  """
  Load a DataFrame into a MySQL database table with error handling.

  Parameters:
  - df: pandas DataFrame to load into the database.
  - table_name: Name of the table where data will be loaded.
  - db_url: Database connection URL string in the format:
        'mysql+pymysql://username:password@hostname:port/database_name'

  Returns:
  - None: Prints success or error message.
  """
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

db_url = "mysql+pymysql://root:password@localhost:3306/database_name"   # Need to replace password and db_name
load_data_to_database(df, "orders_data", db_url)
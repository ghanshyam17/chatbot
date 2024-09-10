import pandas as pd
from sqlalchemy import DateTime, create_engine
import pyodbc
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
import urllib
conn_str = (
    'DSN=SAPB1SQL;'  
    'UID=User18;'  
    'PWD=Toolway23;'  
)


# Define connection string using SQLAlchemy and pyodbc
connection_string = (
    'mssql+pyodbc:///?odbc_connect=' + 
    urllib.parse.quote_plus('DSN=SAPB1SQL;UID=User18;PWD=Toolway23;')
)

# Create SQLAlchemy engine
engine = create_engine(connection_string)


# Query to fetch data from SAP B1 (example: fetching product data)
query = """
SELECT
    ROW_NUMBER() OVER(ORDER BY T0.DocEntry) AS '#',
    T4.SlpName AS 'Sales Rep',
    T0.DocType AS 'Mode',
    T0.DocType AS 'Type',
    T0.DocNum AS 'C#',
    T0.DocNum AS 'Doc #',
    T0.DocDate AS 'Posting Date',
    T0.NumAtCard AS 'Customer Ref.No.',
    T1.ShipToCode AS 'S Address',
    T2.City AS 'S City',
    T2.ZipCode AS 'S ZipCode',
    T2.State AS 'S Province',
    T2.Country AS 'S Country',
    T3.ItemCode AS 'Item #',
    T3.ItemName AS 'Item Description',
    T1.WhsCode AS 'Whse #',
    T1.QtyToShip AS 'Q2S',
    T1.Quantity AS 'Quantity',
    T1.Price AS 'Unit Price',
    T1.DiscPrcnt AS 'Ln Disc',
    T1.LineTotal AS 'Price after Discount',
    T1.TotalSumSy AS 'Row Total',
    T0.DiscPrcnt AS 'Doc Disc',
    T1.Quantity AS 'Quantity.1',
    T1.TotalSumSy AS 'AMOUNT',
    (T1.LineTotal - T1.TotalSumSy) AS 'Gross Profit',
    T1.FreeTxt AS 'Line Remark'
FROM
    ORDR T0
INNER JOIN
    RDR1 T1 ON T0.DocEntry = T1.DocEntry
LEFT JOIN
    CRD1 T2 ON T1.ShipToCode = T2.Address
LEFT JOIN
    OITM T3 ON T1.ItemCode = T3.ItemCode
LEFT JOIN
    OSLP T4 ON T0.SlpCode = T4.SlpCode
WHERE
    T0.DocDate BETWEEN '2022-06-01' AND '2024-08-01'
ORDER BY
    T0.DocDate ASC;
"""
# Step 2: Load the data into a pandas DataFrame
conn = pyodbc.connect(conn_str)

# Step 2: Load the data into a pandas DataFrame
df = pd.read_sql(query, conn)
df1 = pd.read_sql(query, engine)
# Step 3: Handle missing values in the DataFrame (fill NaNs with None or 0 for numerical values)
df1.fillna({
    'Sales Rep': None,
    'Mode': None,
    'Type': None,
    'Customer Ref.No.': None,
    'S Address': None,
    'S City': None,
    'S ZipCode': None,
    'S Province': None,
    'S Country': None,
    'Item #': None,
    'Item Description': None,
    'Whse #': None,
    'Q2S': 0.0,
    'Quantity': 0.0,
    'Unit Price': 0.0,
    'Ln Disc': 0.0,
    'Price after Discount': 0.0,
    'Row Total': 0.0,
    'Doc Disc': 0.0,
    'AMOUNT': 0.0,
    'Gross Profit': 0.0,
    'Line Remark': None
}, inplace=True)

# Step 4: Close the connection
conn.close()

# Define SQLAlchemy base and model
Base = declarative_base()

class Analysis(Base):
    __tablename__ = 'analysis'
    
    id = Column(Integer, primary_key=True)
    row_number = Column(Integer)
    sales_rep = Column(String)
    mode = Column(String)
    type = Column(String)
    customer_ref_no = Column(String)
    doc_num = Column(Integer)
    posting_date = Column(DateTime)
    ship_to_code = Column(String)
    s_city = Column(String)
    s_zipcode = Column(String)
    s_province = Column(String)
    s_country = Column(String)
    item_code = Column(String)
    item_description = Column(String)
    warehouse_code = Column(String)
    qty_to_ship = Column(Float)
    quantity = Column(Float)
    unit_price = Column(Float)
    line_discount = Column(Float)
    price_after_discount = Column(Float)
    row_total = Column(Float)
    doc_discount = Column(Float)
    amount = Column(Float)
    gross_profit = Column(Float)
    line_remark = Column(String)

# Step 5: Create the SQLite database and insert data
engine = create_engine('sqlite:///analysis.db', echo=True)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert the data into the database
try:
    for index, row in df1.iterrows():
        analysis = Analysis(
            row_number=row['#'], 
            sales_rep=row['Sales Rep'], 
            mode=row['Mode'], 
            type=row['Type'], 
            doc_num=row['Doc #'], 
            posting_date=row['Posting Date'], 
            customer_ref_no=row['Customer Ref.No.'], 
            ship_to_code=row['S Address'], 
            s_city=row['S City'], 
            s_zipcode=row['S ZipCode'], 
            s_province=row['S Province'], 
            s_country=row['S Country'], 
            item_code=row['Item #'], 
            item_description=row['Item Description'], 
            warehouse_code=row['Whse #'], 
            qty_to_ship=row['Q2S'], 
            quantity=row['Quantity'], 
            unit_price=row['Unit Price'], 
            line_discount=row['Ln Disc'], 
            price_after_discount=row['Price after Discount'], 
            row_total=row['Row Total'], 
            doc_discount=row['Doc Disc'], 
            amount=row['AMOUNT'], 
            gross_profit=row['Gross Profit'], 
            line_remark=row['Line Remark']
        )
        session.add(analysis)
    session.commit()

    # Verify data insertion
    inserted_analysis = session.query(Analysis).limit(5).all()
    for analysis in inserted_analysis:
        print(f"Analysis ID: {analysis.id}, Description: {analysis.item_description}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    session.close()

print("End of script")

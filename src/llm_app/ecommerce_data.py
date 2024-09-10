import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

# Step 1: Read the CSV file
df = pd.read_excel('/Users/ghanshyam/Projects/fornax/llm/langchain/Krylon 09-05-2024_saved 2.xlsx', encoding='ISO-8859-1')
# Convert NaN in CustomerID to None for database compatibility
df['CustomerID'] = df['CustomerID'].apply(lambda x: None if pd.isna(x) else int(x))
print(df.info())

# Step 2: Define your database model
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    InvoiceNo = Column(String)  # Changed to String to match CSV schema
    StockCode = Column(String)
    Description = Column(String)
    Quantity = Column(Integer)
    InvoiceDate = Column(DateTime)  # Kept as DateTime, assuming correct format in CSV
    UnitPrice = Column(Float)
    CustomerID = Column(Integer, nullable=True)  # Correct as per schema, handling None values
    Country = Column(String)

# Ensure the correct database file path
engine = create_engine('sqlite:///ecommerce1.db', echo=True)
Base.metadata.create_all(engine)  # This line creates the table schema

# Step 4: Insert data into the database
Session = sessionmaker(bind=engine)
session = Session()

try:
    for index, row in df.iterrows():
        product = Product(
            InvoiceNo=row['InvoiceNo'], 
            StockCode=row['StockCode'], 
            Description=row['Description'], 
            Quantity=row['Quantity'], 
            InvoiceDate=pd.to_datetime(row['InvoiceDate']),  # Assuming the InvoiceDate is in a format pandas can parse
            UnitPrice=row['UnitPrice'], 
            CustomerID=row['CustomerID'],  # Now correctly handling None values
            Country=row['Country']
        )
        session.add(product)
    session.commit()

    # Step 5: Verify data insertion
    inserted_products = session.query(Product).limit(5).all()
    for product in inserted_products:
        print(f"Product ID: {product.id}, Description: {product.Description}")
except Exception as e:
    session.rollback()
    print(f"An error occurred: {e}")
finally:
    session.close()
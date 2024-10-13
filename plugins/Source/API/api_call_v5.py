import requests
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, select
from datetime import datetime
import psycopg2
import random

def get_and_store_metal_prices():
    # SQLAlchemy setup
    #DATABASE_URL = "postgresql+psycopg2://postgres:<password>@192.168.1.164:5433/MetalPrices" # Wired IP ISP1
    DATABASE_URL = "postgresql+psycopg2://postgres:<password>@192.168.8.6:5433/MetalPrices" # Wired IP ISP2
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Define the metal_prices_analytics table
    metadata = MetaData()

    metal_prices_analytics = Table(
        'metal_prices_analytics', metadata,
        Column('id', Integer, primary_key=True),
        Column('timestamp', DateTime),
        Column('gold_price', Float),
        Column('silver_price', Float),
        Column('platinum_price', Float),
        Column('palladium_price', Float)
    )

    # Create table if it doesn't exist
    metadata.create_all(engine)

    # Generate a unique random number
    def generate_unique_id(conn, table):
        while True:
            random_number = random.randint(1, 1000000)
            query = select(table.c.id).where(table.c.id == random_number)
            result = conn.execute(query).fetchone()
            if result is None:
                return random_number

    # API call to get metal prices
    api_url = "https://api.metalpriceapi.com/v1/latest"
    params = {
        "api_key": "<api_key>",
        "base": "USD",
        "currencies": "XAU,XAG,XPT,XPD"
    }

    response = requests.get(api_url, params=params)
    data = response.json()

    # Debug: Print the API data to check its structure
    print("API Response:", data)

    # Extract metal prices
    timestamp = datetime.utcfromtimestamp(data['timestamp'])
    gold_price = data['rates'].get('USDXAU', None)  # Use .get() to avoid KeyErrors
    silver_price = data['rates'].get('USDXAG', None)
    platinum_price = data['rates'].get('USDXPT', None)
    palladium_price = data['rates'].get('USDXPD', None)

    # Check if data was correctly extracted
    print("Gold:", gold_price, "Silver:", silver_price, "Platinum:", platinum_price, "Palladium:", palladium_price)

    # Insert data into the metal_prices_analytics table
    # Insert data using a session for explicit transaction management
    with Session() as session:
        random_number = generate_unique_id(session, metal_prices_analytics)
   
        stmt = insert(metal_prices_analytics).values(
            id=random_number,
            timestamp=timestamp,
            gold_price=gold_price,
            silver_price=silver_price,
            platinum_price=platinum_price,
            palladium_price=palladium_price
            )
        session.execute(stmt)
        session.commit()  # Explicit commit
        
    print("Data inserted successfully!")

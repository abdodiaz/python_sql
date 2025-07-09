from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, ForeignKey,insert,select
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# load info from .env
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
# url for connection
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# create connection with database
engine = create_engine(DATABASE_URL, echo=True)
# table mnpltion
metadata=MetaData()

# tables
clients = Table(
    "clients", metadata,
    Column("client_id", Integer, primary_key=True),
    Column("first_name", String(100), nullable=False),
    Column("last_name", String(100), nullable=False),
    Column("email", String(255), unique=True),
    Column("phone_number", String(20))
)


destinations = Table(
    "destinations", metadata,
    Column("destination_id", Integer, primary_key=True),
    Column("name", String(150), nullable=False),
    Column("country", String(100)),
    Column("price_per_person", Float, nullable=False)
)


bookings = Table(
    "bookings", metadata,
    Column("booking_id", Integer, primary_key=True),
    Column("client_id", Integer, ForeignKey("clients.client_id"), nullable=False),
    Column("booking_date", DateTime, default=datetime.utcnow),
    Column("total_price", Float)
)


booking_items = Table(
    "booking_items", metadata,
    Column("item_id", Integer, primary_key=True),
    Column("booking_id", Integer, ForeignKey("bookings.booking_id"), nullable=False),
    Column("destination_id", Integer, ForeignKey("destinations.destination_id"), nullable=False),
    Column("travelers_count", Integer, nullable=False)
)

# create tables
# metadata.create_all(engine)
with engine.begin() as conn:
    conn.execute(
        insert(clients),
        [
            {"first_name": "Alice", "last_name": "Smith", "email": "alice@example.com", "phone_number": "0601010101"},
            {"first_name": "Bob", "last_name": "Johnson", "email": "bob@example.com", "phone_number": "0602020202"},
            {"first_name": "Charlie", "last_name": "Lee", "email": "charlie@example.com", "phone_number": "0603030303"},
            {"first_name": "Dina", "last_name": "Mansour", "email": "dina@example.com", "phone_number": "0604040404"},
            {"first_name": "Elias", "last_name": "Nouri", "email": "elias@example.com", "phone_number": "0605050505"},
        ]
    )

    conn.execute(
        insert(destinations),
        [
            {"name": "Paris", "country": "France", "price_per_person": 250.0},
            {"name": "Tokyo", "country": "Japan", "price_per_person": 800.0},
            {"name": "Marrakech", "country": "Morocco", "price_per_person": 150.0},
            {"name": "New York", "country": "USA", "price_per_person": 600.0},
            {"name": "Barcelona", "country": "Spain", "price_per_person": 300.0},
        ]
    )

    conn.execute(
        insert(bookings),
        [
            {"client_id": 1, "booking_date": datetime(2025, 7, 1), "total_price": 500.0},
            {"client_id": 2, "booking_date": datetime(2025, 7, 2), "total_price": 800.0},
            {"client_id": 3, "booking_date": datetime(2025, 7, 3), "total_price": 600.0},
        ]
    )

    conn.execute(
        insert(booking_items),
        [
            {"booking_id": 1, "destination_id": 1, "travelers_count": 2},  # Paris
            {"booking_id": 1, "destination_id": 3, "travelers_count": 1},  # Marrakech
            {"booking_id": 2, "destination_id": 2, "travelers_count": 1},  # Tokyo
            {"booking_id": 3, "destination_id": 4, "travelers_count": 2},  # New York
            {"booking_id": 3, "destination_id": 5, "travelers_count": 1},  # Barcelona
        ]
    )

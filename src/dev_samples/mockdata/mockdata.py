import argparse
from loguru import logger
from sqlalchemy import create_engine, MetaData, Table, select, Column, Integer, String, insert, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from dotenv import load_dotenv
import os
import uuid 
from faker import Faker

class POSTGRESConfig:

    def __init__(self, env: str = "dev"):
        
        prefix = env.upper()

        self.POSTGRES_HOST = os.getenv(f'{prefix}_POSTGRES_HOST')
        self.POSTGRES_PORT = int(os.getenv(f'{prefix}_POSTGRES_PORT'))
        self.POSTGRES_DB = os.getenv(f'{prefix}_POSTGRES_DB')
        self.POSTGRES_USER = os.getenv(f'{prefix}_POSTGRES_USER')
        self.POSTGRES_PASSWORD = os.getenv(f'{prefix}_POSTGRES_PASSWORD')

        self.engine = create_engine(f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}')
        self.metadata = MetaData()

        self.src_user_signups = Table(
            'src_user_signups',
            self.metadata,
            Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
            Column('signup', TIMESTAMP, nullable=False),
            Column('country', String, nullable=False),
            Column('platform', String, nullable=False),
            Column('app_version_signup', String, nullable=False),
            Column('device_id', UUID(as_uuid=True), nullable=False),        
            Column('updated_at', TIMESTAMP, nullable=False),
            )

        # Create the table if it doesn't exist
        self.metadata.create_all(self.engine)
        logger.info(f"Connected to PostgreSQL database {self.POSTGRES_DB} and ensured table exists.")
        
    def insert_user_signup(self, record: dict):
        with self.engine.connect() as conn:
            with conn.begin(): 
                stmt = insert(self.src_user_signups).values(**record)
                conn.execute(stmt)

def generate_fake_data(db, n=50):
    fake = Faker()
    countries = ['US', 'GB', 'DE', 'FR', 'IN', 'BR', 'CA', 'AU']
    platforms = ['ios', 'android']
    app_versions = ['1.0.0', '1.1.0', '1.2.5', '2.0.0', '2.1.3']
    
    for _ in range(n):
        yield {
            'id': uuid.uuid4(),
            'signup': fake.date_time_between(start_date='-2y', end_date='now'),
            'country': fake.random.choice(countries),
            'platform': fake.random.choice(platforms),
            'app_version_signup': fake.random.choice(app_versions),
            'device_id': uuid.uuid4(),
            'updated_at': fake.date_time_between(start_date='-2y', end_date='-1y'),
        }
    
    logger.info(f"Generated {n} rows in database: {db.POSTGRES_DB}.")
                
if __name__ == "__main__":
    
    # CLI argument parsing
    parser = argparse.ArgumentParser(description="Generate mock data")
    parser.add_argument(
        "-n", "--num_records",
        type=int,
        default=50,
        help="Number of records to generate (default: 50)"
    )
    
    parser.add_argument(
        "-e", "--env",
        type=str,
        choices=["dev","cprod"],
        default="dev",
        help="Target environment (default: dev)"
    )
    
    args = parser.parse_args()
    
    db = POSTGRESConfig()
    for user_record in generate_fake_data(db, args.num_records):
        db.insert_user_signup(user_record)
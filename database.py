import os
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

class Database:
    def __init__(self):
        database_url = os.environ.get('DATABASE_URL', 'sqlite:///rideshare.db')
        self.is_postgres = database_url.startswith('postgresql')
        self.engine = create_engine(database_url)
        self.backup_dir = "backups"
        os.makedirs(self.backup_dir, exist_ok=True)
        self.initialize_tables()

    def initialize_tables(self):
        with self.engine.connect() as conn:
            if self.is_postgres:
                conn.execute(text("""
                    DO $$ BEGIN
                        CREATE SEQUENCE IF NOT EXISTS rides_id_seq;
                    EXCEPTION WHEN duplicate_table THEN NULL;
                    END $$;
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS rides (
                        id INTEGER PRIMARY KEY DEFAULT nextval('rides_id_seq'),
                        date DATE NOT NULL,
                        hours FLOAT NOT NULL,
                        miles FLOAT NOT NULL,
                        earnings FLOAT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
            else:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS rides (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE NOT NULL,
                        hours FLOAT NOT NULL,
                        miles FLOAT NOT NULL,
                        earnings FLOAT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
            conn.commit()

    def add_ride(self, date, hours, miles, earnings):
        with self.engine.connect() as conn:
            conn.execute(
                text("INSERT INTO rides (date, hours, miles, earnings) VALUES (:date, :hours, :miles, :earnings)"),
                {"date": date, "hours": hours, "miles": miles, "earnings": earnings}
            )
            conn.commit()

    def get_rides(self, start_date=None, end_date=None):
        query = "SELECT * FROM rides"
        if start_date and end_date:
            query += " WHERE date BETWEEN :start_date AND :end_date"
        query += " ORDER BY date"

        with self.engine.connect() as conn:
            result = conn.execute(
                text(query),
                {"start_date": start_date, "end_date": end_date} if start_date and end_date else {}
            )
            return pd.DataFrame(result.fetchall(), columns=result.keys())

    def delete_ride(self, ride_id):
        with self.engine.connect() as conn:
            conn.execute(text("DELETE FROM rides WHERE id = :id"), {"id": ride_id})
            conn.commit()

    def update_ride(self, ride_id, date, hours, miles, earnings):
        with self.engine.connect() as conn:
            conn.execute(
                text("""
                    UPDATE rides 
                    SET date = :date, hours = :hours, miles = :miles, earnings = :earnings 
                    WHERE id = :id
                """),
                {"id": ride_id, "date": date, "hours": hours, "miles": miles, "earnings": earnings}
            )
            conn.commit()

    def backup_data(self, backup_name):
        if not backup_name.endswith('.json'):
            backup_name += '.json'

        backup_path = os.path.join(self.backup_dir, backup_name)
        df = self.get_rides()

        if df.empty:
            df = pd.DataFrame(columns=['id', 'date', 'hours', 'miles', 'earnings', 'created_at'])

        df['date'] = df['date'].astype(str)
        df['created_at'] = df['created_at'].astype(str)
        df.to_json(backup_path, orient='records', date_format='iso')
        return backup_path

    def restore_data(self, backup_name):
        if not backup_name.endswith('.json'):
            backup_name += '.json'

        backup_path = os.path.join(self.backup_dir, backup_name)

        try:
            df = pd.read_json(backup_path, orient='records')
            self.clear_data()

            if df.empty or 'date' not in df.columns:
                return

            df['date'] = pd.to_datetime(df['date']).dt.date

            with self.engine.connect() as conn:
                for _, row in df.iterrows():
                    conn.execute(
                        text("INSERT INTO rides (date, hours, miles, earnings) VALUES (:date, :hours, :miles, :earnings)"),
                        {"date": row['date'], "hours": row['hours'], "miles": row['miles'], "earnings": row['earnings']}
                    )
                conn.commit()
        except Exception:
            self.clear_data()

    def clear_data(self):
        with self.engine.connect() as conn:
            conn.execute(text("DELETE FROM rides"))
            conn.commit()

    def get_available_backups(self):
        return [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]

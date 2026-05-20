import sqlite3
import os

db_path = r"c:\Users\keyse\Desktop\Weaver\Models\MatterEnergyScheduler\data\weaver.db"

def migrate():
    if not os.path.exists(db_path):
        print("Database file not found. SQLAlchemy will create it on startup.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Columns to add
    migrations = [
        ("households", "bidding_zone", "TEXT"),
        ("schedules", "is_daily", "BOOLEAN DEFAULT 0"),
        ("appliances", "stored_fingerprint", "TEXT"),
        ("appliances", "matter_node_id", "INTEGER"),
        ("appliances", "device_type", "TEXT DEFAULT 'generic'")
    ]

    for table, column, col_type in migrations:
        try:
            print(f"Adding column {column} to {table}...")
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
            print(f"SUCCESS: Added {column} to {table}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"INFO: Column {column} already exists in {table}")
            else:
                print(f"ERROR: adding {column} to {table}: {e}")

    conn.commit()
    conn.close()
    print("\nMigration complete. You can now start the backend.")

if __name__ == "__main__":
    migrate()

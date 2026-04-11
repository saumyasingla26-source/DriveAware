import sqlite3
from datetime import datetime

class DatabaseManager:
    """
    Advanced database for analytics & reporting
    """

    def __init__(self, db_name="drowsiness.db"):
        import os
        db_path=os.path.join(os.getcwd(),"drowsiness.db")
        print("DB created at:", db_path)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.create_tables()

        self.session_id = None
        self.start_session()

    # -------- TABLES -------- #
    def create_tables(self):

        # Detailed logs
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            date TEXT,
            time TEXT,
            ear REAL,
            status TEXT
        )
        """)

        # Session summary
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions(
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT,
            end_time TEXT,
            total_alerts INTEGER,
            avg_ear REAL
        )
        """)

        self.conn.commit()

    # -------- SESSION MANAGEMENT -------- #
    def start_session(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
        INSERT INTO sessions(start_time, end_time, total_alerts, avg_ear)
        VALUES(?, ?, ?, ?)
        """, (now, None, 0, 0))

        self.conn.commit()

        self.session_id = self.cursor.lastrowid
        print(f"Session started: {self.session_id}")

    def end_session(self, avg_ear, total_alerts):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
        UPDATE sessions
        SET end_time=?, total_alerts=?, avg_ear=?
        WHERE session_id=?
        """, (now, total_alerts, avg_ear, self.session_id))

        self.conn.commit()
        print("Session ended")

    # -------- DATA INSERT -------- #
    def insert_record(self, ear, status):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        self.cursor.execute("""
        INSERT INTO alerts(session_id,date,time,ear,status)
        VALUES(?,?,?, ?,?)
        """, (self.session_id, date, time, ear, status))

        self.conn.commit()

    # -------- ANALYTICS -------- #
    def get_total_alerts(self):
        self.cursor.execute("""
        SELECT COUNT(*) FROM alerts WHERE status='DROWSY'
        """)
        return self.cursor.fetchone()[0]

    def get_average_ear(self):
        self.cursor.execute("""
        SELECT AVG(ear) FROM alerts
        """)
        result = self.cursor.fetchone()[0]
        return round(result, 3) if result else 0

    def get_drowsy_percentage(self):
        self.cursor.execute("SELECT COUNT(*) FROM alerts")
        total = self.cursor.fetchone()[0]

        self.cursor.execute("""
        SELECT COUNT(*) FROM alerts WHERE status='DROWSY'
        """)
        drowsy = self.cursor.fetchone()[0]

        if total == 0:
            return 0

        return round((drowsy / total) * 100, 2)

    def get_last_session(self):
        self.cursor.execute("""
        SELECT * FROM sessions ORDER BY session_id DESC LIMIT 1
        """)
        return self.cursor.fetchone()

    # -------- CLEANUP -------- #
    def close(self):
        self.conn.close()
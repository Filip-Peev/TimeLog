from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import sqlite3
from datetime import datetime
import pandas as pd
import os
import re  # For worker_id validation

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages
DB_NAME = "worker_logs.db"
MIN_DELAY_SECONDS = 3  # Minimum delay between consecutive scans

# Initialize database
def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS worker_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id TEXT NOT NULL,
            arrival_time TEXT,
            leaving_time TEXT
        )
    """)
    conn.commit()
    conn.close()

# Get the last scan time for a worker
def get_last_scan_time(worker_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MAX(arrival_time), MAX(leaving_time) FROM worker_logs WHERE worker_id = ?
    """, (worker_id,))
    result = cursor.fetchone()
    conn.close()
    times = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S") for t in result if t]
    return max(times) if times else None

# Log worker arrival or leaving time securely
def log_worker(worker_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    last_scan_time = get_last_scan_time(worker_id)
    
    # Check if scanned too quickly
    if last_scan_time and (current_time - last_scan_time).total_seconds() < MIN_DELAY_SECONDS:
        conn.close()
        return False, f"Worker {worker_id} scanned too quickly. Please wait before scanning again."
    
    # Check if worker is already logged in without logging out
    cursor.execute("""
        SELECT id FROM worker_logs WHERE worker_id = ? AND leaving_time IS NULL
    """, (worker_id,))
    record = cursor.fetchone()
    
    if record:
        # Log leaving time securely
        cursor.execute("""
            UPDATE worker_logs SET leaving_time = ? WHERE id = ?
        """, (current_time_str, record[0]))
        conn.commit()
        conn.close()
        return True, f"Worker {worker_id} logged out at {current_time_str}"
    else:
        # Log arrival time securely
        cursor.execute("""
            INSERT INTO worker_logs (worker_id, arrival_time) VALUES (?, ?)
        """, (worker_id, current_time_str))
        conn.commit()
        conn.close()
        return True, f"Worker {worker_id} logged in at {current_time_str}"

# Export logs to Excel
def export_to_excel():
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT worker_id AS 'Worker ID', arrival_time AS 'Arrival Time', leaving_time AS 'Leaving Time' FROM worker_logs"
    df = pd.read_sql_query(query, conn)
    conn.close()
    if df.empty:
        return None
    file_name = f"worker_logs_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    df.to_excel(file_name, index=False, engine='openpyxl')
    return file_name

# Clear all logs
def clear_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM worker_logs")
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    query = "SELECT * FROM worker_logs"
    logs = conn.execute(query).fetchall()
    conn.close()
    return render_template('index.html', logs=logs)

@app.route('/scan', methods=['POST'])
def scan_worker():
    worker_id = request.form.get('worker_id')
    
    # Validate worker_id for alphanumeric characters only
    if not worker_id or not re.match(r'^[a-zA-Z0-9]{3,20}$', worker_id):
        flash("Worker ID must be 3-20 characters long and contain only letters and numbers.", "danger")
        return redirect(url_for('index'))
    
    success, message = log_worker(worker_id)
    flash(message, "success" if success else "warning")
    return redirect(url_for('index'))

@app.route('/export')
def export_logs():
    file_name = export_to_excel()
    if file_name:
        return send_file(file_name, as_attachment=True)
    flash("No data to export.", "warning")
    return redirect(url_for('index'))

@app.route('/clear')
def clear_all_logs():
    clear_logs()
    flash("All logs cleared.", "success")
    return redirect(url_for('index'))

# Initialize database and run app
if __name__ == "__main__":
    initialize_db()
    app.run(debug=False)

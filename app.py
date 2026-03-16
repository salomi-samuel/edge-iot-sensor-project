from flask import Flask, request, render_template_string
import psycopg2
import os
import pandas as pd

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    DATABASE_URL = "postgresql://sensordb_user:password@dpg-xxxxx:5432/sensordb_0653"

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP,
    motion INTEGER,
    distance FLOAT
)
""")

conn.commit()

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Edge IoT Sensor Dashboard</title>
<meta http-equiv="refresh" content="5">
<style>
body { font-family: Arial; text-align:center; background:#f2f2f2; }
table { margin:auto; border-collapse:collapse; margin-bottom:40px;}
th, td { padding:10px 20px; border:1px solid black; }
th { background:#333; color:white; }
</style>
</head>

<body>

<h2>Edge IoT Sensor Dashboard</h2>

<h3>Raw Sensor Data</h3>
<table>
<tr>
<th>Time</th>
<th>Motion</th>
<th>Distance</th>
</tr>
{% for row in raw %}
<tr>
<td>{{row[0]}}</td>
<td>{{row[1]}}</td>
<td>{{row[2]}}</td>
</tr>
{% endfor %}
</table>

<h3>Filtered Sensor Data (Distance < 20)</h3>
<table>
<tr>
<th>Time</th>
<th>Motion</th>
<th>Distance</th>
</tr>
{% for row in filtered %}
<tr>
<td>{{row[0]}}</td>
<td>{{row[1]}}</td>
<td>{{row[2]}}</td>
</tr>
{% endfor %}
</table>

</body>
</html>
"""

@app.route("/")
def home():

    cur.execute("SELECT time, motion, distance FROM sensor_data ORDER BY time DESC LIMIT 20")
    raw = cur.fetchall()

    cur.execute("SELECT time, motion, distance FROM sensor_data WHERE distance < 20 ORDER BY time DESC LIMIT 20")
    filtered = cur.fetchall()

    return render_template_string(HTML, raw=raw, filtered=filtered)

# API endpoint for Raspberry Pi
@app.route("/upload", methods=["POST"])
def upload():

    time = request.form["time"]
    motion = request.form["motion"]
    distance = request.form["distance"]

    cur.execute(
        "INSERT INTO sensor_data (time, motion, distance) VALUES (%s, %s, %s)",
        (time, motion, distance)
    )

    conn.commit()

    return "OK"

from flask import Flask, request, render_template_string
import psycopg2
import os
import pandas as pd

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    DATABASE_URL = "postgresql://sensordb_user:uOvPl9qWl5q7CTscURdLSQtgUr8k1wPK@dpg-d6s1n0juibrs73e2vsog-a/sensordb_0653"

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
<title>Edge IoT Analytics Dashboard</title>

<meta http-equiv="refresh" content="5">

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
font-family:Arial;
background:#0f172a;
color:white;
text-align:center;
}

h1{
margin-top:20px;
}

.container{
width:90%;
margin:auto;
}

.cards{
display:flex;
justify-content:space-around;
margin-top:20px;
}

.card{
background:#1e293b;
padding:20px;
border-radius:10px;
width:200px;
box-shadow:0px 0px 10px rgba(0,0,0,0.4);
}

.card h2{
margin:0;
}

.alert{
background:#dc2626;
padding:10px;
border-radius:6px;
margin:20px;
font-weight:bold;
}

table{
margin:auto;
border-collapse:collapse;
background:white;
color:black;
}

th,td{
padding:10px 15px;
border:1px solid #ccc;
}

th{
background:#111827;
color:white;
}

.section{
margin-top:40px;
}

canvas{
background:white;
border-radius:10px;
padding:10px;
}

</style>
</head>

<body>

<h1>Edge IoT Analytics Dashboard</h1>

<div class="container">

<div class="cards">

<div class="card">
<h2>{{total}}</h2>
<p>Total Readings</p>
</div>

<div class="card">
<h2>{{events}}</h2>
<p>Filtered Events (&lt;20cm)</p>
</div>

<div class="card">
<h2>{{reduction}}%</h2>
<p>Edge Data Reduction</p>
</div>

</div>

{% if alert %}
<div class="alert">
⚠️ Object Detected: {{alert}} cm
</div>
{% endif %}

<div class="section">

<h2>Distance Trend</h2>

<canvas id="chart" width="800" height="300"></canvas>

</div>

<div class="section">

<h2>Recent Sensor Readings</h2>

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

</div>

</div>

<script>

const ctx = document.getElementById('chart');

new Chart(ctx,{
type:'line',
data:{
labels: {{times|safe}},
datasets:[{
label:'Distance (cm)',
data: {{distances|safe}},
borderColor:'red',
fill:false,
tension:0.2
}]
},
options:{
responsive:true
}
});

</script>

</body>
</html>
"""

@app.route("/")
def home():

    cur.execute("SELECT time, motion, distance FROM sensor_data ORDER BY time DESC LIMIT 20")
    raw = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM sensor_data")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sensor_data WHERE distance < 20")
    events = cur.fetchone()[0]

    reduction = 0
    if total > 0:
        reduction = round((events / total) * 100, 2)

    cur.execute("SELECT time, distance FROM sensor_data ORDER BY time DESC LIMIT 20")
    rows = cur.fetchall()

    times = [str(r[0]) for r in rows][::-1]
    distances = [r[1] for r in rows][::-1]

    alert = None
    if rows and rows[0][1] < 20:
        alert = rows[0][1]

    return render_template_string(
        HTML,
        raw=raw,
        total=total,
        events=events,
        reduction=reduction,
        times=times,
        distances=distances,
        alert=alert
    )

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
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

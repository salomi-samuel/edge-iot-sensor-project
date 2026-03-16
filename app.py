from flask import Flask, request, render_template_string
import psycopg2
import os

app = Flask(__name__)

# DATABASE CONNECTION
DATABASE_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# CREATE TABLE IF NOT EXISTS
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

<title>Smart Proximity Monitoring System</title>
<p>
Edge Device: Raspberry Pi |
Cloud API: Flask |
Database: PostgreSQL |
Deployment: Render Cloud
</p>
<meta http-equiv="refresh" content="5">

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>

body{
font-family: Arial;
background:#0f172a;
color:white;
text-align:center;
}

h1{
color:#38bdf8;
}

.tabs{
margin-top:20px;
}

button{
padding:10px 20px;
margin:5px;
border:none;
background:#38bdf8;
color:black;
font-weight:bold;
cursor:pointer;
}

.section{
display:none;
padding:20px;
}

table{
margin:auto;
border-collapse:collapse;
background:white;
color:black;
}

th,td{
padding:8px 15px;
border:1px solid black;
}

.card{
display:inline-block;
background:#1e293b;
padding:20px;
margin:10px;
border-radius:10px;
}

</style>

<script>

function showTab(tab){

localStorage.setItem("activeTab", tab)

document.getElementById("dashboard").style.display="none"
document.getElementById("raw").style.display="none"
document.getElementById("filtered").style.display="none"
document.getElementById("analytics").style.display="none"

document.getElementById(tab).style.display="block"

}

window.onload = function(){

var tab = localStorage.getItem("activeTab")

if(tab){
showTab(tab)
}else{
showTab("dashboard")
}

}

</script>

</head>

<body>

<h1>Smart Proximity Monitoring System</h1>
<h3>Edge‑Assisted Serverless IoT Analytics</h3>

<div class="tabs">

<button onclick="showTab('dashboard')">Dashboard</button>
<button onclick="showTab('raw')">Raw Data</button>
<button onclick="showTab('filtered')">Filtered Events</button>
<button onclick="showTab('analytics')">Analytics</button>

</div>

<!-- DASHBOARD -->

<div id="dashboard" class="section" style="display:block">

<div class="card">
<h2>Total Readings</h2>
<h1>{{total}}</h1>
<p>Raw sensor readings generated</p>
</div>

<div class="card">
<h2>Filtered Events</h2>
<h1>{{filtered_count}}</h1>
<p>Events sent to cloud</p>
</div>

<div class="card">
<h2>Edge Reduction</h2>
<h1>{{reduction}} %</h1>
<p>Data reduced at edge device</p>
</div>

<div class="card">
<h2>System</h2>
<p>Edge Device: Raspberry Pi</p>
<p>Database: PostgreSQL</p>
<p>Server: Flask API</p>
<p>Cloud: Render</p>
</div>

<p>
Edge Processing filters unnecessary sensor readings before sending to the cloud.
This reduces network usage and improves sustainability in IoT systems.
</p>

<h2>Distance Trend</h2>

<canvas id="distanceChart" width="600" height="250"></canvas>

<script>

var ctx = document.getElementById('distanceChart')

new Chart(ctx, {
type: 'line',
data: {
labels: {{labels}},
datasets: [{
label: 'Distance (cm)',
data: {{distances}},
borderColor: 'cyan',
fill:false
}]
}
})

</script>

</div>

<!-- RAW DATA -->

<div id="raw" class="section">

<h2>Raw Sensor Data</h2>

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

<!-- FILTERED DATA -->

<div id="filtered" class="section">

<h2>Filtered Events (Distance < 20 cm)</h2>

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

</div>

<!-- ANALYTICS -->

<div id="analytics" class="section">

<h2>System Analytics</h2>

<p>Average Distance: {{avg}}</p>
<p>Minimum Distance: {{min}}</p>
<p>Maximum Distance: {{max}}</p>

</div>

</body>
</html>
"""

@app.route("/")
def home():

    cur.execute("SELECT time,motion,distance FROM sensor_data ORDER BY time DESC LIMIT 50")
    raw = cur.fetchall()

    cur.execute("SELECT time,motion,distance FROM sensor_data WHERE distance<20 ORDER BY time DESC LIMIT 20")
    filtered = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM sensor_data")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM sensor_data WHERE distance<20")
    filtered_count = cur.fetchone()[0]

    if total > 0:
        reduction = round((1-(filtered_count/total))*100,2)
    else:
        reduction = 0

    cur.execute("SELECT AVG(distance),MIN(distance),MAX(distance) FROM sensor_data")
    avg,minv,maxv = cur.fetchone()

    labels = [str(r[0]) for r in raw[::-1]]
    distances = [r[2] for r in raw[::-1]]

    return render_template_string(
        HTML,
        raw=raw,
        filtered=filtered,
        total=total,
        filtered_count=filtered_count,
        reduction=reduction,
        avg=avg,
        min=minv,
        max=maxv,
        labels=labels,
        distances=distances
    )

@app.route("/upload",methods=["POST"])
def upload():

    time = request.form["time"]
    motion = request.form["motion"]
    distance = request.form["distance"]

    cur.execute(
    "INSERT INTO sensor_data(time,motion,distance) VALUES(%s,%s,%s)",
    (time,motion,distance)
    )

    conn.commit()

    return "OK"

app.run(host="0.0.0.0",port=10000)

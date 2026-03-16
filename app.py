from flask import Flask, request, render_template_string
import pandas as pd
import csv

app = Flask(__name__)

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

    try:
        raw = pd.read_csv("raw_sensor_data.csv", header=None).tail(20).values.tolist()
    except:
        raw = []

    try:
        filtered = pd.read_csv("filtered_sensor_data.csv", header=None).tail(20).values.tolist()
    except:
        filtered = []

    return render_template_string(HTML, raw=raw, filtered=filtered)


# API endpoint for Raspberry Pi
@app.route("/upload", methods=["POST"])
def upload():

    time = request.form["time"]
    motion = request.form["motion"]
    distance = request.form["distance"]

    with open("raw_sensor_data.csv","a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time,motion,distance])

    if float(distance) < 20:
        with open("filtered_sensor_data.csv","a",newline="") as f:
            writer = csv.writer(f)
            writer.writerow([time,motion,distance])

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

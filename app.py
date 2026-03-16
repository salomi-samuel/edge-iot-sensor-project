from flask import Flask, render_template_string
import pandas as pd

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
h2 {color:#333;}
</style>
</head>

<body>

<h2>Edge IoT Sensor Dashboard</h2>

<h3>All Sensor Readings (Raw Data)</h3>
<table>
<tr>
<th>Time</th>
<th>Motion</th>
<th>Distance (cm)</th>
</tr>

{% for row in raw %}
<tr>
<td>{{row[0]}}</td>
<td>{{row[1]}}</td>
<td>{{row[2]}}</td>
</tr>
{% endfor %}

</table>


<h3>Filtered Sensor Readings (Edge Filtered: Distance &lt; 20 cm)</h3>

<table>
<tr>
<th>Time</th>
<th>Motion</th>
<th>Distance (cm)</th>
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
        raw_df = pd.read_csv("raw_sensor_data.csv", header=None)
        raw_data = raw_df.tail(20).values.tolist()
    except:
        raw_data = []

    try:
        filtered_df = pd.read_csv("filtered_sensor_data.csv", header=None)
        filtered_data = filtered_df.tail(20).values.tolist()
    except:
        filtered_data = []

    return render_template_string(HTML, raw=raw_data, filtered=filtered_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

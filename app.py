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
table { margin:auto; border-collapse:collapse; }
th, td { padding:10px 20px; border:1px solid black; }
th { background:#333; color:white; }
</style>
</head>

<body>
<h2>Edge IoT Sensor Dashboard</h2>

<table>
<tr>
<th>Time</th>
<th>Motion</th>
<th>Distance (cm)</th>
</tr>

{% for row in data %}
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
        df = pd.read_csv("sensor_data.csv", header=None)
        data = df.tail(20).values.tolist()
    except:
        data = []
    return render_template_string(HTML, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, redirect, render_template
import os
import requests
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/logs/", defaults={"log": ""})
@app.route("/logs/<path:log>")
def logs(log):
    BASE_URL = os.environ["API_URL"]
    if log == "":
        r = requests.get(BASE_URL + "/logs/")
        if r.status_code != 200:
            return "<h1>ERROR</h1>", 500
        entries = r.json()
        return render_template("logs.html", entries=entries)
    else:
        r = requests.get(BASE_URL + "/logs/" + log)
        return render_template("log_view.html", log_data=r.text.split("\n"))



@app.route("/reports/", defaults={"report": ""})
@app.route("/reports/<path:report>")
def reports(report):
    BASE_URL = os.environ["API_URL"]
    if report == "":
        r = requests.get(BASE_URL + "/reports/")
        if r.status_code != 200:
            return r.text, 500
        entries = r.json()
        entries = format_data(entries)
        return render_template("reports.html", entries=entries)
    r = requests.get(BASE_URL + "/reports/" + str(report))
    return render_template("report_view.html", entry=r.json())

@app.route("/view/<report>/")
def render_report(report):
    STATIC_SERVER = os.environ["NGINX_URL"].rstrip("/")
    full_path = STATIC_SERVER + "/" + "daily_BY" + "/" + report + "/report.html" 
    return redirect(full_path, 301)


def format_data(entries):
    result = []
    for entry in entries:
        entry["test_id"] = entry["test_day"]
        entry["test_day"] = str(entry["test_day"])
        entry["test_day"] = '-'.join(entry["test_day"][i:i+2] for i in range(0, len(entry["test_day"]), 2)).split("-")
        entry["test_day"][0] = "20" + entry["test_day"][0]
        entry["test_day"].reverse()
        entry["test_day"] = "-".join(entry["test_day"])
        result.append(entry)
    return result

app.run("0.0.0.0", port=5001)
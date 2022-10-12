from flask import Flask, redirect, render_template, request
import os
import requests
from dotenv import load_dotenv

if os.path.exists(".env"):
    load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    print(request.headers)
    BASE_URL = os.environ["API_URL"]
    daily_BY = requests.get(BASE_URL + "/reports/daily_BY/today")
    daily_BW = requests.get(BASE_URL + "/reports/daily_BW/today")
    is_today_daily_BY = True
    is_today_daily_BW = True
    is_today_release_BW = True
    is_today_release_BY = True
    if daily_BY.status_code == 404:
        daily_BY = requests.get(BASE_URL + "/reports/daily_BY/latest")
        is_today_daily_BY = False
    if daily_BW.status_code == 404:
        daily_BW = requests.get(BASE_URL + "/reports/daily_BW/latest")
        is_today_daily_BW = False
    if daily_BW.status_code == 404:
        daily_BW = requests.get(BASE_URL + "/reports/release_BY/latest")
        is_today_release_BY = False
    if daily_BW.status_code == 404:
        daily_BW = requests.get(BASE_URL + "/reports/release_BW/latest")
        is_today_release_BW = False
    # a bit of a workaround so format_data() can work for this response as well as for /reports/<version>
    daily_BY = format_data([daily_BY.json()])[0]
    daily_BW = format_data([daily_BW.json()])[0]
    release_BY = format_data([release_BY.json()])[0]
    release_BW = format_data([release_BW.json()])[0]
    return render_template("index.html", daily_BY=daily_BY, daily_BW=daily_BW, release_BW=release_BW, release_BY=release_BY, 
                                        is_today_BY=is_today_daily_BY, is_today_BW=is_today_daily_BW,
                                        is_today_release_BY=is_today_release_BY, is_today_release_BW=is_today_release_BW)


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



@app.route("/reports/<version>/", defaults={"report": ""})
@app.route("/reports/<version>/<path:report>")
def reports(version, report):
    BASE_URL = os.environ["API_URL"]
    if report == "":
        r = requests.get(BASE_URL + "/reports/" + version)
        print(BASE_URL + "/reports/" + version)
        if r.status_code != 200:
            return r.text, 500
        entries = r.json()
        entries = format_data(entries)
        return render_template("reports.html", entries=entries, version=version)
    r = requests.get(BASE_URL + "/reports/" + version + "/" + str(report))
    nginx = os.environ["CURRENT_IP"] + ":" + os.environ["NGINX_PORT"]
    return render_template("report_view.html", entry=r.json(), nginx=nginx, distribution=version)



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
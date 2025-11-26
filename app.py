from flask import Flask, render_template, request
import requests
from flask import Flask, render_template, request
app = Flask(__name__, static_folder='static', template_folder='templates')

app = Flask(__name__)

API_KEY = "0f2d1870346e5e2724a04ae02b42318c7c5b25c3"   # Your API KEY

def get_aqi(city):
    url = f"https://api.waqi.info/feed/{city}/?token={API_KEY}"
    response = requests.get(url).json()

    try:
        data = response["data"]
        return {
            "city": city.capitalize(),
            "aqi": data.get("aqi", "N/A"),
            "pm25": data.get("iaqi", {}).get("pm25", {}).get("v", "N/A"),
            "pm10": data.get("iaqi", {}).get("pm10", {}).get("v", "N/A"),
            "temp": data.get("iaqi", {}).get("t", {}).get("v", "N/A"),
            "humidity": data.get("iaqi", {}).get("h", {}).get("v", "N/A")
        }
    except:
        return {
            "city": city.capitalize(),
            "aqi": "N/A",
            "pm25": "N/A",
            "pm10": "N/A",
            "temp": "N/A",
            "humidity": "N/A"
        }


@app.route("/", methods=["GET", "POST"])
def index():
    city = "Hyderabad"  # default city

    if request.method == "POST":
        city = request.form.get("city").strip()

    aqi_data = get_aqi(city)
    return render_template("index.html", data=aqi_data)

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/architecture")
def architecture():
    return render_template("architecture.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/demo", methods=["GET","POST"])
def demo():
    data = None
    if request.method == "POST":
        city = request.form.get("city")
        data = get_aqi(city)
    return render_template("demo.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

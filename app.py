import requests
import json
from flask import Flask, render_template, request

app = Flask(__name__)


# Instead of directly giving API key we use a fucntion and get the API key from the config.json file
def get_api_key():
    with open('config.json') as config_file:
        data = json.load(config_file)
        return data["api"]

# TO get the weather data from the API in JSON format


def get_weather_data(zip_code, api_key):
    # api_url = https://api.openweathermap.org/data/2.5/weather?zip={},IN&units=metric&appid={}
    api_url = f'https://api.openweathermap.org/data/2.5/weather?zip={zip_code},IN&units=metric&appid={api_key}'
    success_code = requests.get(api_url)
    return success_code.json()

# get_weather_data("500053",get_api_key())


@app.route('/')
def weather_dashboard():
    return render_template('index.html')


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']
    api_key = get_api_key()
    data = get_weather_data(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    pressure = data["main"]["pressure"]
    humidity = data["main"]['humidity']
    wind_speed = data["wind"]["speed"]

    return render_template('results.html', location=location, weather=weather, temp=temp,\
         feels_like=feels_like, pressure = pressure, humidity = humidity, wind_speed = wind_speed)


if __name__ == "__main__":
    app.run(debug=True)

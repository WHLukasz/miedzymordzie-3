from __future__ import unicode_literals
# coding: utf-8
# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request, current_app
from pathlib import Path
from utils.weather import get_forecast, download_weather_icon, get_weather, get_forecast
from flask import send_from_directory
import logging

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/static/weather_icons/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.root_path + '/static/weather_icons', filename)

@app.template_filter('file_exist')
def file_exist(file_path):
    return Path(file_path).is_file()

def generate_footer():
    return render_template('footer.html')

@app.route('/')
def home():
    return render_template('index.html', footer=generate_footer())

@app.route('/browse_interfaces', methods=['GET', 'POST'])
def browse_interfaces():
    icon_path = None
    theme = request.args.get('theme', 'light')
    detail = request.args.get('detail', 'basic')
    display_format_option_value = request.args.get('display_format_option_value', 'text')

    if request.method == 'POST':
        theme = request.form.get('theme', 'light')
        detail = request.form.get('detail', 'basic')
        display_format_option_value = request.form.get('display_format_option_value', 'text')

    city = "Wroclaw"
    weather_data = get_weather(city)

    # Pobierz ikone i zapisz ja lokalnie
    if weather_data.get('weather'):
        weather_icon = weather_data['weather'][0]['icon']
        print(f"Downloading weather Icon: {weather_icon}")
        download_weather_icon(current_app, weather_icon)
        icon_path = f"/static/weather_icons/{weather_icon}.png"

    print(f"display_format_option_value inside browse_interfaces: {display_format_option_value}")

    print(f"Icon path inside browse_interfaces: {icon_path}")
          
    forecast_data = get_forecast(city)

    print("Forecast Data Type:", type(forecast_data))

    if forecast_data:
        print("Processing forecast:", forecast_data.get('dt_txt', 'Unknown'))

    return render_template(
        'browse_interfaces.html',
        theme=theme,
        detail=detail,
        display_format_option_value=display_format_option_value,
        weather_data=weather_data,
        icon_path=icon_path,
        forecast_data=forecast_data,
        footer=generate_footer()
    )

def file_exists_case_sensitive(file_path):
    return os.path.exists(file_path)

app.jinja_env.filters['file_exists_case_sensitive'] = file_exists_case_sensitive


@app.route('/survey')
def survey():
    return render_template('survey.html', footer=generate_footer())

app.logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app.run(debug=True)

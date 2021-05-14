from django.shortcuts import render
import numpy as np
import pandas as pd
from . import disease
from . import fertilizer 
import requests
import config
import pickle
import io




crop_recommendation_model_path = 'E:/VCODE/HTML_LEVEL_ONE/DJANGO_COURSE_2.xx/aiml/agricos/mod/RandomForest.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))


def weather_fetch(city_name):
    """
    Fetch and returns the temperature and humidity of a city
    :params: city_name
    :return: temperature, humidity
    """
    api_key = "a9f80553551d7000a5a7fc1dfca3ed85"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None




# Create your views here.
def index(request):
    return render(request,"agricos/index.html")

def crop_recommend(request):
    if request.method == "POST":
        N = int(request.POST['nitrogen'])
        P = int(request.POST['phosphorous'])
        K = int(request.POST['pottasium'])
        ph = float(request.POST['ph'])
        rainfall = float(request.POST['rainfall'])

        # state = request.form.get("stt")
        city = request.POST.get("city")

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]

            return render(request,'agricos/crop-result.html', {'prediction': final_prediction })

        else:

            return render(request,'agricos/try_again.html')

    else:
        return render(request,'agricos/crop.html')

def fertilizer_recommend(request):
    if request.method == "POST":
        crop_name = str(request.POST['cropname'])
        N = int(request.POST['nitrogen'])
        P = int(request.POST['phosphorous'])
        K = int(request.POST['pottasium'])
        # ph = float(request.form['ph'])

        df = pd.read_csv('E:/VCODE/HTML_LEVEL_ONE/DJANGO_COURSE_2.xx/aiml/agricos/Data/fertilizer.csv')

        nr = df[df['Crop'] == crop_name]['N'].iloc[0]
        pr = df[df['Crop'] == crop_name]['P'].iloc[0]
        kr = df[df['Crop'] == crop_name]['K'].iloc[0]

        n = nr - N
        p = pr - P
        k = kr - K
        temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
        max_value = temp[max(temp.keys())]
        if max_value == "N":
            if n < 0:
                key = 'NHigh'
            else:
                key = "Nlow"
        elif max_value == "P":
            if p < 0:
                key = 'PHigh'
            else:
                key = "Plow"
        else:
            if k < 0:
                key = 'KHigh'
            else:
                key = "Klow"

        response = str(fertilizer.fertilizer_dic[key])

        return render(request,'agricos/fertilizer-result.html', {'recommendation':response})
    else:
        return render(request,'agricos/fertilizer.html')
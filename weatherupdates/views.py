# views.py
from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
from datetime import datetime
from .models import Weatherupdates

def index(request):
    if request.method == 'POST':
        try:
            API_KEY = os.getenv('WEATHER_API_KEY')
            city_name = request.POST.get('city')

            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
            response = requests.get(url).json()

            if response['cod'] == 200:  # Check if API call was successful
                current_time = datetime.now().strftime("%A, %B %d %Y, %I:%M %p")

                city_weather_update = {
                    'city': city_name,
                    'description': response['weather'][0]['description'],
                    'icon': response['weather'][0]['icon'],
                    'temperature': f"Temperature: {response['main']['temp']} °C",
                    'country_code': response['sys']['country'],
                    'wind': f"Wind: {response['wind']['speed']} km/h",
                    'humidity': f"Humidity: {response['main']['humidity']}%",
                    'time': current_time
                }

                # Write to database
                Weatherupdates.objects.create(
                    city=city_name,
                    description=response['weather'][0]['description'],
                    temperature=response['main']['temp'],
                    wind=response['wind']['speed'],
                    humidity=response['main']['humidity']
                )
                

                context = {'city_weather_update': city_weather_update}
                return render(request, 'weatherupdates/home.html', context)
            else:
                context = {'error': f"Error: {response['message']}"}
                return render(request, 'weatherupdates/home.html', context)
        
        except requests.exceptions.RequestException as e:
            context = {'error': f"Error: {e}"}
            return render(request, 'weatherupdates/home.html', context)
        
        except KeyError as e:
            context = {'error': f"Error: {e}"}
            return render(request, 'weatherupdates/home.html', context)
        
        except Exception as e:
            context = {'error': f"Error: {e}"}
            return render(request, 'weatherupdates/404.html', context)

    else:
        return render(request, 'weatherupdates/home.html')

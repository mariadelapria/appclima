import requests
import os
API_key = os.getenv("OPENWEATHER_API_KEY")


def clima_atual(cidade):  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_key}&units=metric&lang=pt_br"
    res = requests.get(url).json()

    if res.get("cod") != 200:
        print("Cidade não encontrada!")
        return None  
    else:
      temp = res['main']['temp']
      desc = res['weather'][0]['description']
      vento = res['wind']['speed']
      lat = res['coord']['lat']
      lon = res['coord']['lon']
      vento_kmh = vento * 3.6


    if res['weather'][0]['main'].lower() == "rain":
        chuva_mm = res.get('rain', {}).get('1h', 0)
        desc = f"chuva ({chuva_mm} mm nas últimas 1h)"

    return cidade, temp, vento_kmh, desc, lat, lon


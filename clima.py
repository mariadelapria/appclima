import requests

def clima_atual(cidade, api_key):  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"
    res = requests.get(url).json()

    if res.get("cod") != 200:
        print("Cidade não encontrada!")
        return None  
    else:
        main = res.get('main', {})
        weather = res.get('weather', [{}])[0]
        wind = res.get('wind', {})
        coord = res.get('coord', {})

        temp = main.get('temp', 0)
        desc = weather.get('description', '–')
        vento = wind.get('speed', 0)
        lat = coord.get('lat', 0)
        lon = coord.get('lon', 0)
        vento_kmh = vento * 3.6

    if weather.get('main', '').lower() == "rain":
        chuva_mm = res.get('rain', {}).get('1h', 0)
        desc = f"chuva ({chuva_mm} mm nas últimas 1h)"

    return cidade, temp, vento_kmh, desc, lat, lon


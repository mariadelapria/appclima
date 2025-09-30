import requests
import time 
import os
API_key = os.getenv("OPENWEATHER_API_KEY")

def previsao_5dias(cidade):
    url_5dias = f"http://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={API_key}&units=metric&lang=pt_br"
    res_5dias = requests.get(url_5dias).json()

    if res_5dias.get("cod") != "200":
        print("Não foi possível obter a previsão!")
        return None

    previsoes = {}
    for item in res_5dias['list']:
        data = item['dt_txt'].split(" ")[0]
        temp = item['main']['temp']
        desc = item['weather'][0]['description']

        if data not in previsoes:
            previsoes[data] = {"temp_min": temp, "temp_max": temp, "desc": desc}
        else:
            previsoes[data]['temp_min'] = min(previsoes[data]['temp_min'], temp)
            previsoes[data]['temp_max'] = max(previsoes[data]['temp_max'], temp)

    # Mantém os prints originais
    print(f"\n Previsão de 5 dias para {cidade}:\n")
    print(f"{'Data':<12} | {'Descrição':<15} | {'Temp Mín':<8} | {'Temp Máx':<8}")
    print("-"*50)
    dias = list(previsoes.keys())[:5]
    for dia in dias:
        info = previsoes[dia]
        print(f"{dia:<12} | {info['desc']:<15} | {info['temp_min']:<8.1f} | {info['temp_max']:<8.1f}")
    
   
    return previsoes

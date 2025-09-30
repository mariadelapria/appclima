import requests
import time

def previsao_5dias(cidade, api_key):
    url_5dias = f"http://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={api_key}&units=metric&lang=pt_br"
    res_5dias = requests.get(url_5dias).json()

    if res_5dias.get("cod") != "200":
        print("Não foi possível obter a previsão!")
        return None

    previsoes = {}
    for item in res_5dias.get('list', []):
        data = item.get('dt_txt', '0000-00-00').split(" ")[0]
        main = item.get('main', {})
        weather = item.get('weather', [{}])[0]

        temp = main.get('temp', 0)
        desc = weather.get('description', '–')

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

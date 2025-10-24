import requests
def weather_get(city):
    response = requests.get(f"https://ipinfo.io/{city}")
    if response.status_code == 200 :
        return response.json()
    else:
        raise ValueError("could not find")
print(weather_get("json"))
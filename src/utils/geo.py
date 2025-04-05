import requests

def reverse_geocode(lat, lon):
    try:
        url = f"https://nominatim.openstreetmap.org/reverse"
        params = {
            "format": "jsonv2",
            "lat": lat,
            "lon": lon,
            "zoom": 10,
            "addressdetails": 1,
        }
        headers = {"User-Agent": "orienting_project"}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        address = data.get("address", {})
        country = address.get("country", None)
        state = address.get("state", None)
        region = address.get("region", None)
        city = address.get("city", None)

            # Возвращаем информацию
        return {
            "country": country,
            "state": state,
            "region": region,
            "city": city
        }
            
    except requests.RequestException as e:
        return {"error": str(e)}
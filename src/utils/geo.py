import requests
from fastapi import HTTPException

from config.logger import api_error_logger, api_logger

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
        headers = {
            "User-Agent": "orienting_project",
            "Accept-Language": "ru"
        }
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        address = data.get("address", {})
        country = address.get("country", None)
        region = address.get("region", None)
        city = address.get("city", None)

        # Возвращаем информацию
        return {
            "country": country,
            "region": region,
            "city": city,
            "latitude": lat,
            "longitude": lon
        }
            
    except requests.RequestException as e:
        api_error_logger.error(f"OSM error - {e}")
        raise HTTPException(status_code=500, detail=f"Error with OpenStreetMap API: {e}")
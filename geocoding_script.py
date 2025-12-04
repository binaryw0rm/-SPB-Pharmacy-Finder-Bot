import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

def geocode_missing_data(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    
    geolocator = Nominatim(user_agent="spb_pharmacy_bot_v1")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    print("Начинаем геокодинг отсутствующих координат...")

    for index, row in df.iterrows():
        # Если координат нет (NaN или пустые)
        if pd.isna(row['lat']) or pd.isna(row['lon']):
            address = f"Санкт-Петербург, {row['address']}"
            try:
                location = geocode(address)
                if location:
                    df.at[index, 'lat'] = location.latitude
                    df.at[index, 'lon'] = location.longitude
                    print(f"Найдено для {row['name']}: {location.latitude}, {location.longitude}")
                else:
                    print(f"Не удалось найти: {address}")
            except Exception as e:
                print(f"Ошибка геокодинга {address}: {e}")
            
    df.to_csv(output_csv, index=False)
    print(f"Готово. Сохранено в {output_csv}")

if __name__ == "__main__":
    # Создайте исходный файл data/raw_pharmacies.csv
    # Результат будет в data/pharmacies.csv
    geocode_missing_data("data/raw_pharmacies.csv", "data/pharmacies.csv")
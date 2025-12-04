import pandas as pd
import logging
import os
from src.config import CSV_PATH
from src.utils import calculate_distance

class PharmacyRepo:
    def __init__(self):
        self.data = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(CSV_PATH):
            logging.warning("CSV файл не найден, создаем пустой список.")
            self.data = []
            return

        try:
            # Читаем CSV
            df = pd.read_csv(CSV_PATH, sep=None, engine='python')
            # Заполняем пустые значения (NaN) пустыми строками, чтобы не ломать логику
            df = df.fillna("")
            self.data = df.to_dict('records')
            logging.info(f"Загружено {len(self.data)} аптек.")
        except Exception as e:
            logging.error(f"Ошибка загрузки CSV: {e}")
            self.data = []

    def save_data(self):
        """Сохраняет текущий список self.data обратно в CSV."""
        try:
            if not self.data:
                return
            
            df = pd.DataFrame(self.data)
            # Сохраняем с кавычками для всех текстовых полей, чтобы запятые в адресе не ломали файл
            df.to_csv(CSV_PATH, index=False, quoting=1) # quoting=1 это quote_all (кавычки везде)
            logging.info("Данные успешно сохранены в CSV.")
        except Exception as e:
            logging.error(f"Ошибка сохранения CSV: {e}")

    def add_pharmacy(self, pharm_data):
        """Добавляет новую аптеку и сохраняет файл.
        pharm_data = {name, address, district, ...}
        """
        # Генерируем новый ID (максимальный + 1)
        if self.data:
            try:
                max_id = max(int(p['id']) for p in self.data if str(p['id']).isdigit())
            except:
                max_id = 0
            new_id = max_id + 1
        else:
            new_id = 1
        
        pharm_data['id'] = new_id
        self.data.append(pharm_data)
        self.save_data()
        return new_id

    def delete_pharmacy(self, pharm_id):
        """Удаляет аптеку по ID."""
        initial_len = len(self.data)
        self.data = [p for p in self.data if str(p['id']) != str(pharm_id)]
        
        if len(self.data) < initial_len:
            self.save_data()
            return True
        return False

    # ... (методы find_nearest, get_by_district, get_by_id остаются без изменений) ...
    def find_nearest(self, user_lat, user_lon, only_24h=True):
        if not self.data: return None
        nearest = None
        min_dist = float('inf')
        for pharm in self.data:
            if only_24h and str(pharm.get('is_24h', '')).lower() not in ['true', '1', 'yes', 'да']:
                continue
            try:
                # Проверка на пустые координаты
                if not pharm['lat'] or not pharm['lon']: continue
                
                p_lat = float(pharm['lat'])
                p_lon = float(pharm['lon'])
                dist = calculate_distance(user_lat, user_lon, p_lat, p_lon)
                if dist < min_dist:
                    min_dist = dist
                    nearest = pharm.copy() # Возвращаем копию, чтобы не менять оригинал
                    nearest['distance_km'] = round(dist, 2)
            except (ValueError, TypeError):
                continue
        return nearest

    def get_by_district(self, district_name, only_24h=True):
        result = []
        for pharm in self.data:
            if only_24h and str(pharm.get('is_24h', '')).lower() not in ['true', '1', 'yes', 'да']:
                continue
            if district_name.lower() in str(pharm.get('district', '')).lower():
                result.append(pharm)
        return result

    def get_by_id(self, pharm_id):
        for pharm in self.data:
            if str(pharm.get('id')) == str(pharm_id):
                return pharm
        return None

repo = PharmacyRepo()
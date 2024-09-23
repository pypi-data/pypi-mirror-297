# my_hisse_api/my_hisse_api.py

import requests
import pandas as pd

def hisse_verisi(hisse_adi, base_url='https://borsaapi-436410.uc.r.appspot.com'):
    """
    Google App Engine üzerindeki API'den belirtilen hisse adına göre veri çeker.
    
    Parameters:
    - hisse_adi (str): Hisse senedi adı (örneğin, 'THYAO')
    - base_url (str): API'nin temel URL'si (varsayılan olarak verilir)
    
    Returns:
    - pd.DataFrame: API'den gelen verileri içeren Pandas DataFrame
    """
    url = f'{base_url}/get_data_by_hisse/{hisse_adi}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        return df
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Hatası: {http_err}")
    except Exception as err:
        print(f"Başka bir hata oluştu: {err}")
    return pd.DataFrame()

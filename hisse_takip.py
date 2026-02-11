import yfinance as yf
import requests
import os

# --- AYARLAR ---
NTFY_TOPIC = "Hisse" # Uygulamadaki ismin birebir aynisi olmali

hisseler = {
    "NVDA": (0, 175),
    "AMD": (0, 210),
    "UBER": (0, 70),
    "CRWV": (0, 75),
    "JOBY": (0, 8.5),
    "QBTS": (0, 16)
}

def mesaj_gonder(mesaj):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        requests.post(url, 
                      data=mesaj.encode('utf-8'), 
                      headers={
                          "Title": "Hisse Hedef Fiyat Uyarisi", # Turkce karakter icermemeli
                          "Priority": "high",
                          "Tags": "moneybag,chart_with_upwards_trend"
                      }, 
                      timeout=10)
        print("Bildirim telefona gonderildi.")
    except Exception as e:
        print(f"Bildirim hatasi: {e}")

def kontrol_et():
    rapor = ""
    firsat_var_mi = False
    
    for sembol, (dusuk, yuksek) in hisseler.items():
        try:
            hisse = yf.Ticker(sembol)
            data = hisse.history(period="1d")
            if data.empty:
                continue
            
            fiyat = data['Close'].iloc[-1]
            
            # --- GERCEK KONTROL ---
            if dusuk <= fiyat <= yuksek:
                rapor += f"🚨 {sembol}: ${fiyat:.2f} - ALIM NOKTASINDA!\n"
                firsat_var_mi = True
                
        except Exception as e:
            print(f"{sembol} hatasi: {e}")
    
    if firsat_var_mi:
        mesaj_gonder(f"Hisse Alim Firsati!\n\n{rapor}")
    else:
        print("Hedef fiyata ulasan hisse yok, bildirim gonderilmedi.")

if __name__ == "__main__":
    if NTFY_TOPIC:
        kontrol_et()

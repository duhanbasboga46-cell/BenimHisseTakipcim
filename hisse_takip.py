import yfinance as yf
import requests
import os

# --- AYARLAR ---
# GitHub Secrets üzerinden alınacak
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 0 ile senin belirlediğin üst limit arasındaki aralıklar
hisseler = {
    "NVDA": (0, 188),
    "AMD": (0, 210),
    "UBER": (0, 70),
    "CRWV": (0, 75),
    "JOBY": (0, 8.5),
    "QBTS": (0, 16)
}

def mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Mesaj gönderme hatası: {e}")

def kontrol_et():
    rapor = ""
    firsat_var_mi = False
    
    for sembol, (dusuk, yuksek) in hisseler.items():
        try:
            hisse = yf.Ticker(sembol)
            # En son kapanış fiyatını alıyoruz
            data = hisse.history(period="1d")
            if data.empty:
                continue
                
            fiyat = data['Close'].iloc[-1]
            
            # Fiyat 0 ile senin belirlediğin üst limit arasındaysa (Yani alım noktasındaysa)
            if dusuk <= fiyat <= yuksek:
                rapor += f"🚨 {sembol}: ${fiyat:.2f} - ALIM NOKTASINDA (Hedef: ${yuksek} altı)\n"
                firsat_var_mi = True
        except Exception as e:
            print(f"{sembol} verisi çekilirken hata oluştu: {e}")
    
    if firsat_var_mi:
        mesaj_gonder(f"📈 HEDEF FİYAT UYARISI!\n\n{rapor}")
    else:
        print("Şu an alım noktasında olan bir hisse yok.")

if __name__ == "__main__":
    if TOKEN and CHAT_ID:
        kontrol_et()
    else:
        print("Hata: GitHub Secrets üzerinden TELEGRAM_TOKEN veya TELEGRAM_CHAT_ID tanımlanmamış!")
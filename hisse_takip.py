import yfinance as yf
import requests
import os

# --- AYARLAR ---
# GitHub Secrets üzerinden alınacak
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
NTFY_TOPIC = "Duhan_Borsa_Takip" # Uygulamada belirlediğin ismin aynısı olmalı

# 0 ile senin belirlediğin üst limit arasındaki aralıklar
hisseler = {
    "NVDA": (0, 188),
    "AMD": (0, 210),
    "UBER": (0, 70),
    "CRWV": (0, 75),
    "JOBY": (0, 10.5),
    "QBTS": (0, 20)
}

def mesaj_gonder(mesaj):
    # 1. Telegram Bildirimi (Yedek olarak kalsın)
    url_tg = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload_tg = {"chat_id": CHAT_ID, "text": mesaj}
    
    # 2. NTFY Bildirimi (Doğrudan Telefona Bildirim)
    url_ntfy = f"https://ntfy.sh/{NTFY_TOPIC}"
    
    try:
        # Telegram'a gönder
        requests.post(url_tg, data=payload_tg, timeout=10)
        
        # Telefonuna (ntfy) gönder
        requests.post(url_ntfy, 
                      data=mesaj.encode('utf-8'), 
                      headers={
                          "Title": "Hisse Alım Fırsatı!",
                          "Priority": "high",
                          "Tags": "chart_with_upwards_trend,moneybag"
                      },
                      timeout=10)
    except Exception as e:
        print(f"Bildirim gönderme hatası: {e}")

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
            if True: # Test bittikten sonra tekrar eski haline getirirsin:
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


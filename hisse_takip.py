import yfinance as yf
import requests
import os
import smtplib
from email.message import EmailMessage

# Üst kısımdaki ayarlara şunları ekle
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# --- AYARLAR ---
NTFY_TOPIC = "Hisse" # Uygulamadaki ismin birebir aynisi olmali

hisseler = {
    "NVDA": (0, 195),
    "AMD": (0, 215),
    "UBER": (0, 70),
    "CRWV": (0, 75),
    "JOBY": (0, 8.5),
    "QBTS": (0, 16)
}

def mesaj_gonder(mesaj):
    # --- 1. TELEFON BİLDİRİMİ (ntfy.sh) ---
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        requests.post(url, data=mesaj.encode('utf-8'), 
                      headers={"Title": "Hisse Fiyat Uyarısı", "Priority": "high"}, timeout=10)
    except:
        print("ntfy hatası")

    # --- 2. E-POSTA BİLDİRİMİ (Gmail) ---
    if EMAIL_USER and EMAIL_PASS:
        try:
            msg = EmailMessage()
            msg.set_content(mesaj)
            msg['Subject'] = 'Hisse Alım Fırsatı Hatırlatıcısı'
            msg['From'] = EMAIL_USER
            msg['To'] = EMAIL_USER # Bildirimi kendine gönderiyorsun

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_USER, EMAIL_PASS)
                smtp.send_message(msg)
            print("E-posta başarıyla gönderildi.")
        except Exception as e:
            print(f"E-posta hatası: {e}")
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






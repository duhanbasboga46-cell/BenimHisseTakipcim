import yfinance as yf
import requests
import os

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
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        requests.post(url, 
                      data=mesaj.encode('utf-8'), 
                      headers={
                          "Title": "Hisse Hedef Fiyat Uyarısı",
                          "Priority": "high",
                          "Tags": "moneybag,chart_with_upwards_trend"
                      }, 
                      timeout=10)
        print("Bildirim telefona gönderildi.")
    except Exception as e:
        print(f"Bildirim gönderilirken hata oluştu: {e}")

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
    # Sadece ntfy başlığı tanımlı mı diye bakar
    if NTFY_TOPIC:
        kontrol_et()
    else:
        print("Hata: NTFY_TOPIC tanımlanmamış!")



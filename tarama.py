from datetime import datetime
import time
import pandas as pd
import requests
import yfinance as yf

# Ntfy Kanal Ayarı
NTFY_TOPIC = "kaptan_78"
COOLDOWN_SECONDS = 1800  # Aynı hisse için 30 dakika spam engelleme
son_bildirimler = {}

# BIST Hisse Listesi
BIST_HISSELERI = [
    "THYAO.IS",
    "GARAN.IS",
    "AKBNK.IS",
    "EREGL.IS",
    "KCHOL.IS",
    "ISCTR.IS",
    "BIMAS.IS",
    "YKBNK.IS",
    "SAHOL.IS",
    "ASELS.IS",
    "PETKM.IS",
    "TUPRS.IS",
    "SASA.IS",
    "HEKTS.IS",
    "KOZAA.IS",
    "FROTO.IS",
    "TOASO.IS",
    "PGSUS.IS",
    "KRDMD.IS",
    "SISE.IS",
]


def bildirim_gonder(mesaj):
  try:
    requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=mesaj.encode("utf-8"))
  except Exception as e:
    print(f"Bildirim hatası: {e}")


def veri_cek(hisse, period="5d", interval="15m"):
  try:
    df = yf.download(
        hisse, period=period, interval=interval, progress=False, timeout=10
    )
    if isinstance(df.columns, pd.MultiIndex):
      df.columns = df.columns.get_level_values(0)
    time.sleep(0.5)
    return df
  except Exception:
    return None


def dalga_ve_verimlilik_hesapla(df):
  try:
    if df is None or len(df) < 35:
      return False, 0, 0, 0, 0

    close = df["Close"]
    volume = df["Volume"]
    high = df["High"]
    low = df["Low"]

    ma8 = close.rolling(8).mean()
    vol_ma20 = volume.rolling(window=20).mean()
    rvol = volume.iloc[-1] / (vol_ma20.iloc[-1] + 1e-10)

    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))

    verimlilik_puani = 0
    if rvol > 1.5:
      verimlilik_puani += 15
    if rsi.iloc[-1] > 50:
      verimlilik_puani += 10
    if close.iloc[-1] > ma8.iloc[-1]:
      verimlilik_puani += 10

    fiyat_degisim_kisa = (
        (close.iloc[-1] - close.iloc[-4]) / close.iloc[-4] * 100
    )
    bar_araligi = high.iloc[-1] - low.iloc[-1]
    toparlanma_orani = (
        (close.iloc[-1] - low.iloc[-1]) / bar_araligi if bar_araligi > 0 else 0
    )

    dip_patlama_sarti = (
        fiyat_degisim_kisa <= 1.0
        and rvol >= 2.5
        and toparlanma_orani >= 0.70
        and verimlilik_puani >= 35
    )

    return (
        dip_patlama_sarti,
        verimlilik_puani,
        rvol,
        close.iloc[-1],
        fiyat_degisim_kisa,
    )
  except Exception:
    return False, 0, 0, 0, 0


def ana_tarama_motoru(periyot_adi="15m"):
  print(f"[{datetime.now()}] {periyot_adi} Tarama Başladı...")
  bulunanlar = 0

  for hisse in BIST_HISSELERI:
    df = veri_cek(hisse, period="5d", interval=periyot_adi)
    if df is None or len(df) < 35:
      continue

    sart_saglandi, puan, rvol, fiyat, degisim = dalga_ve_verimlilik_hesapla(df)

    if sart_saglandi:
      simdi = time.time()
      if (
          hisse not in son_bildirimler
          or (simdi - son_bildirimler[hisse]) > COOLDOWN_SECONDS
      ):
        mesaj = (
            f"🎯 [PROFESYONEL HİBRİT - DİP AVCISI]\n"
            f"• Hisse: {hisse} ({periyot_adi})\n"
            f"• Fiyat: {fiyat:.2f} TL\n"
            f"• Verimlilik Puanı: {puan} / 35+\n"
            f"• RVOL (Hacim Çarpanı): {rvol:.1f}x\n"
            f"• Durum: Eksiden Sert Toparlanma & Patlama!"
        )
        bildirim_gonder(mesaj)
        son_bildirimler[hisse] = simdi
        bulunanlar += 1

  print(f"[{datetime.now()}] {periyot_adi} Tarama Tamamlandı.")


if __name__ == "__main__":
  ana_tarama_motoru("15m")
  ana_tarama_motoru("1h")

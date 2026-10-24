from datetime import datetime
import time
import pandas as pd
import requests
import yfinance as yf

# Ntfy Kanal Ayarı
NTFY_TOPIC = "kaptan_78"
COOLDOWN_SECONDS = 1800  # Aynı hisse için 30 dakika spam engelleme
son_bildirimler = {}

# BIST Tüm Hisseler (Eksiksiz Tam Liste - 40'arLı Gruplar)
BIST_GRUPLARI = [
    # Grup 1
    [
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
        "TAVHL.IS",
        "ENKAI.IS",
        "MGROS.IS",
        "ARCLK.IS",
        "VESTL.IS",
        "OYAKC.IS",
        "ALARK.IS",
        "ODAS.IS",
        "KONTR.IS",
        "GESAN.IS",
        "ASTOR.IS",
        "CWENE.IS",
        "EUPWR.IS",
        "SDTTR.IS",
        "YEOTK.IS",
        "ALFAS.IS",
        "BRYAT.IS",
        "CLEBI.IS",
        "ISGYO.IS",
        "EKGYO.IS",
    ],
    # Grup 2
    [
        "ENJSA.IS",
        "ZOREN.IS",
        "AKSEN.IS",
        "BIOEN.IS",
        "GWIND.IS",
        "CANTE.IS",
        "IPEKE.IS",
        "KOZAL.IS",
        "GUBRF.IS",
        "TKFEN.IS",
        "AGHOL.IS",
        "ANACM.IS",
        "ARASE.IS",
        "AYDEM.IS",
        "BAGFS.IS",
        "BANVT.IS",
        "BSOKE.IS",
        "CCOLA.IS",
        "CEMTS.IS",
        "CIMSA.IS",
        "DEVA.IS",
        "ECILC.IS",
        "EGEEN.IS",
        "ENERY.IS",
        "EGEPO.IS",
        "ERCB.IS",
        "EKSUN.IS",
        "FORMT.IS",
        "GENIL.IS",
        "GLYHO.IS",
        "GSDHO.IS",
        "GOLTS.IS",
        "GOODY.IS",
        "GRTRK.IS",
        "HURGZ.IS",
        "INVES.IS",
        "ITTFH.IS",
        "JANTS.IS",
        "KAPLM.IS",
        "KARTN.IS",
    ],
    # Grup 3
    [
        "KERVT.IS",
        "KMPUR.IS",
        "KONYA.IS",
        "KORDS.IS",
        "KRPLS.IS",
        "KRVGD.IS",
        "LOGO.IS",
        "LUKSK.IS",
        "MAVI.IS",
        "MEDTR.IS",
        "MERKO.IS",
        "MIPAZ.IS",
        "MPARK.IS",
        "NATEN.IS",
        "NTHOL.IS",
        "OBASE.IS",
        "ONCSM.IS",
        "OTKAR.IS",
        "OYLUM.IS",
        "PAKDM.IS",
        "PAPIL.IS",
        "PCILT.IS",
        "PENGD.IS",
        "PNSUT.IS",
        "POLHO.IS",
        "PRKME.IS",
        "PSGYO.IS",
        "QUAGR.IS",
        "RALYH.IS",
        "RNPOL.IS",
        "RTALB.IS",
        "RYGYO.IS",
        "SAFKR.IS",
        "SELEC.IS",
        "SELVA.IS",
        "SEYKM.IS",
        "SMRTG.IS",
        "SOKM.IS",
        "TATEN.IS",
        "TBORG.IS",
    ],
    # Grup 4
    [
        "TGSAS.IS",
        "TMPOL.IS",
        "TMSN.IS",
        "TRGYO.IS",
        "TSKB.IS",
        "TTKOM.IS",
        "TTRAK.IS",
        "TUKAS.IS",
        "TURSG.IS",
        "UFUK.IS",
        "ULKER.IS",
        "ULUUN.IS",
        "VAKBN.IS",
        "VAKKO.IS",
        "VBTYZ.IS",
        "VERTU.IS",
        "VKGYO.IS",
        "VKING.IS",
        "YAPRK.IS",
        "YATAS.IS",
        "YAYLA.IS",
        "YUNSA.IS",
        "ZIRAY.IS",
        "ACSEL.IS",
        "ADEL.IS",
        "ADGYO.IS",
        "AEFES.IS",
        "AFYON.IS",
        "AGEHA.IS",
        "AGROT.IS",
        "AHGAZ.IS",
        "AKENR.IS",
        "AKFGY.IS",
        "AKFYE.IS",
        "AKSGY.IS",
        "AKSUE.IS",
        "ALBRK.IS",
        "ALCAR.IS",
        "ALCTL.IS",
        "ALKA.IS",
    ],
    # Grup 5
    [
        "ALTNY.IS",
        "ANELE.IS",
        "ANGEN.IS",
        "ARFYO.IS",
        "ARSAN.IS",
        "ARTMS.IS",
        "ARZUM.IS",
        "ASUZU.IS",
        "ATAKP.IS",
        "ATEKS.IS",
        "ATLAS.IS",
        "AVGYO.IS",
        "AVOD.IS",
        "AVTUR.IS",
        "AYCES.IS",
        "AYEN.IS",
        "AYES.IS",
        "AZTEK.IS",
        "BAKAB.IS",
        "BALAT.IS",
        "BARMA.IS",
        "BASGZ.IS",
        "BASCM.IS",
        "BATI.IS",
        "BERA.IS",
        "BEYAZ.IS",
        "BIENY.IS",
        "BJKAS.IS",
        "BLCYT.IS",
        "BMSCH.IS",
        "BMSTL.IS",
        "BNTAS.IS",
        "BOBET.IS",
        "BORLS.IS",
        "BOSSA.IS",
        "BRKO.IS",
        "BRKSN.IS",
        "BRMEN.IS",
        "BRSAN.IS",
        "BUCIM.IS",
    ],
    # Grup 6
    [
        "BURCE.IS",
        "BURVA.IS",
        "BVSAN.IS",
        "BYDNR.IS",
        "CASA.IS",
        "CATES.IS",
        "CEFH.IS",
        "CEMAS.IS",
        "CEOEM.IS",
        "CVKMD.IS",
        "DAPGM.IS",
        "DARDL.IS",
        "DENGE.IS",
        "DERHL.IS",
        "DERIM.IS",
        "DESA.IS",
        "DESPC.IS",
        "DGNMO.IS",
        "DIRIT.IS",
        "DITAS.IS",
        "DMRGD.IS",
        "DMSAS.IS",
        "DNISI.IS",
        "DOAS.IS",
        "DOBUR.IS",
        "DOCO.IS",
        "DOGUE.IS",
        "DOHOL.IS",
        "DOKTA.IS",
        "DSI.IS",
        "DURDO.IS",
        "DYOBY.IS",
        "DZGYO.IS",
        "EBEBK.IS",
        "EDATA.IS",
        "EDIP.IS",
        "EGEGY.IS",
        "EGGUB.IS",
        "EGPRO.IS",
        "EGSER.IS",
    ],
    # Grup 7
    [
        "EMKEL.IS",
        "ENSRI.IS",
        "EPLAS.IS",
        "ERBOS.IS",
        "ERSU.IS",
        "ESEN.IS",
        "ESCOM.IS",
        "ETILR.IS",
        "EUHOL.IS",
        "EUKO.IS",
        "FADE.IS",
        "FENER.IS",
        "FLAP.IS",
        "FMIZP.IS",
        "FONET.IS",
        "FORTE.IS",
        "FRIGO.IS",
        "GARFA.IS",
        "GEDIK.IS",
        "GENTS.IS",
        "GEREL.IS",
        "GESAN.IS",
        "GIPAS.IS",
        "GLRYH.IS",
        "GMTAS.IS",
        "GOKNR.IS",
        "GRNYO.IS",
        "GZNMI.IS",
        "HATEK.IS",
        "HDFGS.IS",
        "HKTM.IS",
        "HLGYO.IS",
        "HTTBT.IS",
        "HUBVC.IS",
        "ICBCT.IS",
        "IDEAS.IS",
        "IHEVA.IS",
        "IHGZT.IS",
        "IHLAS.IS",
        "IHLGM.IS",
    ],
    # Grup 8
    [
        "IMASM.IS",
        "INDES.IS",
        "INFO.IS",
        "INTEM.IS",
        "INVEO.IS",
        "ISATR.IS",
        "ISBIR.IS",
        "ISBTR.IS",
        "ISFIN.IS",
        "ISKUR.IS",
        "IZENR.IS",
        "IZFAS.IS",
        "IZINV.IS",
        "KAHMK.IS",
        "KAKK.IS",
        "KAYSE.IS",
        "KFEIN.IS",
        "KGYO.IS",
        "KIMMR.IS",
        "KLGYO.IS",
        "KLKIM.IS",
        "KLRHO.IS",
        "KLMSN.IS",
        "KMPUR.IS",
        "KNFRT.IS",
        "KOCMT.IS",
        "KOTON.IS",
        "KRSTL.IS",
        "KUTPO.IS",
        "KUVVA.IS",
        "LIDER.IS",
        "LKMNH.IS",
        "MAALT.IS",
        "MAKIM.IS",
        "MAKTK.IS",
        "MANAS.IS",
        "MARKA.IS",
        "MARTI.IS",
        "MACKO.IS",
        "MEGAP.IS",
    ],
    # Grup 9
    [
        "MEKAG.IS",
        "MESAN.IS",
        "METRO.IS",
        "METUR.IS",
        "MHRGY.IS",
        "MIKRO.IS",
        "MMCAS.IS",
        "MNDRS.IS",
        "MNDTR.IS",
        "MOBTL.IS",
        "MTRKS.IS",
        "MZHLD.IS",
        "NUGYO.IS",
        "NUHCM.IS",
        "OBASE.IS",
        "ODINE.IS",
        "OFSYM.IS",
        "ONRYT.IS",
        "ORCAY.IS",
        "ORGE.IS",
        "OSMEN.IS",
        "OSTIM.IS",
        "OTTO.IS",
        "OYYAT.IS",
        "OZAKG.IS",
        "OZRDN.IS",
        "OZSUB.IS",
        "PAGYO.IS",
        "PAMEL.IS",
        "PARDUS.IS",
        "PARSN.IS",
        "PATEK.IS",
        "PEKGY.IS",
        "PENTA.IS",
        "PKART.IS",
        "PKENT.IS",
        "PNLSN.IS",
        "POLTK.IS",
        "PRDGS.IS",
        "PRZMA.IS",
    ],
    # Grup 10
    [
        "PSDTC.IS",
        "QNBFL.IS",
        "REEDR.IS",
        "RGYAS.IS",
        "RODRG.IS",
        "ROWAN.IS",
        "SANKO.IS",
        "SARKY.IS",
        "SAYAS.IS",
        "SDTTR.IS",
        "SEGMN.IS",
        "SEKFK.IS",
        "SEKUR.IS",
        "SELGD.IS",
        "SERNT.IS",
        "SILVR.IS",
        "SMART.IS",
        "SMRTG.IS",
        "SNICA.IS",
        "SNPAM.IS",
        "SODSN.IS",
        "SOKE.IS",
        "SURGY.IS",
        "SUWEN.IS",
        "TABGD.IS",
        "TARKN.IS",
        "TATEN.IS",
        "TAVHL.IS",
        "TBORG.IS",
        "TCELL.IS",
        "TEZOL.IS",
        "TGSAS.IS",
        "THYAO.IS",
        "TKNSA.IS",
        "TMPOL.IS",
        "TMSN.IS",
        "TOASO.IS",
        "TRGYO.IS",
        "TSKB.IS",
        "TTKOM.IS",
    ],
]


def bildirim_gonder(mesaj):
  try:
    requests.post(f"https://ntfy.sh/{NTFY_TOPIC}", data=mesaj.encode("utf-8"))
  except Exception as e:
    print(f"Bildirim hatası: {e}")


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
  print(f"[{datetime.now()}] {periyot_adi} BIST Toplu İndirme ve Tarama Başladı...")
  bulunanlar = 0

  for grup_index, grup in enumerate(BIST_GRUPLARI):
    print(f"-> Grup {grup_index + 1} toplu indiriliyor...")
    try:
      df_grup = yf.download(
          grup, period="5d", interval=periyot_adi, progress=False, timeout=30
      )

      for hisse in grup:
        clean_hisse = hisse.strip()
        try:
          if isinstance(df_grup.columns, pd.MultiIndex):
            if clean_hisse in df_grup["Close"].columns:
              df = pd.DataFrame(
                  {
                      "Open": df_grup["Open"][clean_hisse],
                      "High": df_grup["High"][clean_hisse],
                      "Low": df_grup["Low"][clean_hisse],
                      "Close": df_grup["Close"][clean_hisse],
                      "Volume": df_grup["Volume"][clean_hisse],
                  }
              ).dropna()
            else:
              continue
          else:
            df = df_grup

          if df is None or len(df) < 35:
            continue

          sart_saglandi, puan, rvol, fiyat, degisim = (
              dalga_ve_verimlilik_hesapla(df)
          )

          if sart_saglandi:
            simdi = time.time()
            if (
                clean_hisse not in son_bildirimler
                or (simdi - son_bildirimler[clean_hisse]) > COOLDOWN_SECONDS
            ):
              mesaj = (
                  f"🎯 [PROFESYONEL HİBRİT - DİP AVCISI]\n"
                  f"• Hisse: {clean_hisse} ({periyot_adi})\n"
                  f"• Fiyat: {fiyat:.2f} TL\n"
                  f"• Verimlilik Puanı: {puan} / 35+\n"
                  f"• RVOL (Hacim Çarpanı): {rvol:.1f}x\n"
                  f"• Durum: Eksiden Sert Toparlanma & Patlama!"
              )
              bildirim_gonder(mesaj)
              son_bildirimler[clean_hisse] = simdi
              bulunanlar += 1
        except Exception:
          continue
    except Exception as e:
      print(f"Grup indirme hatası: {e}")

  print(f"[{datetime.now()}] {periyot_adi} Tarama Tamamlandı. Bulunan: {bulunanlar}")


if __name__ == "__main__":
  ana_tarama_motoru("15m")
  ana_tarama_motoru("1h")

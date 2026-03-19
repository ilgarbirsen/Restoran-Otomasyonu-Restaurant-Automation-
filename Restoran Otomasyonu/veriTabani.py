import mysql.connector
from datetime import datetime
import random

#Giriş bilgileri
girisBilgileri = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "restoran"
}


def baglantiYap():
    try:
        return mysql.connector.connect(**girisBilgileri)
    except:
        return None


def veritabaniHazirla():
    try:
        geciciBaglanti = mysql.connector.connect(host="localhost", user="root", password="")
        islem = geciciBaglanti.cursor()
        islem.execute("CREATE DATABASE IF NOT EXISTS restoran")
        geciciBaglanti.close()

        baglanti = baglantiYap()
        if baglanti.is_connected():
            print("Veritabanı bağlantısı BAŞARILI.")
            baglanti.close()
        else:
            print("HATA: Veritabanına bağlanılamadı.")
    except Exception as hata:
        print(f"KRİTİK HATA: {hata}")


#İŞLEM FONKSİYONLARI

def masaListesiniGetir(durumFiltresi):
    baglanti = baglantiYap()
    islem = baglanti.cursor(dictionary=True)

    sorgu = "SELECT m.*, u.ad as musteri_adi FROM restoran_masalari m LEFT JOIN uyeler u ON m.aktif_uye_id = u.id WHERE m.aktif_mi=1"
    if durumFiltresi and durumFiltresi != "Tümü":
        sorgu += f" AND m.durum = '{durumFiltresi}'"
    sorgu += " ORDER BY m.masa_no"

    islem.execute(sorgu)
    liste = islem.fetchall()
    baglanti.close()
    return liste


def masaEkle(masaNumarasi):
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    try:
        islem.execute("SELECT id FROM restoran_masalari WHERE masa_no = %s", (masaNumarasi,))
        kayit = islem.fetchone()

        if kayit:
            masaId = kayit[0]
            islem.execute("UPDATE restoran_masalari SET aktif_mi=1, durum='bos' WHERE id=%s", (masaId,))
        else:
            islem.execute("INSERT INTO restoran_masalari (masa_no, durum, aktif_mi) VALUES (%s, 'bos', 1)",
                          (masaNumarasi,))

        baglanti.commit()
    except Exception as hata:
        print(f"Masa Ekleme Hatası: {hata}")
    finally:
        baglanti.close()

def masaSil(masaId):
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    islem.execute("SELECT COUNT(*) FROM siparisler WHERE masa_id=%s AND odeme_durumu='aktif'", (masaId,))
    if islem.fetchone()[0] > 0:
        baglanti.close()
        return False
    islem.execute("UPDATE restoran_masalari SET aktif_mi=0 WHERE id=%s", (masaId,))
    baglanti.commit()
    baglanti.close()
    return True


def urunListesiniGetir(aramaKelimesi="", kategoriSecimi=""):
    baglanti = baglantiYap()
    islem = baglanti.cursor(dictionary=True)
    sorgu = "SELECT * FROM urunler WHERE aktif_mi=1"

    if kategoriSecimi and kategoriSecimi != "Genel" and kategoriSecimi != "Tümü":
        sorgu += f" AND kategori = '{kategoriSecimi}'"
    if aramaKelimesi:
        sorgu += f" AND ad LIKE '%{aramaKelimesi}%'"

    sorgu += " ORDER BY ad"
    islem.execute(sorgu)
    liste = islem.fetchall()
    baglanti.close()
    return liste


def urunEkleVeyaGuncelle(id, ad, kategori, fiyat):
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    try:
        if id:
            islem.execute("UPDATE urunler SET ad=%s, kategori=%s, fiyat=%s WHERE id=%s", (ad, kategori, fiyat, id))
        else:
            islem.execute("INSERT INTO urunler (ad, kategori, fiyat) VALUES (%s, %s, %s)", (ad, kategori, fiyat))
        baglanti.commit()
        return True
    except:
        return False
    finally:
        baglanti.close()


def musteriAraVeGetir(kelime=""):
    baglanti = baglantiYap()
    islem = baglanti.cursor(dictionary=True)
    sorgu = "SELECT * FROM uyeler WHERE aktif_mi=1"
    if kelime:
        sorgu += f" AND (ad LIKE '%{kelime}%' OR telefon LIKE '%{kelime}%')"
    islem.execute(sorgu)
    liste = islem.fetchall()
    baglanti.close()
    return liste


def musteriDuzenle(id, ad, telefon, email, adres):
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    try:
        if id:
            islem.execute("UPDATE uyeler SET ad=%s, telefon=%s, email=%s, adres=%s WHERE id=%s",
                          (ad, telefon, email, adres, id))
        else:
            rastgeleKod = f"M{random.randint(1000, 9999)}"
            islem.execute("INSERT INTO uyeler (uye_kod, ad, telefon, email, adres) VALUES (%s, %s, %s, %s, %s)",
                          (rastgeleKod, ad, telefon, email, adres))
        baglanti.commit()
        return True
    except:
        return False
    finally:
        baglanti.close()


def siparisOlustur(uyeId, masaId):
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    tarih = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    siparisKodu = f"SIP{random.randint(1000, 9999)}"
    islem.execute(
        "INSERT INTO siparisler (siparis_kod, uye_id, masa_id, odeme_durumu, olusturma_tarihi) VALUES (%s, %s, %s, 'aktif', %s)",
        (siparisKodu, uyeId, masaId, tarih))
    yeniSiparisId = islem.lastrowid
    islem.execute("UPDATE restoran_masalari SET durum='dolu', aktif_uye_id=%s WHERE id=%s", (uyeId, masaId))
    baglanti.commit()
    baglanti.close()
    return yeniSiparisId


def siparisDetayi(siparisId, urunId, fiyat):
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    islem.execute("INSERT INTO siparis_detaylari (siparis_id, urun_id, adet, birim_fiyat) VALUES (%s, %s, 1, %s)",
                  (siparisId, urunId, fiyat))
    islem.execute(
        "UPDATE siparisler s SET toplam_fiyat = (SELECT SUM(adet*birim_fiyat) FROM siparis_detaylari WHERE siparis_id=s.id) WHERE s.id=%s",
        (siparisId,))
    baglanti.commit()
    baglanti.close()


def masadakiAktifSiparisiBul(masaId):
    baglanti = baglantiYap()
    islem = baglanti.cursor(dictionary=True)
    islem.execute(
        "SELECT s.*, u.ad as musteri_adi FROM siparisler s JOIN uyeler u ON s.uye_id = u.id WHERE s.masa_id=%s AND s.odeme_durumu='aktif' LIMIT 1",
        (masaId,))
    siparis = islem.fetchone()
    baglanti.close()
    return siparis


def siparisSepetiniGetir(siparisId):
    baglanti = baglantiYap()
    islem = baglanti.cursor(dictionary=True)
    islem.execute(
        "SELECT d.*, u.ad as urun_adi FROM siparis_detaylari d JOIN urunler u ON d.urun_id = u.id WHERE d.siparis_id=%s",
        (siparisId,))
    liste = islem.fetchall()
    baglanti.close()
    return liste


def siparisiKapat(siparisId, masaId, durum="tamamlandi"):
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    islem.execute("UPDATE siparisler SET odeme_durumu=%s WHERE id=%s", (durum, siparisId))
    islem.execute("UPDATE restoran_masalari SET durum='bos', aktif_uye_id=NULL WHERE id=%s", (masaId,))
    baglanti.commit()
    baglanti.close()


def gunlukKarHesapla():
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    bugun = datetime.now().strftime('%Y-%m-%d')
    islem.execute(
        f"SELECT SUM(toplam_fiyat), COUNT(*) FROM siparisler WHERE odeme_durumu='tamamlandi' AND DATE(olusturma_tarihi)='{bugun}'")
    sonuc = islem.fetchone()
    baglanti.close()
    return sonuc


def musteriGecmisSiparisleriniGetir(musteriId):
    baglanti = baglantiYap()
    islem = baglanti.cursor(dictionary=True)
    sorgu = "SELECT * FROM siparisler WHERE uye_id = %s AND odeme_durumu = 'tamamlandi' ORDER BY olusturma_tarihi DESC"
    islem.execute(sorgu, (musteriId,))
    liste = islem.fetchall()
    baglanti.close()
    return liste

def urunSil(urunId):
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    try:
        islem.execute("UPDATE urunler SET aktif_mi=0 WHERE id=%s", (urunId,))
        baglanti.commit()
        return True
    except:
        return False
    finally:
        baglanti.close()

def musteriSil(musteriId):
    baglanti = baglantiYap()
    islem = baglanti.cursor()
    try:
        islem.execute("UPDATE uyeler SET aktif_mi=0 WHERE id=%s", (musteriId,))
        baglanti.commit()
        return True
    except:
        return False
    finally:
        baglanti.close()
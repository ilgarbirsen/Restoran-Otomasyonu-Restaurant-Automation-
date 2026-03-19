import tkinter as tk
from tkinter import messagebox
import veriTabani

#DEĞİŞKENLER
seciliMasaNumarasi = None
seciliMasaId = None
aktifSiparisId = None
seciliMusteriId = None
duzenlenecekUrunId = None
duzenlenecekMusteriId = None

araclar = {}


def baslat():
    masaListesiniGuncelle()
    urunListesiniGuncelle()
    musteriListesiniGuncelle()
    karRaporunuGuncelle()


# MASA İŞLEMLERİ
def masaListesiniGuncelle():
    for widget in araclar['masaCercevesi'].winfo_children():
        widget.destroy()

    filtre = araclar['masaFiltre'].get()
    masalar = veriTabani.masaListesiniGetir(filtre)

    for masa in masalar:
        renk = "green" if masa['durum'] == 'bos' else "red"
        yazi = f"Masa {masa['masa_no']}\n{masa['durum']}"
        if masa['musteri_adi']:
            yazi += f"\n{masa['musteri_adi']}"

        btn = tk.Button(araclar['masaCercevesi'], text=yazi, bg=renk, fg='white', width=12, height=4,
                        command=lambda mid=masa['id'], mno=masa['masa_no']: masaSecildi(mid, mno))

        sira = (masa['masa_no'] - 1) // 5
        sutun = (masa['masa_no'] - 1) % 5
        btn.grid(row=sira, column=sutun, padx=5, pady=5)


def yeniMasaEkle():
    masaNo = araclar['masaEkleme'].get()
    if masaNo:
        veriTabani.masaEkle(masaNo)
        masaListesiniGuncelle()
        araclar['masaEkleme'].delete(0, tk.END)


def masaSil():
    if not seciliMasaId:
        messagebox.showerror("Hata", "Önce bir masa seçin!")
        return
    basari = veriTabani.masaSil(seciliMasaId)
    if basari:
        messagebox.showinfo("Tamam", "Masa silindi.")
        masaListesiniGuncelle()
    else:
        messagebox.showerror("Hata", "Dolu masa silinemez!")


def masaSecildi(masaId, masaNo):
    global seciliMasaId, seciliMasaNumarasi, aktifSiparisId, seciliMusteriId

    seciliMasaId = masaId
    seciliMasaNumarasi = masaNo

    araclar['seciliMasaEtiketi'].config(text=f"Seçili Masa: {masaNo}")

    araclar['sekmePanel'].select(araclar['siparisSekmesi'])

    araclar['siparisMasa'].config(state='normal')
    araclar['siparisMasa'].delete(0, tk.END)
    araclar['siparisMasa'].insert(0, str(masaNo))
    araclar['siparisMasa'].config(state='readonly')

    siparis = veriTabani.masadakiAktifSiparisiBul(masaId)

    sepetiTemizle()

    if siparis:
        aktifSiparisId = siparis['id']
        seciliMusteriId = siparis['uye_id']
        araclar['musteriEtiketi'].config(text=f"Müşteri: {siparis['musteri_adi']}", fg="blue")
        araclar['toplamFiyatEtiketi'].config(text=f"Toplam: {siparis['toplam_fiyat']} TL")
        sepetiDoldur(aktifSiparisId)
    else:
        aktifSiparisId = None
        seciliMusteriId = None
        araclar['musteriEtiketi'].config(text="Müşteri Seçilmedi", fg="red")
        araclar['toplamFiyatEtiketi'].config(text="Toplam: 0.00 TL")

    musteriAra()


def musteriSecili(event):
    global seciliMusteriId
    secilenSatir = araclar['musteriSecim'].selection()
    if secilenSatir:
        degerler = araclar['musteriSecim'].item(secilenSatir)['values']
        seciliMusteriId = degerler[0]
        ad = degerler[2]
        araclar['musteriEtiketi'].config(text=f"Seçilecek: {ad}", fg="green")


def siparisBaslat():
    global aktifSiparisId
    if not seciliMasaId:
        messagebox.showerror("Hata", "Masa seçili değil!")
        return
    if not seciliMusteriId:
        messagebox.showerror("Hata", "Müşteri seçmediniz!")
        return
    if aktifSiparisId:
        messagebox.showinfo("Bilgi", "Bu masa zaten açık.")
        return

    aktifSiparisId = veriTabani.siparisOlustur(seciliMusteriId, seciliMasaId)
    messagebox.showinfo("Başarılı", "Sipariş açıldı.")
    araclar['musteriEtiketi'].config(fg="blue")
    masaListesiniGuncelle()


def sepeteUrunEkle():
    if not aktifSiparisId:
        messagebox.showerror("Hata", "Önce 'Siparişi Başlat' butonuna basın.")
        return

    secilen = araclar['menuListesi'].curselection()
    if not secilen:
        messagebox.showerror("Hata", "Listeden ürün seçin.")
        return

    urun = urunHafizasi[secilen[0]]
    veriTabani.siparisDetayi(aktifSiparisId, urun['id'], float(urun['fiyat']))

    sepetiDoldur(aktifSiparisId)

    siparis = veriTabani.masadakiAktifSiparisiBul(seciliMasaId)
    araclar['toplamFiyatEtiketi'].config(text=f"Toplam: {siparis['toplam_fiyat']} TL")


def sepetiDoldur(siparisId):
    sepetiTemizle()
    urunler = veriTabani.siparisSepetiniGetir(siparisId)
    for urun in urunler:
        araclar['sepetListesiGorunumu'].insert("", "end", values=(urun['urun_adi'], urun['adet'], urun['birim_fiyat']))


def sepetiTemizle():
    for satir in araclar['sepetListesiGorunumu'].get_children():
        araclar['sepetListesiGorunumu'].delete(satir)


def siparisiKapatVeOde():
    if aktifSiparisId:
        veriTabani.siparisiKapat(aktifSiparisId, seciliMasaId)
        messagebox.showinfo("Tamam", "Hesap ödendi, masa boşaldı.")
        masaListesiniGuncelle()
        araclar['sekmePanel'].select(araclar['masaSekmesi'])


def siparisiIptalEt():
    if aktifSiparisId:
        cevap = messagebox.askyesno("İptal", "Siparişi iptal etmek istediğinize emin misiniz?")
        if cevap:
            veriTabani.siparisiKapat(aktifSiparisId, seciliMasaId, durum="iptal")
            messagebox.showinfo("İptal", "Sipariş iptal edildi, masa boşaldı.")
            masaListesiniGuncelle()
            araclar['sekmePanel'].select(araclar['masaSekmesi'])


urunHafizasi = []


def urunListesiniGuncelle(event=None):
    global urunHafizasi
    arananKelime = araclar['urunArama'].get()

    araclar['menuListesi'].delete(0, tk.END)
    araclar['menuDuzenleListesi'].delete(*araclar['menuDuzenleListesi'].get_children())

    urunler = veriTabani.urunListesiniGetir(aramaKelimesi=arananKelime)
    urunHafizasi = urunler

    for urun in urunler:
        araclar['menuListesi'].insert(tk.END, f"{urun['ad']} - {urun['fiyat']} TL")
        araclar['menuDuzenleListesi'].insert("", "end",
                                             values=(urun['id'], urun['ad'], urun['kategori'], urun['fiyat']))


def urunKaydet():
    global duzenlenecekUrunId
    ad = araclar['urunAdi'].get()
    fiyat = araclar['urunFiyati'].get()
    kategori = araclar['urunKategori'].get()

    if ad and fiyat:
        veriTabani.urunEkleVeyaGuncelle(duzenlenecekUrunId, ad, kategori, float(fiyat))
        messagebox.showinfo("Tamam", "Ürün kaydedildi.")
        urunFormunuTemizle()
        urunListesiniGuncelle()
    else:
        messagebox.showerror("Hata", "Bilgiler eksik.")


def urunSil():
    global duzenlenecekUrunId
    if not duzenlenecekUrunId:
        messagebox.showerror("Hata", "Lütfen listeden silinecek bir ürün seçin.")
        return

    cevap = messagebox.askyesno("Sil", "Bu ürünü silmek istediğinize emin misiniz?")
    if cevap:
        basari = veriTabani.urunSil(duzenlenecekUrunId)
        if basari:
            messagebox.showinfo("Tamam", "Ürün silindi.")
            urunFormunuTemizle()
            urunListesiniGuncelle()
        else:
            messagebox.showerror("Hata", "Ürün silinemedi.")


def urunDuzenlemekIcinSec(event):
    global duzenlenecekUrunId
    secilen = araclar['menuDuzenleListesi'].selection()
    if secilen:
        degerler = araclar['menuDuzenleListesi'].item(secilen)['values']
        duzenlenecekUrunId = degerler[0]

        araclar['urunAdi'].delete(0, tk.END)
        araclar['urunAdi'].insert(0, degerler[1])
        araclar['urunFiyati'].delete(0, tk.END)
        araclar['urunFiyati'].insert(0, degerler[3])
        araclar['urunKategori'].set(degerler[2])


def urunFormunuTemizle():
    global duzenlenecekUrunId
    duzenlenecekUrunId = None
    araclar['urunAdi'].delete(0, tk.END)
    araclar['urunFiyati'].delete(0, tk.END)


# MÜŞTERİ İŞLEMLERİ
def musteriKaydet():
    global duzenlenecekMusteriId
    ad = araclar['musteriAdi'].get()
    tel = araclar['musteriTelefon'].get()
    email = araclar['musteriEmail'].get()
    adres = araclar['musteriAdres'].get()

    if ad and tel:
        veriTabani.musteriDuzenle(duzenlenecekMusteriId, ad, tel, email, adres)
        messagebox.showinfo("Tamam", "Müşteri kaydedildi.")
        musteriFormunuTemizle()
        musteriListesiniGuncelle()
    else:
        messagebox.showerror("Hata", "Ad ve Telefon şart.")


def musteriSil():
    global duzenlenecekMusteriId
    if not duzenlenecekMusteriId:
        messagebox.showerror("Hata", "Lütfen listeden silinecek bir müşteri seçin.")
        return

    cevap = messagebox.askyesno("Sil", "Bu müşteriyi silmek istediğinize emin misiniz?")
    if cevap:
        basari = veriTabani.musteriSil(duzenlenecekMusteriId)
        if basari:
            messagebox.showinfo("Tamam", "Müşteri silindi.")
            musteriFormunuTemizle()
            musteriListesiniGuncelle()
        else:
            messagebox.showerror("Hata", "Müşteri silinemedi.")


def musteriAra(event=None):
    kelime = araclar['musteriArama'].get()
    for satir in araclar['musteriSecim'].get_children():
        araclar['musteriSecim'].delete(satir)

    liste = veriTabani.musteriAraVeGetir(kelime)
    for musteri in liste:
        araclar['musteriSecim'].insert("", "end",
                                       values=(musteri['id'], musteri['uye_kod'], musteri['ad'], musteri['telefon'],
                                               musteri['email']))


def musteriListesiniGuncelle():
    for satir in araclar['musteriListesi'].get_children():
        araclar['musteriListesi'].delete(satir)

    liste = veriTabani.musteriAraVeGetir("")
    for musteri in liste:
        araclar['musteriListesi'].insert("", "end",
                                         values=(musteri['id'], musteri['ad'], musteri['telefon'], musteri['email'],
                                                 musteri['adres']))


def musteriDuzenlemekIcinSec(event):
    global duzenlenecekMusteriId
    secilen = araclar['musteriListesi'].selection()
    if secilen:
        degerler = araclar['musteriListesi'].item(secilen)['values']
        duzenlenecekMusteriId = degerler[0]  # ID

        araclar['musteriAdi'].delete(0, tk.END)
        araclar['musteriAdi'].insert(0, degerler[1])

        araclar['musteriTelefon'].delete(0, tk.END)
        araclar['musteriTelefon'].insert(0, str(degerler[2]))

        araclar['musteriEmail'].delete(0, tk.END)
        araclar['musteriEmail'].insert(0, degerler[3])

        araclar['musteriAdres'].delete(0, tk.END)
        araclar['musteriAdres'].insert(0, degerler[4])

        musteriGecmisiniGuncelle(duzenlenecekMusteriId)


def musteriGecmisiniGuncelle(musteriId):
    for satir in araclar['gecmisSiparisListesi'].get_children():
        araclar['gecmisSiparisListesi'].delete(satir)

    siparisler = veriTabani.musteriGecmisSiparisleriniGetir(musteriId)

    for siparis in siparisler:
        araclar['gecmisSiparisListesi'].insert("", "end", values=(
            siparis['siparis_kod'],
            siparis['olusturma_tarihi'],
            f"{siparis['toplam_fiyat']} TL"
        ))


def musteriFormunuTemizle():
    global duzenlenecekMusteriId
    duzenlenecekMusteriId = None
    araclar['musteriAdi'].delete(0, tk.END)
    araclar['musteriTelefon'].delete(0, tk.END)
    araclar['musteriEmail'].delete(0, tk.END)
    araclar['musteriAdres'].delete(0, tk.END)


# Günlük gelir
def karRaporunuGuncelle():
    sonuc = veriTabani.gunlukKarHesapla()
    tutar = sonuc[0] if sonuc[0] else 0
    adet = sonuc[1] if sonuc[1] else 0
    araclar['karEtiketi'].config(text=f"Bugün: {tutar} TL ({adet} Sipariş)")
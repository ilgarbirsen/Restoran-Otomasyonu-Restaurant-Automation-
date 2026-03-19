import tkinter as tk
from tkinter import ttk
import uygulama


def arayuzuOlustur(pencere):
    sekmePanel = ttk.Notebook(pencere)
    sekmePanel.pack(fill="both", expand=True)

    masaSekmesi = tk.Frame(sekmePanel)
    siparisSekmesi = tk.Frame(sekmePanel)
    musteriSekmesi = tk.Frame(sekmePanel)
    menuSekmesi = tk.Frame(sekmePanel)
    raporSekmesi = tk.Frame(sekmePanel)

    sekmePanel.add(masaSekmesi, text="Masalar")
    sekmePanel.add(siparisSekmesi, text="Sipariş")
    sekmePanel.add(musteriSekmesi, text="Müşteriler")
    sekmePanel.add(menuSekmesi, text="Menü")
    sekmePanel.add(raporSekmesi, text="Günlük Kazanç")

    uygulama.araclar['sekmePanel'] = sekmePanel
    uygulama.araclar['siparisSekmesi'] = siparisSekmesi
    uygulama.araclar['masaSekmesi'] = masaSekmesi

    # MASA EKRANI
    ustCerceve = tk.Frame(masaSekmesi, bg="lightblue", pady=10)
    ustCerceve.pack(fill="x")

    tk.Label(ustCerceve, text="Masa Ekle (No):", bg="lightblue").pack(side="left", padx=5)
    masaEkleme = tk.Entry(ustCerceve, width=5)
    masaEkleme.pack(side="left")
    tk.Button(ustCerceve, text="Ekle", command=uygulama.yeniMasaEkle).pack(side="left", padx=5)

    tk.Label(ustCerceve, text="Filtre:", bg="lightblue").pack(side="left", padx=20)
    masaFiltre = ttk.Combobox(ustCerceve, values=["Tümü", "bos", "dolu"], state="readonly", width=10)
    masaFiltre.current(0)
    masaFiltre.pack(side="left")
    masaFiltre.bind("<<ComboboxSelected>>", lambda e: uygulama.masaListesiniGuncelle())

    tk.Button(ustCerceve, text="Seçili Masayı Sil", bg="red", fg="white", command=uygulama.masaSil).pack(side="right",
                                                                                                         padx=10)

    uygulama.araclar['seciliMasaEtiketi'] = tk.Label(ustCerceve, text="Seçili Masa: Yok", font=("Arial", 12, "bold"),
                                                     bg="lightblue")
    uygulama.araclar['seciliMasaEtiketi'].pack(side="right", padx=20)

    masaCercevesi = tk.Frame(masaSekmesi)
    masaCercevesi.pack(fill="both", expand=True, padx=10, pady=10)

    uygulama.araclar['masaEkleme'] = masaEkleme
    uygulama.araclar['masaFiltre'] = masaFiltre
    uygulama.araclar['masaCercevesi'] = masaCercevesi

    # SİPARİŞ EKRANI
    solPanel = tk.LabelFrame(siparisSekmesi, text="1. Müşteri & Masa", width=300)
    solPanel.pack(side="left", fill="y", padx=5, pady=5)

    tk.Label(solPanel, text="Masa No:").pack(pady=5)
    siparisMasa = tk.Entry(solPanel, state="readonly", font=("Arial", 14, "bold"), justify="center")
    siparisMasa.pack(pady=5)

    tk.Label(solPanel, text="Müşteri Ara:").pack(pady=5)
    musteriArama = tk.Entry(solPanel)
    musteriArama.pack()
    musteriArama.bind("<KeyRelease>", uygulama.musteriAra)

    musteriSecim = ttk.Treeview(solPanel, columns=("id", "kod", "ad", "tel", "email"), show="headings", height=8)
    musteriSecim.heading("ad", text="Ad Soyad")
    musteriSecim.heading("tel", text="Telefon")
    musteriSecim.heading("email", text="E-Mail")
    musteriSecim.column("id", width=0, stretch=False)
    musteriSecim.column("kod", width=0, stretch=False)
    musteriSecim.column("ad", width=80)
    musteriSecim.column("tel", width=80)
    musteriSecim.column("email", width=120)
    musteriSecim.pack(fill="x", pady=5)

    musteriSecim.bind("<<TreeviewSelect>>", uygulama.musteriSecili)

    musteriEtiketi = tk.Label(solPanel, text="Müşteri Seçilmedi", fg="red", font=("Arial", 10, "bold"))
    musteriEtiketi.pack(pady=10)

    tk.Button(solPanel, text="SİPARİŞİ BAŞLAT", bg="green", fg="white", font=("Arial", 12),
              command=uygulama.siparisBaslat).pack(fill="x", pady=10)

    # Orta Panel
    ortaPanel = tk.LabelFrame(siparisSekmesi, text="2. Ürün Ekle")
    ortaPanel.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    tk.Label(ortaPanel, text="Ürün Ara:").pack()
    urunArama = tk.Entry(ortaPanel)
    urunArama.pack(fill="x", padx=5)
    urunArama.bind("<KeyRelease>", uygulama.urunListesiniGuncelle)

    menuListesi = tk.Listbox(ortaPanel, font=("Arial", 12))
    menuListesi.pack(fill="both", expand=True, padx=5, pady=5)

    tk.Button(ortaPanel, text="SEPETE EKLE ->", bg="orange", command=uygulama.sepeteUrunEkle).pack(pady=5)

    # Sağ Panel
    sagPanel = tk.LabelFrame(siparisSekmesi, text="3. Sepet & Ödeme")
    sagPanel.pack(side="right", fill="y", padx=5, pady=5)

    sepetListesiGorunumu = ttk.Treeview(sagPanel, columns=("urun", "adet", "fiyat"), show="headings")
    sepetListesiGorunumu.heading("urun", text="Ürün")
    sepetListesiGorunumu.heading("adet", text="Adet")
    sepetListesiGorunumu.heading("fiyat", text="Fiyat")
    sepetListesiGorunumu.column("adet", width=50)
    sepetListesiGorunumu.column("fiyat", width=70)
    sepetListesiGorunumu.pack(fill="both", expand=True)

    toplamFiyatEtiketi = tk.Label(sagPanel, text="Toplam: 0.00 TL", font=("Arial", 14, "bold"))
    toplamFiyatEtiketi.pack(pady=10)

    butonAlani = tk.Frame(sagPanel)
    butonAlani.pack(fill="x", pady=5)
    tk.Button(butonAlani, text="İPTAL ET", bg="orange", fg="black", height=2, command=uygulama.siparisiIptalEt).pack(
        side="left", fill="x", expand=True, padx=2)
    tk.Button(butonAlani, text="HESABI KAPAT", bg="red", fg="white", height=2,
              command=uygulama.siparisiKapatVeOde).pack(side="right", fill="x", expand=True, padx=2)

    uygulama.araclar['siparisMasa'] = siparisMasa
    uygulama.araclar['musteriArama'] = musteriArama
    uygulama.araclar['musteriSecim'] = musteriSecim
    uygulama.araclar['musteriEtiketi'] = musteriEtiketi
    uygulama.araclar['urunArama'] = urunArama
    uygulama.araclar['menuListesi'] = menuListesi
    uygulama.araclar['sepetListesiGorunumu'] = sepetListesiGorunumu
    uygulama.araclar['toplamFiyatEtiketi'] = toplamFiyatEtiketi

    # MÜŞTERİ KAYIT
    tk.Label(musteriSekmesi, text="Müşteri Ekle / Düzenle", font=("Arial", 12, "bold")).pack(pady=10)
    musteriFormu = tk.Frame(musteriSekmesi)
    musteriFormu.pack()

    tk.Label(musteriFormu, text="Ad Soyad:").grid(row=0, column=0, sticky="e", pady=2)
    musteriAdi = tk.Entry(musteriFormu)
    musteriAdi.grid(row=0, column=1, pady=2)

    tk.Label(musteriFormu, text="Telefon:").grid(row=1, column=0, sticky="e", pady=2)
    musteriTelefon = tk.Entry(musteriFormu)
    musteriTelefon.grid(row=1, column=1, pady=2)

    tk.Label(musteriFormu, text="E-Mail:").grid(row=2, column=0, sticky="e", pady=2)
    musteriEmail = tk.Entry(musteriFormu)
    musteriEmail.grid(row=2, column=1, pady=2)

    tk.Label(musteriFormu, text="Adres:").grid(row=3, column=0, sticky="e", pady=2)
    musteriAdres = tk.Entry(musteriFormu)
    musteriAdres.grid(row=3, column=1, pady=2)

    #butonlar için alt çerçeve
    butonCerceve = tk.Frame(musteriFormu)
    butonCerceve.grid(row=4, column=0, columnspan=2, pady=10)

    tk.Button(butonCerceve, text="Temizle", command=uygulama.musteriFormunuTemizle).pack(side="left", padx=5)
    tk.Button(butonCerceve, text="SİL", bg="red", fg="white", command=uygulama.musteriSil).pack(side="left", padx=5)

    tk.Button(butonCerceve, text="KAYDET / GÜNCELLE", bg="blue", fg="white", command=uygulama.musteriKaydet).pack(
        side="left", padx=5)

    altPanel = tk.Frame(musteriSekmesi)
    altPanel.pack(fill="both", expand=True, padx=10, pady=10)

    solFrame = tk.Frame(altPanel)
    solFrame.pack(side="left", fill="both", expand=True, padx=(0, 5))

    tk.Label(solFrame, text="Müşteri Listesi", font=("Arial", 10, "bold")).pack()

    musteriListesi = ttk.Treeview(solFrame, columns=("id", "ad", "tel", "email", "adres"), show="headings")
    musteriListesi.heading("ad", text="Ad Soyad")
    musteriListesi.heading("tel", text="Telefon")
    musteriListesi.heading("email", text="E-Mail")
    musteriListesi.heading("adres", text="Adres")

    # Sütun genişlikleri ayarı
    musteriListesi.column("id", width=0, stretch=False)
    musteriListesi.column("ad", width=100)
    musteriListesi.column("tel", width=80)
    musteriListesi.column("email", width=100)

    musteriListesi.pack(fill="both", expand=True)
    musteriListesi.bind("<<TreeviewSelect>>", uygulama.musteriDuzenlemekIcinSec)

    # SAĞ TARAF GEÇMİŞ SİPARİŞLER
    sagFrame = tk.Frame(altPanel)
    sagFrame.pack(side="right", fill="both", expand=True, padx=(5, 0))

    tk.Label(sagFrame, text="Seçili Müşterinin Geçmişi", font=("Arial", 10, "bold"), fg="blue").pack()

    gecmisSiparisListesi = ttk.Treeview(sagFrame, columns=("kod", "tarih", "tutar"), show="headings")
    gecmisSiparisListesi.heading("kod", text="Sipariş Kodu")
    gecmisSiparisListesi.heading("tarih", text="Tarih")
    gecmisSiparisListesi.heading("tutar", text="Tutar")

    gecmisSiparisListesi.column("kod", width=80)
    gecmisSiparisListesi.column("tutar", width=80)

    gecmisSiparisListesi.pack(fill="both", expand=True)

    uygulama.araclar['musteriAdi'] = musteriAdi
    uygulama.araclar['musteriTelefon'] = musteriTelefon
    uygulama.araclar['musteriEmail'] = musteriEmail
    uygulama.araclar['musteriAdres'] = musteriAdres
    uygulama.araclar['musteriListesi'] = musteriListesi
    uygulama.araclar['gecmisSiparisListesi'] = gecmisSiparisListesi

    # MENÜ DÜZENLEME
    tk.Label(menuSekmesi, text="Ürün Ekle / Düzenle", font=("Arial", 12, "bold")).pack(pady=5)
    urunFormu = tk.Frame(menuSekmesi)
    urunFormu.pack()

    tk.Label(urunFormu, text="Ürün Adı:").grid(row=0, column=0)
    urunAdi = tk.Entry(urunFormu, width=30)
    urunAdi.grid(row=0, column=1)

    tk.Label(urunFormu, text="Fiyat:").grid(row=1, column=0)
    urunFiyati = tk.Entry(urunFormu)
    urunFiyati.grid(row=1, column=1)

    tk.Label(urunFormu, text="Kategori:").grid(row=2, column=0)
    urunKategori = ttk.Combobox(urunFormu,
                                values=["Çorbalar", "Ana Yemekler", "Tatlılar", "İçecekler", "Soğuk İçecekler"])
    urunKategori.grid(row=2, column=1)

    #ÜRÜN BUTONLARI
    urunButonCerceve = tk.Frame(urunFormu)
    urunButonCerceve.grid(row=3, column=0, columnspan=2, pady=10)

    tk.Button(urunButonCerceve, text="Temizle", command=uygulama.urunFormunuTemizle).pack(side="left", padx=5)

    tk.Button(urunButonCerceve, text="SİL", bg="red", fg="white", command=uygulama.urunSil).pack(side="left", padx=5)

    tk.Button(urunButonCerceve, text="Kaydet / Güncelle", bg="blue", fg="white", command=uygulama.urunKaydet).pack(
        side="left", padx=5)

    menuDuzenleListesi = ttk.Treeview(menuSekmesi, columns=("id", "ad", "kat", "fiyat"), show="headings")
    menuDuzenleListesi.heading("ad", text="Ürün Adı")
    menuDuzenleListesi.heading("kat", text="Kategori")
    menuDuzenleListesi.heading("fiyat", text="Fiyat")
    menuDuzenleListesi.pack(fill="both", expand=True, padx=10, pady=10)
    menuDuzenleListesi.bind("<<TreeviewSelect>>", uygulama.urunDuzenlemekIcinSec)

    uygulama.araclar['urunAdi'] = urunAdi
    uygulama.araclar['urunFiyati'] = urunFiyati
    uygulama.araclar['urunKategori'] = urunKategori
    uygulama.araclar['menuDuzenleListesi'] = menuDuzenleListesi

    # Kar Hesabı
    karEtiketi = tk.Label(raporSekmesi, text="Kar Hesaplanıyor...", font=("Arial", 24))
    karEtiketi.pack(pady=50)
    tk.Button(raporSekmesi, text="Yenile", command=uygulama.karRaporunuGuncelle).pack()

    uygulama.araclar['karEtiketi'] = karEtiketi
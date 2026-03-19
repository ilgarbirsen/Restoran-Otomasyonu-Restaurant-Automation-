import tkinter as tk
import veriTabani
import arayuz
import uygulama

# Ana pencere
anaPencere = tk.Tk()
anaPencere.title("Restoran")
anaPencere.geometry("1000x700+300+50")
anaPencere.resizable(False, False)

# Veritabanını kontrolü
veriTabani.veritabaniHazirla()

# Arayüz
arayuz.arayuzuOlustur(anaPencere)

# Uygulamayı başlat
uygulama.baslat()

# Pencereyi aç
anaPencere.mainloop()

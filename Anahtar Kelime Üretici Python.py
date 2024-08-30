import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re

def anahtar_kelimeleri_bul():
    baslik = entry.get()
    
    # Google'da başlıkla ilgili arama yap
    url = f"https://www.google.com.tr/search?q={baslik}&num=10"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Google sonuçlarındaki web sayfalarını bul
    linkler = []
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('/url?q='):
            linkler.append(link['href'][7:])
    
    # Web sayfalarını indir ve anahtar kelimeleri çıkar
    anahtar_kelimeler = []
    for link in linkler:
        try:
            response = requests.get(link, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            metin = soup.get_text()
            kelimeler = re.findall(r'\b\w+\b', metin.lower())
            anahtar_kelimeler.extend(kelimeler)
        except:
            pass
    
    # En çok geçen 15 kelimeyi belirle
    en_cok_gecenler = Counter(anahtar_kelimeler).most_common(15)
    
    # Anahtar kelimeleri göster
    anahtar_kelimeler_text = ", ".join([kelime for kelime, _ in en_cok_gecenler])
    result_label.config(text="\nAnahtar kelimeler:\n" + anahtar_kelimeler_text)
    
    # Anahtar kelimeleri dosyaya kaydet
    with open("anahtar_kelimeler.txt", "a") as dosya:
        dosya.write(f"Başlık: {baslik}\n")
        dosya.write(f"Anahtar kelimeler: {anahtar_kelimeler_text}\n\n")

    messagebox.showinfo("Başarılı", "Anahtar kelimeler 'anahtar_kelimeler.txt' dosyasına kaydedildi.")

# Anahtar kelimeleri kopyalama fonksiyonu
def anahtar_kelimeleri_kopyala():
    anahtar_kelimeler = result_label.cget("text")
    root.clipboard_clear()
    root.clipboard_append(anahtar_kelimeler)

# Ana pencere oluştur
root = tk.Tk()
root.title("Anahtar Kelime Bulucu")

# Başlık giriş alanı
label = tk.Label(root, text="Başlık:")
label.pack(pady=5)
entry = tk.Entry(root)
entry.pack(pady=5)

# Anahtar kelime bul butonu
button = tk.Button(root, text="Anahtar Kelimeleri Bul", command=anahtar_kelimeleri_bul)
button.pack(pady=5)

# Sonuçları gösterme alanı
result_label = tk.Label(root, text="", wraplength=400, justify="left")
result_label.pack(pady=5)

# Anahtar kelimeleri kopyala butonu
copy_button = tk.Button(root, text="Anahtar Kelimeleri Kopyala", command=anahtar_kelimeleri_kopyala)
copy_button.pack(pady=5)

# Pencereyi göster
root.mainloop()

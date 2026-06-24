"""
Kalori Takip Uygulaması — Python (Flask) backend  [DEMO MOD]
------------------------------------------------------------
Özellikler:
  • Fotoğraftan öğün analizi (demo: yerel yemek veritabanından tutarlı sonuç)
  • Listeden yemek seçme
  • Öğünleri güne kaydetme (geçmiş)
  • Günlük toplam kalori/protein takibi
  • Hedef kalori belirleme ve kalan kaloriyi gösterme

Veriler basit bir JSON dosyasında (veri.json) saklanır; veritabanı gerektirmez.

Çalıştırmak için:
    1) python3 -m pip install -r requirements.txt
    2) python3 app.py
    3) Telefon ve bilgisayar aynı Wi-Fi'da olsun; terminalde yazan adresi
       (örn. http://172.20.10.2:5001) telefonun tarayıcısında aç.
"""

import hashlib
import json
import os
import time
from datetime import datetime

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DEMO_MOD = True

# Verilerin saklanacağı dosya (proje klasörünün içinde).
VERI_DOSYASI = os.path.join(os.path.dirname(__file__), "veri.json")

# Gerçek (ortalama) besin değerleriyle bir yemek veritabanı.
# Değerler bir porsiyon içindir; kaynak: genel beslenme tabloları.
YEMEK_VERITABANI = [
    # --- Ana Yemekler ---
    {"yemek_adi": "Tavuklu Pilav",        "porsiyon": "1 tabak (~350g)", "kalori": 520, "protein": 32, "karbonhidrat": 65, "yag": 14, "notlar": "Protein açısından zengin, dengeli bir öğün."},
    {"yemek_adi": "Izgara Köfte",         "porsiyon": "4 adet (~200g)",  "kalori": 430, "protein": 34, "karbonhidrat": 6,  "yag": 30, "notlar": "Yüksek protein, yağ oranına dikkat."},
    {"yemek_adi": "Etli Nohut + Pilav",   "porsiyon": "1 tabak (~400g)", "kalori": 610, "protein": 30, "karbonhidrat": 80, "yag": 18, "notlar": "Doyurucu, protein ve lif dengeli."},
    {"yemek_adi": "Izgara Tavuk Göğsü",   "porsiyon": "1 adet (~200g)",  "kalori": 330, "protein": 50, "karbonhidrat": 0,  "yag": 14, "notlar": "Çok yüksek protein, düşük karbonhidrat."},
    {"yemek_adi": "Izgara Köfte + Pilav", "porsiyon": "1 tabak (~400g)", "kalori": 680, "protein": 38, "karbonhidrat": 60, "yag": 32, "notlar": "Doyurucu klasik bir ana yemek."},
    {"yemek_adi": "Kuru Fasulye + Pilav", "porsiyon": "1 tabak (~400g)", "kalori": 590, "protein": 22, "karbonhidrat": 88, "yag": 16, "notlar": "Bitkisel protein ve lif kaynağı."},
    {"yemek_adi": "Karnıyarık",           "porsiyon": "2 adet (~300g)",  "kalori": 420, "protein": 18, "karbonhidrat": 24, "yag": 28, "notlar": "Patlıcan ve kıymalı geleneksel yemek."},
    {"yemek_adi": "İskender Kebap",       "porsiyon": "1 porsiyon",      "kalori": 780, "protein": 42, "karbonhidrat": 55, "yag": 44, "notlar": "Yüksek kalorili, yağ ve protein zengini."},
    {"yemek_adi": "Adana Kebap + Lavaş",  "porsiyon": "1 porsiyon",      "kalori": 720, "protein": 40, "karbonhidrat": 48, "yag": 42, "notlar": "Acılı, yüksek proteinli kebap."},
    {"yemek_adi": "Tavuk Döner Dürüm",    "porsiyon": "1 adet",          "kalori": 560, "protein": 28, "karbonhidrat": 58, "yag": 24, "notlar": "Pratik ve doyurucu bir öğün."},
    {"yemek_adi": "Et Döner Dürüm",       "porsiyon": "1 adet",          "kalori": 640, "protein": 32, "karbonhidrat": 56, "yag": 32, "notlar": "Kırmızı et içerir, kalorisi yüksektir."},
    {"yemek_adi": "Lahmacun",             "porsiyon": "2 adet",          "kalori": 500, "protein": 22, "karbonhidrat": 64, "yag": 18, "notlar": "İnce hamur, kıymalı; ölçülü tüketilebilir."},
    {"yemek_adi": "Mantı (yoğurtlu)",     "porsiyon": "1 tabak (~300g)", "kalori": 560, "protein": 24, "karbonhidrat": 70, "yag": 20, "notlar": "Hamur ağırlıklı, yoğurtlu klasik."},
    {"yemek_adi": "Karışık Pizza",        "porsiyon": "2 dilim (~250g)", "kalori": 600, "protein": 24, "karbonhidrat": 70, "yag": 26, "notlar": "Kalorisi yüksek, ara sıra tercih edilmeli."},
    {"yemek_adi": "Hamburger + Patates",  "porsiyon": "1 menü",          "kalori": 850, "protein": 35, "karbonhidrat": 88, "yag": 42, "notlar": "Yüksek kalorili fast-food öğünü."},
    {"yemek_adi": "Spagetti Bolonez",     "porsiyon": "1 tabak (~400g)", "kalori": 560, "protein": 26, "karbonhidrat": 78, "yag": 16, "notlar": "Karbonhidrat ağırlıklı, enerji verir."},
    {"yemek_adi": "Izgara Somon",         "porsiyon": "1 fileto (~200g)","kalori": 412, "protein": 40, "karbonhidrat": 0,  "yag": 26, "notlar": "Omega-3 ve protein açısından zengin."},
    {"yemek_adi": "Sebzeli Wrap",         "porsiyon": "1 adet (~280g)",  "kalori": 380, "protein": 17, "karbonhidrat": 48, "yag": 13, "notlar": "Dengeli, taşınabilir bir öğün."},
    {"yemek_adi": "Tavuk Şiş + Bulgur",   "porsiyon": "1 tabak (~350g)", "kalori": 540, "protein": 42, "karbonhidrat": 50, "yag": 18, "notlar": "Protein ve kompleks karbonhidrat dengeli."},

    # --- Çorbalar ---
    {"yemek_adi": "Mercimek Çorbası",     "porsiyon": "1 kase (~300ml)", "kalori": 180, "protein": 11, "karbonhidrat": 28, "yag": 4,  "notlar": "Düşük kalorili, lif ve protein kaynağı."},
    {"yemek_adi": "Ezogelin Çorbası",     "porsiyon": "1 kase (~300ml)", "kalori": 200, "protein": 9,  "karbonhidrat": 32, "yag": 5,  "notlar": "Bulgur ve mercimekli besleyici çorba."},
    {"yemek_adi": "Tavuk Çorbası",        "porsiyon": "1 kase (~300ml)", "kalori": 150, "protein": 12, "karbonhidrat": 14, "yag": 5,  "notlar": "Hafif ve doyurucu."},
    {"yemek_adi": "Yayla Çorbası",        "porsiyon": "1 kase (~300ml)", "kalori": 170, "protein": 8,  "karbonhidrat": 22, "yag": 6,  "notlar": "Yoğurt ve pirinçli, mide dostu."},

    # --- Kahvaltı ---
    {"yemek_adi": "Omlet (3 yumurta)",    "porsiyon": "1 porsiyon",      "kalori": 320, "protein": 21, "karbonhidrat": 3,  "yag": 25, "notlar": "Kahvaltı için iyi protein kaynağı."},
    {"yemek_adi": "Menemen",              "porsiyon": "1 tava (~300g)",  "kalori": 290, "protein": 14, "karbonhidrat": 16, "yag": 20, "notlar": "Yumurta, domates, biberli klasik kahvaltı."},
    {"yemek_adi": "Serpme Kahvaltı",      "porsiyon": "1 kişilik",       "kalori": 750, "protein": 28, "karbonhidrat": 60, "yag": 45, "notlar": "Zengin içerik, kalorisi yüksektir."},
    {"yemek_adi": "Kaşarlı Tost",         "porsiyon": "1 adet",          "kalori": 350, "protein": 15, "karbonhidrat": 38, "yag": 16, "notlar": "Pratik bir ara öğün."},
    {"yemek_adi": "Simit + Peynir",       "porsiyon": "1 simit + peynir","kalori": 420, "protein": 14, "karbonhidrat": 58, "yag": 14, "notlar": "Geleneksel pratik kahvaltı."},
    {"yemek_adi": "Yulaf Ezmesi (sütlü)", "porsiyon": "1 kase (~250g)",  "kalori": 280, "protein": 11, "karbonhidrat": 45, "yag": 6,  "notlar": "Lif zengini, tok tutan kahvaltı."},
    {"yemek_adi": "Peynirli Börek",       "porsiyon": "1 dilim (~150g)", "kalori": 380, "protein": 12, "karbonhidrat": 36, "yag": 22, "notlar": "Hamur işi, kalorisi yüksek."},

    # --- Salata & Hafif ---
    {"yemek_adi": "Sezar Salata",         "porsiyon": "1 tabak (~300g)", "kalori": 290, "protein": 18, "karbonhidrat": 14, "yag": 18, "notlar": "Sebze ağırlıklı, hafif bir seçim."},
    {"yemek_adi": "Çoban Salata",         "porsiyon": "1 tabak (~250g)", "kalori": 120, "protein": 3,  "karbonhidrat": 12, "yag": 7,  "notlar": "Çok düşük kalorili, sebze ağırlıklı."},
    {"yemek_adi": "Ton Balıklı Salata",   "porsiyon": "1 tabak (~300g)", "kalori": 260, "protein": 26, "karbonhidrat": 12, "yag": 12, "notlar": "Yüksek protein, düşük kalori."},
    {"yemek_adi": "Yoğurtlu Meyve Kasesi","porsiyon": "1 kase (~250g)",  "kalori": 210, "protein": 12, "karbonhidrat": 32, "yag": 4,  "notlar": "Sağlıklı atıştırmalık veya kahvaltı."},

    # --- Atıştırmalık ---
    {"yemek_adi": "Patates Kızartması",   "porsiyon": "1 orta (~150g)",  "kalori": 430, "protein": 5,  "karbonhidrat": 56, "yag": 21, "notlar": "Yağ oranı yüksek atıştırmalık."},
    {"yemek_adi": "Bir Avuç Karışık Kuruyemiş","porsiyon": "~30g",      "kalori": 180, "protein": 6,  "karbonhidrat": 6,  "yag": 16, "notlar": "Sağlıklı yağ ve protein kaynağı."},
    {"yemek_adi": "Muz",                  "porsiyon": "1 orta (~120g)",  "kalori": 105, "protein": 1,  "karbonhidrat": 27, "yag": 0,  "notlar": "Hızlı enerji ve potasyum kaynağı."},
    {"yemek_adi": "Elma",                 "porsiyon": "1 orta (~180g)",  "kalori": 95,  "protein": 0,  "karbonhidrat": 25, "yag": 0,  "notlar": "Düşük kalorili, lifli atıştırmalık."},

    # --- Tatlı & İçecek ---
    {"yemek_adi": "Künefe",               "porsiyon": "1 porsiyon",      "kalori": 500, "protein": 10, "karbonhidrat": 60, "yag": 25, "notlar": "Şerbetli tatlı, kalorisi yüksek."},
    {"yemek_adi": "Sütlaç",               "porsiyon": "1 kase (~200g)",  "kalori": 250, "protein": 7,  "karbonhidrat": 42, "yag": 6,  "notlar": "Sütlü tatlı, ölçülü tüketilmeli."},
    {"yemek_adi": "Baklava",              "porsiyon": "2 dilim (~100g)", "kalori": 380, "protein": 6,  "karbonhidrat": 45, "yag": 20, "notlar": "Çok şekerli, kalorisi yüksek tatlı."},
    {"yemek_adi": "Ayran",                "porsiyon": "1 bardak (~250ml)","kalori": 90, "protein": 5,  "karbonhidrat": 7,  "yag": 5,  "notlar": "Yoğurt bazlı, ferahlatıcı içecek."},
    {"yemek_adi": "Türk Kahvesi (sade)",  "porsiyon": "1 fincan",        "kalori": 5,   "protein": 0,  "karbonhidrat": 1,  "yag": 0,  "notlar": "Neredeyse kalorisiz (şekersiz)."},
    {"yemek_adi": "Kola",                 "porsiyon": "1 kutu (330ml)",  "kalori": 139, "protein": 0,  "karbonhidrat": 35, "yag": 0,  "notlar": "Tamamen şeker, besin değeri yok."},
]


# ---------------------------------------------------------------------------
# Veri okuma / yazma yardımcıları
# ---------------------------------------------------------------------------
def veri_oku():
    """veri.json dosyasını okur; yoksa varsayılan bir yapı döner."""
    if not os.path.exists(VERI_DOSYASI):
        return {"hedef": 2000, "kayitlar": []}
    try:
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"hedef": 2000, "kayitlar": []}


def veri_yaz(veri):
    """Veriyi veri.json dosyasına kaydeder."""
    with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=2)


def bugun():
    """Bugünün tarihini 'YYYY-AA-GG' formatında döner."""
    return datetime.now().strftime("%Y-%m-%d")


def bugunun_ozeti(veri):
    """Bugüne ait kayıtları ve toplamları hesaplar."""
    bugunku = [k for k in veri["kayitlar"] if k.get("tarih") == bugun()]
    toplam = {
        "kalori": sum(k.get("kalori", 0) for k in bugunku),
        "protein": sum(k.get("protein", 0) for k in bugunku),
        "karbonhidrat": sum(k.get("karbonhidrat", 0) for k in bugunku),
        "yag": sum(k.get("yag", 0) for k in bugunku),
    }
    hedef = veri.get("hedef", 2000)
    return {
        "tarih": bugun(),
        "hedef": hedef,
        "kalan": hedef - toplam["kalori"],
        "toplam": toplam,
        "kayitlar": bugunku,
    }


# ---------------------------------------------------------------------------
# Sayfalar ve API uç noktaları
# ---------------------------------------------------------------------------
@app.route("/")
def ana_sayfa():
    return render_template("index.html", demo=DEMO_MOD)


@app.route("/yemekler")
def yemekler():
    """Listeden seçme için yemek veritabanını döner."""
    return jsonify(YEMEK_VERITABANI)


@app.route("/analiz", methods=["POST"])
def analiz():
    """
    Yüklenen fotoğrafı 'analiz eder'. DEMO MODunda fotoğrafın içeriğinden bir
    parmak izi (hash) çıkarıp veritabanından tutarlı bir yemek seçer.
    """
    if "foto" not in request.files:
        return jsonify({"hata": "Fotoğraf bulunamadı."}), 400

    dosya = request.files["foto"]
    resim_baytlari = dosya.read()
    if not resim_baytlari:
        return jsonify({"hata": "Boş dosya."}), 400

    time.sleep(1.2)  # gerçek analiz hissi için kısa bekleme

    parmak_izi = hashlib.sha256(resim_baytlari).hexdigest()
    indeks = int(parmak_izi, 16) % len(YEMEK_VERITABANI)
    yemek = dict(YEMEK_VERITABANI[indeks])
    yemek["guven"] = round(0.78 + (int(parmak_izi[:2], 16) % 20) / 100, 2)
    return jsonify(yemek)


@app.route("/kaydet", methods=["POST"])
def kaydet():
    """Bir öğünü bugünün geçmişine ekler."""
    g = request.get_json(silent=True) or {}
    if not g.get("yemek_adi"):
        return jsonify({"hata": "Geçersiz öğün."}), 400

    kayit = {
        "tarih": bugun(),
        "zaman": datetime.now().strftime("%H:%M"),
        "yemek_adi": g.get("yemek_adi"),
        "kalori": int(g.get("kalori", 0)),
        "protein": int(g.get("protein", 0)),
        "karbonhidrat": int(g.get("karbonhidrat", 0)),
        "yag": int(g.get("yag", 0)),
    }
    veri = veri_oku()
    veri["kayitlar"].append(kayit)
    veri_yaz(veri)
    return jsonify(bugunun_ozeti(veri))


@app.route("/gecmis")
def gecmis():
    """Bugünün öğünlerini ve toplamlarını döner."""
    return jsonify(bugunun_ozeti(veri_oku()))


@app.route("/hedef", methods=["POST"])
def hedef_ayarla():
    """Günlük hedef kaloriyi günceller."""
    g = request.get_json(silent=True) or {}
    try:
        yeni_hedef = int(g.get("hedef", 2000))
    except (TypeError, ValueError):
        return jsonify({"hata": "Geçersiz hedef."}), 400

    veri = veri_oku()
    veri["hedef"] = max(0, yeni_hedef)
    veri_yaz(veri)
    return jsonify(bugunun_ozeti(veri))


@app.route("/sil", methods=["POST"])
def sil():
    """Bugünün geçmişinden bir öğünü siler (zaman + isim ile)."""
    g = request.get_json(silent=True) or {}
    veri = veri_oku()
    veri["kayitlar"] = [
        k for k in veri["kayitlar"]
        if not (k.get("tarih") == bugun()
                and k.get("zaman") == g.get("zaman")
                and k.get("yemek_adi") == g.get("yemek_adi"))
    ]
    veri_yaz(veri)
    return jsonify(bugunun_ozeti(veri))


if __name__ == "__main__":
    # macOS'ta 5000 portu "AirPlay Receiver" tarafından kullanılır, 5001 kullanıyoruz.
    app.run(host="0.0.0.0", port=5001, debug=True)

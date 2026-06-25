AD :Talha Yalçın
Öğrenci No :24010502133
Proje Amacı : Günlük Kalori İhtiyacını Takip etme ve hesaplayarak kolaylık sağlama


# 🍽️ Kalori Takip Uygulaması (Demo Mod)

Yemek fotoğrafı çek, uygulama öğünün tahmini **kalori, protein, karbonhidrat ve
yağ** değerlerini göstersin. Python (Flask) ile yazıldı.

## Özellikler

- 📷 **Fotoğraftan analiz** — yemeğin fotoğrafını çek, besin değerlerini gör
- 📋 **Listeden seçme** — fotoğraf yerine hazır listeden yemek seç
- ➕ **Güne ekleme** — öğünleri günlük geçmişe kaydet
- 📊 **Günlük takip** — toplam kalori, protein, karbonhidrat, yağ
- 🎯 **Hedef kalori** — günlük hedef belirle, kalan kaloriyi ve ilerleme çubuğunu gör
- 🗓️ **Geçmiş** — bugünün öğünlerini listele, tek tek sil

Veriler `veri.json` dosyasında saklanır (veritabanı gerektirmez).

## Nasıl çalışır?

1. Telefonun tarayıcısından uygulamayı açarsın.
2. Fotoğraf çekerek ya da listeden seçerek bir öğün analiz edersin.
3. "Güne Ekle" ile öğünü kaydedersin.
4. Üstteki özet kartında günlük toplamın ve hedefe göre kalan kalorin güncellenir.

## Kurulum

### 1) Gerekli paketleri yükle
```bash
cd kalori-takip
python3 -m pip install -r requirements.txt
```
> Not: Bu Mac'te `pip` yerine `python3 -m pip`, `python` yerine `python3` kullan.

### 2) Çalıştır
```bash
python3 app.py
```

Terminalde şuna benzer iki adres göreceksin:
```
Running on http://127.0.0.1:5001        <- kendi bilgisayarın
Running on http://172.20.10.2:5001      <- telefon için bu adresi kullan
```

### 3) Telefonda aç
- Telefon ve bilgisayar **aynı Wi-Fi ağında** olmalı.
- Telefonun tarayıcısına terminalde çıkan ikinci adresi yaz (örn. `http://172.20.10.2:5001`).
- İstersen tarayıcı menüsünden "Ana ekrana ekle" diyerek uygulama gibi kullanabilirsin.

> ⚠️ macOS'ta 5000 portu "AirPlay Receiver" tarafından kullanıldığı için uygulama
> **5001** portunda çalışır.

## Proje dosyaları

| Dosya | Açıklama |
|-------|----------|
| `app.py` | Python backend — fotoğrafı alır, veritabanından sonucu seçer ve döner |
| `templates/index.html` | Mobil arayüz (kamera + sonuç ekranı) |
| `requirements.txt` | Gerekli Python paketleri |

## İleride gerçek yapay zeka eklemek istersen
`app.py` içindeki `analiz()` fonksiyonundaki demo seçimini bir vision API
çağrısıyla (örn. Google Gemini ücretsiz katmanı veya Anthropic Claude) değiştirmen
yeterli. Yapı buna hazır.

## Önemli not
Demo moddaki değerler örnek/ortalama tahminlerdir, tıbbi kesinlik taşımaz.
Okul/eğitim amaçlıdır.

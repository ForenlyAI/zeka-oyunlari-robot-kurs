# Zekâ Oyunları ve Robot Bulmacaları — kurs dosyaları

Forenly AI Academy'deki **Zekâ Oyunları ve Robot Bulmacaları** kursunun hesap dosyaları. Derslerde ekranda gördüğünüz her Python oturumu ve her çizim bu betiklerle üretildi: en kısa yollar, mini sudoku, kedi-fare-peynir geçişi, örüntüler, anagram ve şifre, hafıza oyunu, XOX oyun ağacı, şeker küpü oyunu, mangala, tangram, pentomino, küp açınımı ve ayna simetrisi bilgisayarla gerçekten çözülür ve sayılır. Oyun türleri Millî Eğitim Bakanlığının Zekâ Oyunları Modülünden (2026, Düzey I), her ders ayrıca 4. sınıf matematik programındaki (2018) bir kazanıma bağlıdır; kodlar `kaynaklar.py` içinde (`PROGRAM`).

Betikleri çalıştırmak kursu izlemek için şart değildir; isteyen veli ya da öğrenci sayıları değiştirip (masaların yeri, sudoku ipuçları, küp sayısı…) sonucu kendisi görebilir. Programlama bilmek gerekmez.

## Gerekenler

- **Python 3.10 veya üstü**, `numpy`, `matplotlib` ve `pillow`. Hepsi ücretsizdir.
- Kurulum: `python -m pip install -r requirements.txt`
- Bilgisayarınıza kurmak istemezseniz tarayıcıda çalışan bir not defterine (ör. Google Colab) bu klasörü yükleyip aynı betikleri çalıştırabilirsiniz.

## Nasıl çalıştırılır

1. Bu depoyu indirin (Code → Download ZIP) ve klasörde bir terminal açın.
2. Haftaları çalıştırın: `python hafta1.py`, `python hafta2.py`, `python hafta3.py`, `python hafta4.py` (her biri birkaç saniye sürer).
3. Betikler çalışınca `ekran/<ders>/` klasöründe derslerdeki çizimler (`.png`) ve Python oturum kayıtları (`.txt`), kökte de ölçülen sayılar (`OLCUMLER.json`) oluşur.
4. İsteğe bağlı: `python komut_ciz.py` oturum kayıtlarını derslerdeki gibi resme çizer (Linux'taki DejaVu yazı tipini kullanır).

## Sonucunuzu karşılaştırın

`beklenen/OLCUMLER.json` ekibimizin 2026-10-10 koşumunda ölçtüğü sayılardır. Rastgele oyunlar (Ders 2.4 hafıza oyunu, Ders 3.2 XOX, Ders 3.3 şeker küpü) sabit bir tohumla (2026) oynatılır, bu yüzden sizde de aynı sayılar çıkmalıdır.

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ortak.py` | Kaydı okuma, oturum kaydı, grafik çizimi, ölçüm yazma |
| `arac.py` | Bulmaca çözücüler: en kısa yol araması, komut kartları, mini sudoku, geçiş bulmacası, XOX, şeker küpü oyunu, mangala kuralları, pentomino ve küp açınımı |
| `kaynaklar.py` | Resmî belgeler (MEB Zekâ Oyunları Modülü, 4. sınıf matematik programı, mangala turnuva kuralları) ve ders–program eşlemesi |
| `hafta1.py` | Mantık ve yol bulma: robotun yolu, komut kartları, mini sudoku, kedi-fare-peynir |
| `hafta2.py` | Örüntü, şifre ve hafıza: sayı ve şekil örüntüleri, anagram ve kaydırma şifresi, hafıza oyunu |
| `hafta3.py` | Strateji oyunları: XOX oyun ağacı, kaybetmeyen robot, şeker küpü oyunu, mangala |
| `hafta4.py` | Şekil ve uzay: tangram, pentomino, küp açınımı, ayna simetrisi |
| `komut_ciz.py` | Oturum kayıtlarını resme çizer (isteğe bağlı) |
| `veri/cay_servisi_kaydi.csv` | Kafede çay servisi benzetim kaydı: zaman, kol eklem açıları, dirsek hızı, bardağın konumu (saniyede 50 örnek) |
| `veri/sag_kol_parametre.csv` | Sağ kol benzetim parametreleri (eklem adları ve sınırları) |
| `veri/sag_kol_kutle.csv` | Sağ kol parça kütleleri (bu kursta kullanılmıyor, veri bütünlüğü için duruyor) |

## Veri ve sayılar hakkında

Robot verisi **benzetim kaydıdır**, gerçek robot ölçümü değildir. Kafe ızgarasının boyu bardağın kayıttaki yer değiştirmesinden gelir; masaların yeri, yarım metrelik kare, sudoku ipuçları, tepsi sırası ve tepsi ölçüleri **ÖRNEKTİR** ve kodda böyle yazılıdır. Hafıza oyunu ve maçlar bilgisayarda benzetildi, gerçek oyuncu verisi değildir.

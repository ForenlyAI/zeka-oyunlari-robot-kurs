"""Zekâ Oyunları ve Robot Bulmacaları — kursta anılan resmî belgeler ve öğretim programı eşlemesi.
Her satır gerçek bir yayındır; künye ve içerik 2026-10-10'da yayıncının sitesinden indirilip okunarak denetlendi.
Bulmaca sonuçları (yol sayısı, çözüm sayısı, oyun ağacı…) kaynaktan alınmadı, lab/arac.py ile hesaplandı.
Kayıttan, hesaptan ya da bu dosyadaki kaynaklardan gelmeyen her sayı derslerde ÖRNEK diye işaretlenir."""

KAYNAKLAR = [
    dict(anahtar="meb_zeka_2026", yazar="T.C. Millî Eğitim Bakanlığı, Talim ve Terbiye Kurulu Başkanlığı", yil=2026,
         baslik="Ortaokul Oyun ve Oyun Etkinlikleri Dersi Öğretim Programı — Zekâ Oyunları Modülü",
         yer="https://mufredat.meb.gov.tr/Dosyalar/2026814101535114-zeka oyunları modülü.pdf",
         dogrulama="PDF indirildi (51 sayfa) ve okundu: Türkiye Yüzyılı Maarif Modeli'ne göre hazırlanmış, Düzey I ve Düzey II. "
                   "Düzey I (2 saat) temaları: Geometrik-Mekanik Oyunlar (5 öğrenme çıktısı, 13 saat), Sözel Oyunlar (5, 11), "
                   "Akıl Yürütme ve İşlem Oyunları (4, 13), Strateji Oyunları (4, 13), Hafıza Oyunları (3, 9), Zekâ Soruları (4, 9). "
                   "Örnek oyun listeleri: tangram, pentomino, labirentler (Tema 1); anagram, şifre oyunları (Tema 2); sudoku (Tema 3); "
                   "mangala, Tic-Tac-Toe, Nim (Tema 4); resim eşleme, yön bulma (Tema 5); kurt, kuzu ve ot (Tema 6). "
                   "Öğrenme çıktısı kodları OOEZO.1.x.y (Düzey I) bu belgeden",
         derste="bütün dersler — ünite türleri ve öğrenme çıktısı kodları"),
    dict(anahtar="meb_zeka_2013", yazar="T.C. Millî Eğitim Bakanlığı, Talim ve Terbiye Kurulu Başkanlığı", yil=2013,
         baslik="Ortaokul ve İmam Hatip Ortaokulu Zekâ Oyunları Dersi Öğretim Programı (5, 6, 7 ve 8. Sınıflar)",
         yer="https://imo.firat.edu.tr/subdomain_files/imo.firat.edu.tr/files/2652/202152512057724-zeka_oyunlari.pdf",
         dogrulama="PDF indirildi (33 sayfa); kapakta 'T.C. Millî Eğitim Bakanlığı Talim ve Terbiye Kurulu Başkanlığı, Ankara 2013'. "
                   "Kopya bir üniversite sitesinde duruyor (MEB adresi bulunamadı); yalnız seçmeli dersin 2013'te açıldığını göstermek için",
         derste="0.1 — dersin geçmişi (5–8. sınıf seçmeli ders)"),
    dict(anahtar="meb_mat_2018", yazar="T.C. Millî Eğitim Bakanlığı, Talim ve Terbiye Kurulu Başkanlığı", yil=2018,
         baslik="Matematik Dersi Öğretim Programı (İlkokul ve Ortaokul 1, 2, 3, 4, 5, 6, 7 ve 8. Sınıflar)",
         yer="https://mufredat.meb.gov.tr/Dosyalar/201813017165445-MATEMATİK ÖĞRETİM PROGRAMI 2018v.pdf",
         dogrulama="PDF indirildi (80 sayfa); 4. sınıf kazanımları okundu: M.4.1.1.6 sayı örüntüleri (aralarındaki fark sabit), "
                   "M.4.2.1.1 üçgen, kare, dikdörtgen, M.4.2.1.4 açınımı verilen küpü oluşturur, M.4.2.2.1–2 ayna simetrisi, "
                   "M.4.2.3.4 dar, dik, geniş açı, M.4.3.3.1–2 alan (birim kare, çarpma), M.4.1.5 bölme, M.4.4.1 veri (sütun grafiği)",
         derste="her dersin 4. sınıf matematik bağlantısı (harita.py PROGRAM)"),
    dict(anahtar="tymm_takvim", yazar="T.C. Millî Eğitim Bakanlığı", yil=2026,
         baslik="Türkiye Yüzyılı Maarif Modeli — Taslak Çerçeve Planları, Temel Eğitim",
         yer="https://tymm.meb.gov.tr/taslak-cerceve-planlari/temel-egitim",
         dogrulama="sayfada '2026-2027 eğitim öğretim yılında 1, 2, 3 ve 5, 6, 7. sınıflarda Türkiye Yüzyılı Maarif Modeli Öğretim "
                   "Programları uygulanacaktır' cümlesi okundu (2026-10-10); 4. sınıf bu yıl 2018 matematik programıyla okutulur",
         derste="course.yml — 4. sınıf matematik bağlantısı için hangi programın esas alındığı"),
    dict(anahtar="mangala_kural", yazar="Tüm Akıl ve Zekâ Oyunları Federasyonu (MEB il müdürlüğü sitesinde yayımlanan turnuva belgesi)", yil=2023,
         baslik="Türkiye Akıl ve Zekâ Oyunları Turnuvası — Mangala Turnuva Kuralları",
         yer="https://yunusemre.meb.gov.tr/meb_iys_dosyalar/2023_01/13171831_MANGALA_TURNUVA_KURALLARI.pdf",
         dogrulama="PDF indirildi (2 sayfa) ve okundu: 12 küçük kuyu, 2 hazine, 48 taş, her kuyuda 4; dört temel kural "
                   "(ilk taş aldığın kuyuya, sağa doğru dağıt; son taş hazineye düşerse tekrar oyna; rakip kuyusu çift olursa al; "
                   "kendi boş kuyuna düşerse karşıdakini al; bölgesi ilk biten rakibin taşlarını da alır). lab/arac.py mangala_hamle bu kurallarla",
         derste="3.4 — mangala"),
]

# Ders → öğretim programı eşlemesi. Birincil: MEB Zekâ Oyunları Modülü (2026) Düzey I öğrenme çıktıları (OOEZO.1.x.y).
# İlkokul için resmî bir zekâ oyunları programı bulunamadı (planlama/ACIK-SORULAR.md Q1); 9–10 yaşa uyarlandı ve her ders
# 4. sınıf matematik programındaki (2018) bir kazanıma da bağlandı.
PROGRAM = {
    "1.1": "OOEZO.1.1.3 geometrik-mekanik oyunlar oynayabilme (labirentler) · 4. sınıf M.4.3.1 uzunluk ölçme",
    "1.2": "OOEZO.1.6.3 zekâ sorularında temel stratejileri uygulayabilme · 4. sınıf M.4.2.3.4 dik açı",
    "1.3": "OOEZO.1.3.2–1.3.3 akıl yürütme ve işlem oyunları (sudoku) · 4. sınıf M.4.1.5.7 eşitlikte verilmeyen değer",
    "1.4": "OOEZO.1.6.4 zekâ sorularında tümdengelimsel akıl yürütme (kurt, kuzu ve ot) · 4. sınıf M.4.1.2.4 problem çözme",
    "2.1": "OOEZO.1.3.2 ipuçlarından mantıksal çıkarım · 4. sınıf M.4.1.1.6 sayı örüntüleri",
    "2.2": "OOEZO.1.1.5 duruma ilişkin örüntüyü bulma ve genelleme · 4. sınıf M.4.1.1.6 örüntü, adım sayısı",
    "2.3": "OOEZO.1.2.3–1.2.4 sözel oyunlar (anagram, şifre oyunları) · 4. sınıf M.4.1.4.6 çarpma problemi",
    "2.4": "OOEZO.1.5.2–1.5.3 hafıza oyunları (resim eşleme) · 4. sınıf M.4.4.1.1 sütun grafiğini yorumlama",
    "3.1": "OOEZO.1.4.1–1.4.2 strateji oyunlarının kuralları ve hamle planlaması (Tic-Tac-Toe) · 4. sınıf M.4.1.4.6 çarpma",
    "3.2": "OOEZO.1.4.3–1.4.4 temel strateji, taktik ve strateji geliştirme · 4. sınıf M.4.4.1.4 grafikle problem çözme",
    "3.3": "OOEZO.1.4.3 strateji oyunlarına özgü temel strateji (Nim) · 4. sınıf M.4.1.5 bölme ve kalan",
    "3.4": "OOEZO.1.4.1–1.4.4 strateji oyunları (mangala) · 4. sınıf M.4.1.2.4 toplama problemi",
    "4.1": "OOEZO.1.1.2–1.1.3 geometrik şekilleri tanıma, tangram · 4. sınıf M.4.2.1.1 üçgen ve kare, M.4.3.3.1 alan",
    "4.2": "OOEZO.1.1.3 şekil oluşturma oyunları (pentomino) · 4. sınıf M.4.3.3.2 alan ve çarpma",
    "4.3": "OOEZO.1.1.4 üç boyutlu cisimler arasında ilişki · 4. sınıf M.4.2.1.4 açınımı verilen küp",
    "4.4": "OOEZO.1.1.5 tümevarımsal akıl yürütme · 4. sınıf M.4.2.2.1–M.4.2.2.2 ayna simetrisi",
}

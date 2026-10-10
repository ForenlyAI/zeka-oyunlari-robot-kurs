"""Hafta 1 · Mantık ve Yol Bulma — Ders 1.1–1.4.
  python hafta1.py   → ekran/1.x/*.txt + *.png, OLCUMLER.json (d1_*)"""
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch
from ortak import kayit, olc, oturum, grafik, eksen, MAVI, TURUNCU, YESIL, MOR, GRI
import arac as A

KAHVE = "#92400e"


def izgara_ciz(ax, iz, yol=None, renk=TURUNCU, etiket=True):
    for x in range(iz["en"]):
        for y in range(iz["boy"]):
            masa = (x, y) in iz["masalar"]
            ax.add_patch(Rectangle((x, y), 1, 1, fc=KAHVE if masa else "#f8fafc", ec="#cbd5e1", lw=2, alpha=0.85 if masa else 1))
            if masa and etiket:
                ax.text(x + 0.5, y + 0.5, "masa", ha="center", va="center", color="white", fontsize=17)
    if yol:
        xs = [p[0] + 0.5 for p in yol]; ys = [p[1] + 0.5 for p in yol]
        ax.plot(xs, ys, color=renk, lw=8, solid_capstyle="round", zorder=3)
    for (p, ad, r) in ((iz["bas"], "BAŞLA", MAVI), (iz["son"], "BİTİŞ", YESIL)):
        ax.add_patch(FancyBboxPatch((p[0] + 0.12, p[1] + 0.12), 0.76, 0.76, boxstyle="round,pad=0.02", fc=r, ec="none", zorder=4))
        ax.text(p[0] + 0.5, p[1] + 0.5, ad, ha="center", va="center", color="white", fontsize=17 if etiket else 13, weight="bold", zorder=5)
    ax.set_xlim(-0.1, iz["en"] + 0.1); ax.set_ylim(-0.1, iz["boy"] + 0.1); ax.set_aspect("equal"); ax.axis("off")


# ---------- 1.1 Robotun Yolunu Bul (OOEZO.1.1.3 labirentler · M.4.3.1) ----------
def ders_1_1():
    ns = oturum("1.1", "kafe-izgarasi", """
from ortak import kayit
import arac
iz = arac.kafe_izgarasi()          # kareler yarım metre (ÖRNEK)
iz["en"], iz["boy"]                 # sütun ve satır sayısı
iz["bas"], iz["son"]                # bardağın ilk ve son yeri (benzetim kaydı)
iz["masalar"]                       # masaların yeri ÖRNEK
""")
    ns = oturum("1.1", "en-kisa-yol", """
uzunluk, yol_sayisi, incelenen, _ = arac.bfs(iz, engel=False)
uzunluk, yol_sayisi                 # masa yokken
uzunluk, yol_sayisi, incelenen, _ = arac.bfs(iz)
uzunluk, yol_sayisi, incelenen      # masalar varken
""", ns)
    iz = ns["iz"]
    yollar = A.en_kisa_yollar(iz)
    bos_uz, bos_say, _, _ = A.bfs(iz, engel=False)
    uz, say, inc, _ = A.bfs(iz)

    def ciz(fig):
        ax = fig.add_axes([0.03, 0.06, 0.55, 0.78])
        izgara_ciz(ax, iz, yollar[0])
        for y in yollar[1:]:
            ax.plot([p[0] + 0.5 for p in y], [p[1] + 0.5 for p in y], color=TURUNCU, lw=3, alpha=0.35, zorder=2)
        fig.text(0.62, 0.74, f"En kısa yol: {uz} adım", fontsize=34, color=TURUNCU, weight="bold")
        fig.text(0.62, 0.64, f"Farklı en kısa yol: {say}", fontsize=30)
        fig.text(0.62, 0.55, f"Masa olmasaydı: {bos_say} yol", fontsize=26, color=GRI)
        fig.text(0.62, 0.46, f"Bir adım = yarım metre (ÖRNEK)", fontsize=22, color=GRI)
        fig.text(0.62, 0.38, "Başla ve bitiş: bardağın benzetim", fontsize=22, color=GRI)
        fig.text(0.62, 0.34, "kaydındaki ilk ve son yeri", fontsize=22, color=GRI)
        fig.text(0.62, 0.26, "Masaların yeri ÖRNEK", fontsize=22, color=GRI)
    grafik("1.1", "yol-haritasi", "Kafede bardağı taşıyan robot: en kısa yol kaç adım?", ciz)
    olc(d1_1_en=iz["en"], d1_1_boy=iz["boy"], d1_1_masa=len(iz["masalar"]), d1_1_bas=list(iz["bas"]), d1_1_son=list(iz["son"]),
        d1_1_bos_uzunluk=bos_uz, d1_1_bos_yol=bos_say, d1_1_uzunluk=uz, d1_1_yol=say, d1_1_incelenen=inc,
        d1_1_metre=uz * A.HUCRE_M)


# ---------- 1.2 Komut Kartları (OOEZO.1.6.3 · M.4.2.3.4 dik açı) ----------
def ders_1_2():
    iz = A.kafe_izgarasi()
    yollar = A.en_kisa_yollar(iz)
    ns = oturum("1.2", "kartlar", """
import arac
iz = arac.kafe_izgarasi()
yollar = arac.en_kisa_yollar(iz)
kart = [arac.kartlar(y) for y in yollar]
sorted(len(k) for k in kart)               # her en kısa yolun kart sayısı
en_az = min(kart, key=len)
en_az
arac.sikistir(en_az)                        # TEKRARLA kartıyla
len(arac.sikistir(en_az))
""")
    en_az, en_cok = min(ns["kart"], key=len), max(ns["kart"], key=len)
    sik = A.sikistir(en_az)
    donus = sum(k != "İLERİ" for k in en_az)
    i_az = ns["kart"].index(en_az); i_cok = ns["kart"].index(en_cok)

    def ciz(fig):
        for j, (ad, k, yi, r) in enumerate([("En az kartlı yol", en_az, i_az, YESIL), ("En çok kartlı yol", en_cok, i_cok, MOR)]):
            ax = fig.add_axes([0.02 + j * 0.5, 0.33, 0.44, 0.5])
            izgara_ciz(ax, iz, yollar[yi], renk=r, etiket=False)
            ax.set_title(f"{ad}: {len(k)} kart", fontsize=28, color=r)
            satir = "  ".join("↑" if x == "İLERİ" else ("↰" if x == "SOLA DÖN" else "↱") for x in k)
            fig.text(0.24 + j * 0.5, 0.2, satir, ha="center", fontsize=30, family="DejaVu Sans")
        fig.text(0.5, 0.08, "↑ İLERİ (yarım metre)   ↰ SOLA DÖN   ↱ SAĞA DÖN   · her dönüş bir dik açı · robot doğuya bakarak başlar",
                 ha="center", fontsize=20, color=GRI)
    grafik("1.2", "kart-dizisi", "Aynı uzunlukta iki yol, farklı sayıda komut kartı", ciz)
    olc(d1_2_yol_sayisi=len(yollar), d1_2_kart_az=len(en_az), d1_2_kart_cok=len(en_cok), d1_2_donus_az=donus,
        d1_2_donus_cok=sum(k != "İLERİ" for k in en_cok), d1_2_ileri=en_az.count("İLERİ"), d1_2_sikistirilmis=len(sik),
        d1_2_kartlar=en_az, d1_2_sikistir=sik, d1_2_dik_aci=90)


# ---------- 1.3 Mini Sudoku (OOEZO.1.3.3 sudoku) ----------
IPUCU = [[1, 0, 0, 0],      # ÖRNEK bulmaca: 1 çay, 2 su, 3 ayran, 4 süt — her masa sırası, sandalye sırası ve köşe bir kez
         [0, 0, 3, 0],
         [0, 4, 0, 0],
         [0, 0, 0, 2]]
SIMGE = {1: "çay", 2: "su", 3: "ayran", 4: "süt"}


def ders_1_3():
    ns = oturum("1.3", "sudoku-coz", """
import arac
ipucu = [[1, 0, 0, 0],      # ÖRNEK: 1 çay, 2 su, 3 ayran, 4 süt
         [0, 0, 3, 0],
         [0, 4, 0, 0],
         [0, 0, 0, 2]]
sum(v > 0 for satir in ipucu for v in satir)     # verilen ipucu
cozumler, deneme = arac.sudoku_coz(ipucu, hepsi=True)
len(cozumler)                                   # kaç çözüm var?
cozumler[0]
deneme                                          # robotun denediği yerleştirme
arac.sudoku_say()                               # boş 4 × 4 tablonun bütün çözümleri
""")
    coz = ns["cozumler"][0]

    def ciz(fig):
        for j, (ad, t) in enumerate([("Bulmaca (ÖRNEK ipuçları)", IPUCU), ("Robotun bulduğu tek çözüm", coz)]):
            ax = fig.add_axes([0.05 + j * 0.5, 0.1, 0.4, 0.7])
            for r in range(4):
                for c in range(4):
                    v = t[r][c]; ipucu = IPUCU[r][c] > 0
                    ax.add_patch(Rectangle((c, 3 - r), 1, 1, fc="#e0e7ff" if ipucu else "white", ec="#94a3b8", lw=2))
                    if v:
                        ax.text(c + 0.5, 3.5 - r, SIMGE[v], ha="center", va="center", fontsize=26,
                                color="#111" if ipucu else TURUNCU, weight="bold" if ipucu else "normal")
            ax.plot([2, 2], [0, 4], color="#111", lw=6); ax.plot([0, 4], [2, 2], color="#111", lw=6)
            ax.add_patch(Rectangle((0, 0), 4, 4, fill=False, ec="#111", lw=6))
            ax.set_xlim(-0.05, 4.05); ax.set_ylim(-0.05, 4.05); ax.set_aspect("equal"); ax.axis("off")
            ax.set_title(ad, fontsize=28)
        fig.text(0.5, 0.03, f"Her satırda, her sütunda ve her kalın köşede dört içecek birer kez · {len(ns['cozumler'])} çözüm · {ns['deneme']} deneme",
                 ha="center", fontsize=21, color=GRI)
    grafik("1.3", "sudoku", "Dört masa, dört içecek: mini sudoku", ciz)
    olc(d1_3_ipucu=sum(v > 0 for s in IPUCU for v in s), d1_3_cozum_sayisi=len(ns["cozumler"]),
        d1_3_deneme=ns["deneme"], d1_3_bos_cozum=A.sudoku_say(), d1_3_kutu=4)


# ---------- 1.4 Kedi, Fare ve Peynir (OOEZO.1.6.4 zekâ soruları: kurt, kuzu ve ot) ----------
def ders_1_4():
    ns = oturum("1.4", "gecis", """
import arac
arac.ESYA                  # robot tek eliyle bir şey taşır
arac.TEHLIKE               # robot yokken yan yana kalamazlar
adim, yol_sayisi, guvenli_durum, plan = arac.gecis_bfs()
adim                       # en az kaç geçiş?
yol_sayisi                 # bu kadar kısa kaç plan var?
guvenli_durum              # güvenli durum sayısı
plan
""")
    plan = ns["plan"]

    def ciz(fig):
        ax = eksen(fig, 0.03, 0.06, 0.94, 0.78); ax.axis("off"); ax.set_xlim(0, 8); ax.set_ylim(0, 4)
        mutfak, bahce, r = set(A.ESYA), set(), 0
        renk = {"kedi": TURUNCU, "fare": GRI, "peynir": "#ca8a04"}
        for i in range(len(plan) + 1):
            x = 0.15 + i
            ax.text(x + 0.35, 3.75, "başta" if i == 0 else f"{i}. geçiş", ha="center", fontsize=19, weight="bold")
            ax.add_patch(Rectangle((x, 2.05), 0.7, 1.45, fc="#fef3c7", ec="none")); ax.add_patch(Rectangle((x, 0.35), 0.7, 1.45, fc="#dcfce7", ec="none"))
            for k, e in enumerate(sorted(mutfak)):
                ax.text(x + 0.35, 3.25 - k * 0.4, e, ha="center", fontsize=18, color=renk[e], weight="bold")
            for k, e in enumerate(sorted(bahce)):
                ax.text(x + 0.35, 1.55 - k * 0.4, e, ha="center", fontsize=18, color=renk[e], weight="bold")
            ax.text(x + 0.35, 2.2 if r == 0 else 0.5, "ROBOT", ha="center", fontsize=16, color=MAVI, weight="bold")
            if i < len(plan):
                e = plan[i]
                if e != "boş el":
                    (mutfak.remove(e), bahce.add(e)) if r == 0 else (bahce.remove(e), mutfak.add(e))
                r = 1 - r
                ax.text(x + 0.85, 1.92, "→" if r == 1 else "←", ha="center", fontsize=26, color=MAVI)
        ax.text(0.05, 2.75, "mutfak", rotation=90, fontsize=18, color=GRI, va="center")
        ax.text(0.05, 1.05, "bahçe", rotation=90, fontsize=18, color=GRI, va="center")
        fig.text(0.5, 0.03, "Taşınanlar: " + " → ".join(plan) + f" · {ns['adim']} geçiş", ha="center", fontsize=21, color=MAVI)
    grafik("1.4", "gecis-plani", "Kedi, fare ve peynir: robot en az kaç geçişte taşır?", ciz)
    olc(d1_4_adim=ns["adim"], d1_4_yol_sayisi=ns["yol_sayisi"], d1_4_guvenli_durum=ns["guvenli_durum"], d1_4_plan=plan,
        d1_4_bos_el=plan.count("boş el"), d1_4_fare_tasima=plan.count("fare"))


if __name__ == "__main__":
    ders_1_1(); ders_1_2(); ders_1_3(); ders_1_4()
    print("hafta 1 tamam")

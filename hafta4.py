"""Hafta 4 · Şekil ve Uzay — Ders 4.1–4.4.
  python hafta4.py   → ekran/4.x/*.txt + *.png, OLCUMLER.json (d4_*)"""
import numpy as np
from matplotlib.patches import Polygon, Rectangle
from ortak import kayit, olc, oturum, grafik, eksen, MAVI, TURUNCU, YESIL, MOR, GRI
import arac as A

RENK12 = ["#2563eb", "#ea580c", "#16a34a", "#7c3aed", "#db2777", "#ca8a04", "#0891b2", "#65a30d", "#9333ea", "#dc2626", "#0d9488", "#475569"]


# ---------- 4.1 Tangram (OOEZO.1.1.2–1.1.3 tangram · M.4.3.3.1 alan · M.4.2.1.1 üçgen, kare) ----------
TANGRAM = {   # kenarı 4 birim olan kare; köşe koordinatları
    "büyük üçgen 1": [(0, 0), (4, 0), (2, 2)],
    "büyük üçgen 2": [(0, 0), (2, 2), (0, 4)],
    "orta üçgen": [(2, 4), (4, 4), (4, 2)],
    "küçük üçgen 1": [(4, 0), (4, 2), (3, 1)],
    "küçük üçgen 2": [(2, 2), (3, 3), (1, 3)],
    "kare": [(2, 2), (3, 1), (4, 2), (3, 3)],
    "paralelkenar": [(0, 4), (1, 3), (3, 3), (2, 4)],
}


def ders_4_1():
    ns = oturum("4.1", "tangram-alan", """
from hafta4 import TANGRAM
def alan(k):                    # köşelerden alan
    return abs(sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(k, k[1:] + k[:1]))) / 2
list(TANGRAM)
[alan(k) for k in TANGRAM.values()]
sum(alan(k) for k in TANGRAM.values())    # bütün parçalar
4 * 4                                       # kenarı 4 birim olan kare
sum(len(k) == 3 for k in TANGRAM.values())  # kaç üçgen?
""")
    al = {ad: ns["alan"](k) for ad, k in TANGRAM.items()}
    # üst üste binme yok mu? kareyi ince ızgarayla tarayıp her noktanın tek parçaya düştüğünü say
    from matplotlib.path import Path
    xs = (np.arange(400) + 0.37) / 100; ys = (np.arange(400) + 0.61) / 100   # kenar çizgilerine denk gelmesin
    X, Y = np.meshgrid(xs, ys); P = np.column_stack([X.ravel(), Y.ravel()])
    kat = sum(Path(k).contains_points(P).astype(int) for k in TANGRAM.values())
    tek = float((kat == 1).mean())

    def ciz(fig):
        ax = fig.add_axes([0.04, 0.08, 0.42, 0.76])
        for i, (ad, k) in enumerate(TANGRAM.items()):
            ax.add_patch(Polygon(k, fc=RENK12[i], ec="white", lw=4))
            cx = sum(x for x, y in k) / len(k); cy = sum(y for x, y in k) / len(k)
            ax.text(cx, cy, f"{al[ad]:g}", ha="center", va="center", color="white", fontsize=30, weight="bold")
        ax.set_xlim(-0.1, 4.1); ax.set_ylim(-0.1, 4.1); ax.set_aspect("equal"); ax.axis("off")
        a2 = fig.add_axes([0.52, 0.08, 0.46, 0.76]); a2.axis("off"); a2.set_xlim(0, 10); a2.set_ylim(0, 10)
        y = 9.4
        for i, (ad, k) in enumerate(TANGRAM.items()):
            a2.add_patch(Rectangle((0, y - 0.35), 0.6, 0.6, fc=RENK12[i]))
            a2.text(0.9, y, f"{ad}: {al[ad]:g} birim kare", va="center", fontsize=22)
            y -= 0.95
        a2.text(0, y - 0.3, f"Toplam {sum(al.values()):g} = 4 × 4 · beş üçgen, bir kare, bir paralelkenar", fontsize=21, weight="bold")
        a2.text(0, y - 1.2, "Tepsi kenarı 40 cm olsaydı (ÖRNEK): bir birim kare 100 cm²", fontsize=19, color=GRI)
    grafik("4.1", "tangram", "Tangram: yedi parça, bir kare tepsi", ciz)
    olc(d4_1_alan={k: int(v) for k, v in al.items()}, d4_1_toplam=int(sum(al.values())), d4_1_parca=7, d4_1_ucgen=5,
        d4_1_tek_kat=round(tek, 4), d4_1_buyuk_kat=int(al["büyük üçgen 1"] / al["küçük üçgen 1"]),
        d4_1_tepsi_cm=40, d4_1_birim_cm2=100, d4_1_buyuk_cm2=int(al["büyük üçgen 1"] * 100))


# ---------- 4.2 Pentomino (OOEZO.1.1.3 pentomino · M.4.3.3.2 alan ve çarpma) ----------
def ders_4_2():
    ns = oturum("4.2", "pentomino-oturum", """
import arac
parca = arac.polyomino(5)                    # beş kareli bütün parçalar (döndürme ve ayna aynı)
len(parca)
len(arac.polyomino(5, serbest=False))        # döndürme ve ayna ayrı sayılırsa
len(parca) * 5                               # toplam kare
[(en, boy) for en in range(3, 21) for boy in range(3, en + 1) if en * boy == 60]
sayi, ilk = arac.doseme_say(20, 3, parca)    # 3 × 20 tepsi
sayi                                         # döndürülmüş ve aynada çevrilmiş halleri dahil
sayi // 4                                    # birbirinden gerçekten farklı
import itertools
gruplar = list(itertools.combinations(range(12), 5))
len(gruplar)                                 # on ikiden seçilen beşli gruplar
sum(arac.doseme_say(5, 5, [parca[i] for i in g], limit=1)[0] > 0 for g in gruplar)   # 5 × 5 kareyi dolduranlar
""")
    parca = ns["parca"]; ilk = ns["ilk"]

    def ciz(fig):
        ax = fig.add_axes([0.03, 0.47, 0.94, 0.36]); ax.axis("off"); ax.set_xlim(-0.5, 47); ax.set_ylim(-0.5, 6.2); ax.set_aspect("equal")
        x0 = 0
        for i, p in enumerate(parca):
            for (x, y) in p:
                ax.add_patch(Rectangle((x0 + x, y), 1, 1, fc=RENK12[i], ec="white", lw=2))
            x0 += max(x for x, y in p) + 2
        ax.text(0, 5.5, f"{len(parca)} pentomino · her biri 5 birim kare · toplam {len(parca) * 5}", fontsize=22)
        a2 = fig.add_axes([0.08, 0.08, 0.84, 0.3]); a2.axis("off"); a2.set_xlim(-0.2, 20.2); a2.set_ylim(-0.2, 3.6); a2.set_aspect("equal")
        for (x, y), i in ilk.items():
            a2.add_patch(Rectangle((x, y), 1, 1, fc=RENK12[i], ec="white", lw=2))
        a2.add_patch(Rectangle((0, 0), 20, 3, fill=False, ec="#111", lw=4))
        a2.text(0, 3.25, f"3 × 20 tepsiyi doldurmanın {ns['sayi']} yolu var, döndürme ve ayna sayılmazsa {ns['sayi'] // 4} — robotun bulduğu ilki:", fontsize=20)
    grafik("4.2", "pentomino", "On iki pentomino ile tepsiyi boşluksuz doldurmak", ciz)
    olc(d4_2_serbest=len(parca), d4_2_sabit=len(A.polyomino(5, False)), d4_2_kare=len(parca) * 5,
        d4_2_dikdortgen=[[en, boy] for en in range(3, 21) for boy in range(3, en + 1) if en * boy == 60],
        d4_2_doseme=ns["sayi"], d4_2_farkli=ns["sayi"] // 4, d4_2_besli_grup=len(ns["gruplar"]),
        d4_2_kare5_grup=sum(A.doseme_say(5, 5, [parca[i] for i in g], limit=1)[0] > 0 for g in ns["gruplar"]))


# ---------- 4.3 Küp Açınımı (M.4.2.1.4 açınımı verilen küp · OOEZO.1.1.4 üç boyutlu cisimler) ----------
def ders_4_3():
    ns = oturum("4.3", "kup-acinimi", """
import arac
alti = arac.polyomino(6)                     # altı kareli bütün parçalar
len(alti)
acinim = [p for p in alti if arac.kup_acinimi_mi(p)]
len(acinim)                                  # katlanınca küp olanlar
len(alti) - len(acinim)                      # olmayanlar
arac.kup_acinimi_mi([(0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (1, 2)])   # artı biçimli haç
arac.kup_acinimi_mi([(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)])   # altı kare yan yana
""")
    alti, acinim = ns["alti"], ns["acinim"]
    olmayan = [p for p in alti if p not in acinim]

    def ciz(fig):
        ax = fig.add_axes([0.02, 0.04, 0.96, 0.82]); ax.axis("off"); ax.set_aspect("equal")
        x0, y0 = 0, 0
        for i, p in enumerate(acinim):
            w = max(x for x, y in p) + 1
            if x0 + w > 44:
                x0 = 0; y0 -= 6.0
            for (x, y) in p:
                ax.add_patch(Rectangle((x0 + x, y0 + y), 1, 1, fc=YESIL, ec="white", lw=2))
            ax.text(x0, y0 - 0.9, f"{i + 1}", fontsize=16, color=GRI)
            x0 += w + 1.6
        ax.text(0, 6.0, f"Altı kareli {len(alti)} parçanın yalnız {len(acinim)} tanesi küp kutu olur (yeşil)", fontsize=22, weight="bold")
        x0 = 30
        ax.text(x0, y0 + 4.6, f"Küp olmayanlardan ikisi (toplam {len(olmayan)}):", fontsize=18, color=TURUNCU)
        for p in [olmayan[0], olmayan[2]]:
            pp = [(y, x) for x, y in p] if max(y for x, y in p) > 3 else p      # uzun parçayı yatır
            for (x, y) in pp:
                ax.add_patch(Rectangle((x0 + x, y0 + 2 + y), 1, 1, fc=TURUNCU, ec="white", lw=2, alpha=0.85))
            x0 += max(x for x, y in pp) + 2.5
        ax.set_xlim(-0.5, 46); ax.set_ylim(y0 - 1.8, 7.0)
    grafik("4.3", "kup-acinimlari", "Bardak kutusu: hangi açınımlar küp olur?", ciz)
    olc(d4_3_alti=len(alti), d4_3_acinim=len(acinim), d4_3_olmayan=len(olmayan), d4_3_hac=True, d4_3_sira=False, d4_3_yuz=6)


# ---------- 4.4 Ayna Simetrisi (M.4.2.2.1–M.4.2.2.2 · OOEZO.1.1.5) ----------
def ders_4_4():
    ns = oturum("4.4", "simetri", """
import arac
from ortak import kayit
parca = arac.polyomino(5)
dogru = [arac.ayna_dogrusu(p) for p in parca]
dogru                                        # her pentominonun ayna doğrusu sayısı
sum(d > 0 for d in dogru)                    # en az bir ayna doğrusu olan
k = kayit()
x = k["bardak_x_m"] - k["bardak_x_m"][0]
ayna_x = -x                                  # bardağın yolunu dikey doğruya göre yansıt
round(float(x[-1]), 2), round(float(ayna_x[-1]), 2)
iz = arac.kafe_izgarasi()
ayna = dict(iz, bas=(6, 0), son=(0, 4), masalar=[(6 - a, b) for a, b in iz["masalar"]])
arac.bfs(iz)[:2], arac.bfs(ayna)[:2]           # yansıyan kafede yol uzunluğu ve sayısı
""")
    parca, dogru = A.polyomino(5), ns["dogru"]
    k = kayit()
    x = k["bardak_x_m"] - k["bardak_x_m"][0]; y = k["bardak_y_m"] - k["bardak_y_m"][0]

    def ciz(fig):
        ax = fig.add_axes([0.05, 0.12, 0.42, 0.68])
        ax.plot(x, y, color=MAVI, lw=4, label="bardağın yolu (benzetim kaydı)")
        ax.plot(-x, y, color=TURUNCU, lw=4, ls="--", label="aynadaki görüntüsü")
        ax.axvline(0, color="#111", lw=3)
        ax.set_aspect("equal"); ax.set_xlabel("doğu–batı (m)"); ax.set_ylabel("kuzey (m)")
        fig.text(0.05, 0.06, "mavi: bardağın yolu (benzetim kaydı) · turuncu kesikli: aynadaki görüntüsü", fontsize=19, color=GRI)
        ax.set_title("Siyah çizgi: simetri doğrusu", fontsize=22)
        a2 = fig.add_axes([0.52, 0.12, 0.46, 0.68]); a2.axis("off"); a2.set_aspect("equal"); a2.set_xlim(-0.5, 24); a2.set_ylim(-1.5, 15)
        x0, y0 = 0, 8
        for i, p in enumerate(parca):
            if i == 6:
                x0, y0 = 0, 1.5
            for (px, py) in p:
                a2.add_patch(Rectangle((x0 + px, y0 + py), 1, 1, fc=YESIL if dogru[i] else "#cbd5e1", ec="white", lw=2))
            a2.text(x0, y0 - 1.0, f"{dogru[i]}", fontsize=20, weight="bold", color=YESIL if dogru[i] else GRI)
            x0 += max(px for px, py in p) + 2.2
        a2.text(0, 14.2, f"Pentominolar: {sum(d > 0 for d in dogru)} tanesinde ayna doğrusu var (yeşil)", fontsize=20)
        a2.text(0, -1.3, "alttaki sayı: kaç ayna doğrusu", fontsize=17, color=GRI)
    grafik("4.4", "ayna", "Ayna simetrisi: bardağın yolu ve pentominolar", ciz)
    olc(d4_4_dogru=dogru, d4_4_simetrik=sum(d > 0 for d in dogru), d4_4_simetrisiz=sum(d == 0 for d in dogru), d4_4_en_cok=max(dogru),
        d4_4_x_son=round(float(x[-1]), 2), d4_4_ayna_x_son=round(float(-x[-1]), 2),
        d4_4_kafe=list(ns["arac"].bfs(ns["iz"])[:2]), d4_4_ayna_kafe=list(ns["arac"].bfs(ns["ayna"])[:2]))


if __name__ == "__main__":
    ders_4_1(); ders_4_2(); ders_4_3(); ders_4_4()
    print("hafta 4 tamam")

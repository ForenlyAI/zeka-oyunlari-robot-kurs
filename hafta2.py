"""Hafta 2 · Örüntü, Şifre ve Hafıza — Ders 2.1–2.4.
  python hafta2.py   → ekran/2.x/*.txt + *.png, OLCUMLER.json (d2_*)"""
import math, random
import numpy as np
from matplotlib.patches import Rectangle, Circle, RegularPolygon
from ortak import kayit, olc, oturum, grafik, eksen, MAVI, TURUNCU, YESIL, MOR, GRI
import arac as A


# ---------- 2.1 Sayı Örüntüleri (M.4.1.1.6 · OOEZO.1.3.2) ----------
def ders_2_1():
    ns = oturum("2.1", "olcum-oruntusu", """
from ortak import kayit
k = kayit()
t = k["zaman_s"]
[int((t < s).sum()) for s in range(1, 6)]     # ilk 1, 2, 3, 4, 5 saniyedeki ölçüm sayısı
fark = int((t < 2).sum() - (t < 1).sum())
fark                                          # örüntünün kuralı: her adımda kaç artıyor?
10 * fark                                     # onuncu adım
len(t)                                        # kaydın bütün ölçümleri
[len(t) - fark * s for s in range(0, 5)]     # azalan örüntü: kalan ölçüm
""")
    t = kayit()["zaman_s"]
    dizi = [int((t < s).sum()) for s in range(1, 6)]
    fark = ns["fark"]

    def ciz(fig):
        ax = eksen(fig, 0.08, 0.14, 0.86, 0.66)
        s = np.arange(1, 11)
        ax.bar(s, fark * s, color=[MAVI] * 5 + ["#cbd5e1"] * 5, width=0.6)
        for i in s:
            ax.text(i, fark * i + 8, str(fark * i), ha="center", fontsize=22, weight="bold", color=MAVI if i <= 5 else GRI)
        for i in range(1, 10):
            ax.annotate("", xy=(i + 0.72, fark * (i + 1) + 25), xytext=(i + 0.28, fark * i + 25),
                        arrowprops=dict(arrowstyle="->", color=TURUNCU, lw=2))
            ax.text(i + 0.5, fark * (i + 0.5) + 35, f"+{fark}", ha="center", fontsize=17, color=TURUNCU, weight="bold")
        ax.set_xticks(s); ax.set_xlabel("saniye"); ax.set_ylabel("ölçüm sayısı"); ax.set_ylim(0, fark * 11)
        fig.text(0.5, 0.03, "Mavi sütunlar benzetim kaydından sayıldı · gri sütunlar örüntünün kuralıyla tahmin edildi",
                 ha="center", fontsize=21, color=GRI)
    grafik("2.1", "artan-oruntu", f"Her saniye {fark} ölçüm: artan sayı örüntüsü", ciz)
    olc(d2_1_dizi=dizi, d2_1_fark=fark, d2_1_onuncu=10 * fark, d2_1_toplam=len(t), d2_1_azalan=[len(t) - fark * s for s in range(0, 5)], d2_1_sure_s=round(float(t[-1]), 1))


# ---------- 2.2 Şekil Örüntüleri (OOEZO.1.1.4 örüntü · M.4.1.1.6) ----------
SIRA = ["çay", "çay", "su"]          # ÖRNEK tepsi sırası


def ders_2_2():
    ns = oturum("2.2", "kol-simgeleri", """
import numpy as np
from ortak import kayit
k = kayit()
aci = np.degrees(k["dirsek_rad"])[::50]       # her saniyenin ilk ölçümü
fark = np.diff(aci)
simge = "".join("▲" if d > 3 else "▼" if d < -3 else "●" for d in fark)
len(simge)
simge[:40]
{s: simge.count(s) for s in "▲▼●"}
""")
    ns2 = oturum("2.2", "tepsi-oruntusu", """
birim = ["çay", "çay", "su"]       # ÖRNEK tepsi sırası, tekrar eden birim
len(birim)
[birim[(n - 1) % 3] for n in range(1, 10)]
birim[(20 - 1) % 3]                # yirminci bardak
sum(birim[(n - 1) % 3] == "çay" for n in range(1, 31))   # otuz bardakta kaç çay?
""")
    simge = ns["simge"]
    say = {s: simge.count(s) for s in "▲▼●"}
    # en uzun bekleme (art arda ●)
    en_uzun = max(len(g) for g in simge.split("▲") for g in g.split("▼"))

    def ciz(fig):
        ax = fig.add_axes([0.03, 0.47, 0.94, 0.36]); ax.axis("off"); ax.set_xlim(0, 40); ax.set_ylim(-1.2, 1.4)
        renk = {"▲": YESIL, "▼": TURUNCU, "●": GRI}
        for i, s in enumerate(simge[:40]):
            ax.text(i + 0.5, 0.3, s, ha="center", va="center", fontsize=30, color=renk[s])
        ax.text(0, 1.2, "Robotun dirseği, ilk kırk saniye (benzetim kaydı): ▲ kalkıyor · ▼ iniyor · ● duruyor", fontsize=22)
        ax.text(0, -0.9, f"Bütün kayıt: ▲ {say['▲']} · ▼ {say['▼']} · ● {say['●']} — düzenli bir tekrar yok", fontsize=22, color=GRI)
        ax2 = fig.add_axes([0.03, 0.06, 0.94, 0.34]); ax2.axis("off"); ax2.set_xlim(0, 21); ax2.set_ylim(-1, 2)
        for n in range(1, 21):
            ic = SIRA[(n - 1) % 3]
            r = TURUNCU if ic == "çay" else MAVI
            ax2.add_patch(Rectangle((n - 0.4, 0), 0.8, 1.1, fc=r if n < 20 else "white", ec=r, lw=3, alpha=0.9))
            ax2.text(n, -0.4, str(n), ha="center", fontsize=16, color=GRI)
        ax2.text(20, 0.55, "?", ha="center", va="center", fontsize=32, weight="bold", color=TURUNCU)
        ax2.text(0.6, 1.5, "ÖRNEK tepsi örüntüsü: çay (turuncu), çay, su (mavi) — tekrar eden birim üç bardak · yirminci bardak: "
                 + ns2["birim"][(20 - 1) % 3], fontsize=21)
    grafik("2.2", "iki-oruntu", "Tekrar eden ve tekrar etmeyen dizi", ciz)
    olc(d2_2_saniye=len(simge), d2_2_simge=say, d2_2_en_uzun_bekleme=en_uzun, d2_2_birim=len(SIRA),
        d2_2_yirminci=SIRA[19 % 3], d2_2_otuzda_cay=sum(SIRA[(n - 1) % 3] == "çay" for n in range(1, 31)))


# ---------- 2.3 Şifre ve Kelime Oyunları (OOEZO.1.2.3 anagram, şifre oyunları) ----------
ALFABE = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"


def ders_2_3():
    ns = oturum("2.3", "anagram", """
from itertools import permutations
from ortak import parametre
[p for p in parametre()]                       # robotun sağ kol eklemleri (benzetim dosyası)
def anagram(kelime):
    return len(set(permutations(kelime)))
anagram("KOL"), anagram("OMUZ"), anagram("BİLEK"), anagram("DİRSEK")
sorted("".join(p) for p in set(permutations("KOL")))
anagram("BARDAK")                               # iki A var
""")
    ns2 = oturum("2.3", "sifre", """
alfabe = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
len(alfabe)
def sifrele(metin, kaydir):
    return "".join(alfabe[(alfabe.index(h) + kaydir) % 29] if h in alfabe else h for h in metin)
sifrele("ÇAY HAZIR", 1)
sifrele(sifrele("ÇAY HAZIR", 1), -1)
sifrele("ÇAY HAZIR", 3)
""")
    an = {w: len(set(__import__("itertools").permutations(w))) for w in ["KOL", "OMUZ", "BİLEK", "DİRSEK", "BARDAK"]}
    sf = ns2["sifrele"]

    def ciz(fig):
        ax = fig.add_axes([0.12, 0.14, 0.34, 0.68]); ax.axis("off")
        kel = ["KOL", "OMUZ", "BİLEK", "DİRSEK"]
        ax.barh(kel, [an[k] for k in kel], color=[MAVI, YESIL, MOR, TURUNCU])
        ax.set_xscale("log"); ax.axis("on"); ax.set_xlabel("farklı diziliş (anagram) · eksen 10 kat adımlı")
        for i, k in enumerate(kel):
            ax.text(an[k] * 1.15, i, f"{an[k]}", va="center", fontsize=26, weight="bold")
        ax.set_xlim(1, 5000); ax.invert_yaxis(); ax.set_title("Robot kolunun parça adları", fontsize=26)
        ax2 = fig.add_axes([0.52, 0.12, 0.45, 0.7]); ax2.axis("off"); ax2.set_xlim(0, 10); ax2.set_ylim(0, 10)
        ax2.text(0, 9.2, "Robotun mesajı, bir harf kaydırma:", fontsize=24)
        for j, (a, b) in enumerate(zip("ÇAY HAZIR", sf("ÇAY HAZIR", 1))):
            if a == " ":
                continue
            ax2.text(0.5 + j * 1.05, 7.4, a, ha="center", fontsize=34, weight="bold", color=MAVI)
            ax2.text(0.5 + j * 1.05, 6.4, "↓", ha="center", fontsize=24, color=GRI)
            ax2.text(0.5 + j * 1.05, 5.3, b, ha="center", fontsize=34, weight="bold", color=TURUNCU)
        ax2.text(0, 3.4, f"Türk alfabesi {len(ALFABE)} harf: Z'den sonra yine A gelir", fontsize=22, color=GRI)
        ax2.text(0, 2.4, f"Üç kaydırma: {sf('ÇAY HAZIR', 3)}", fontsize=22, color=GRI)
        ax2.text(0, 1.4, "Çözmek için aynı sayıda geri kaydırılır", fontsize=22, color=GRI)
    grafik("2.3", "anagram-sifre", "Harflerle oyun: anagram ve kaydırma şifresi", ciz)
    olc(d2_3_anagram=an, d2_3_kol=sorted("".join(p) for p in set(__import__("itertools").permutations("KOL"))),
        d2_3_alfabe=len(ALFABE), d2_3_sifre_1=sf("ÇAY HAZIR", 1), d2_3_sifre_3=sf("ÇAY HAZIR", 3), d2_3_eklem=len(ns["parametre"]()))


# ---------- 2.4 Hafıza Oyunu (OOEZO.1.5.2–1.5.3 resim eşleme) ----------
def ders_2_4():
    ns = oturum("2.4", "hafiza", """
import random, statistics
import arac
rng = random.Random(2026)          # aynı sonuç için sabit tohum
CIFT, OYUN = 8, 1000               # sekiz çift kart, bin oyun
robot = [arac.hafiza_oyunu(CIFT, rng, bellek=True) for _ in range(OYUN)]
unutkan = [arac.hafiza_oyunu(CIFT, rng, bellek=False) for _ in range(OYUN)]
round(statistics.mean(robot), 1), min(robot), max(robot)
round(statistics.mean(unutkan), 1), min(unutkan), max(unutkan)
CIFT                               # en şanslı oyun: her hamlede bir çift
""")
    r, u = ns["robot"], ns["unutkan"]
    import statistics as st

    def ciz(fig):
        ax = eksen(fig, 0.08, 0.14, 0.86, 0.66)
        b = np.arange(0, 141, 4)
        ax.hist(r, bins=np.arange(6, 30, 1), color=YESIL, alpha=0.85, label=f"hatırlayan robot · ortalama {st.mean(r):.1f}".replace(".", ","))
        ax.hist(u, bins=b, color=TURUNCU, alpha=0.6, label=f"hiç hatırlamayan oyuncu · ortalama {st.mean(u):.1f}".replace(".", ","))
        ax.set_xlabel("oyunu bitirmek için hamle (her hamlede iki kart)"); ax.set_ylabel("oyun sayısı (1000 oyundan)")
        ax.axvline(8, color=MAVI, lw=3, ls="--"); ax.text(7, ax.get_ylim()[1] * 0.6, "en az 8 hamle", color=MAVI, fontsize=22, ha="right")
        ax.legend(fontsize=22, loc="upper right")
        fig.text(0.5, 0.03, "16 kart, 8 çift · kartların yeri her oyunda rastgele (sabit tohum 2026)", ha="center", fontsize=20, color=GRI)
    grafik("2.4", "hafiza-farki", "Hafıza oyunu: hatırlamak kaç hamle kazandırır?", ciz)
    olc(d2_4_cift=8, d2_4_kart=16, d2_4_oyun=1000, d2_4_robot_ort=round(st.mean(r), 1), d2_4_robot_min=min(r), d2_4_robot_max=max(r),
        d2_4_unutkan_ort=round(st.mean(u), 1), d2_4_unutkan_min=min(u), d2_4_unutkan_max=max(u),
        d2_4_kat=round(st.mean(u) / st.mean(r), 1))


if __name__ == "__main__":
    ders_2_1(); ders_2_2(); ders_2_3(); ders_2_4()
    print("hafta 2 tamam")

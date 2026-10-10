"""Hafta 3 · Strateji Oyunları — Ders 3.1–3.4.
  python hafta3.py   → ekran/3.x/*.txt + *.png, OLCUMLER.json (d3_*)"""
import random
import numpy as np
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Ellipse
from ortak import olc, oturum, grafik, eksen, MAVI, TURUNCU, YESIL, MOR, GRI
import arac as A


def tahta_ciz(ax, t, x0, y0, boy=1.0, vurgu=None):
    for i in range(9):
        r, c = divmod(i, 3)
        x, y = x0 + c * boy, y0 + (2 - r) * boy
        ax.add_patch(Rectangle((x, y), boy, boy, fc="#fef9c3" if vurgu and i in vurgu else "white", ec="#334155", lw=2))
        if t[i] != ".":
            ax.text(x + boy / 2, y + boy / 2, t[i], ha="center", va="center", fontsize=int(30 * boy),
                    color=MAVI if t[i] == "X" else TURUNCU, weight="bold")


# ---------- 3.1 XOX Oyun Ağacı (OOEZO.1.4.1–1.4.2 Tic-Tac-Toe) ----------
def ders_3_1():
    ns = oturum("3.1", "oyun-agaci", """
import arac
derinlik, sonuc, tahta = arac.xox_agac()
derinlik[:4]              # 0, 1, 2, 3 hamle sonra kaç farklı oyun yolu
sum(sonuc.values())       # bitebilecek bütün oyunlar
sonuc
tahta                     # birbirinden farklı tahta sayısı
""")
    d, s = ns["derinlik"], ns["sonuc"]

    def ciz(fig):
        ax = eksen(fig, 0.08, 0.14, 0.5, 0.66)
        ax.bar(range(10), d, color=[MAVI] * 4 + ["#93c5fd"] * 6)
        ax.set_yscale("log"); ax.set_xticks(range(10)); ax.set_xlabel("kaçıncı hamle"); ax.set_ylabel("oyun yolu · eksen 10 kat adımlı")
        for i in range(4):
            ax.text(i, d[i] * 1.4, str(d[i]), ha="center", fontsize=22, weight="bold")
        ax.set_ylim(0.5, 2e6)
        a2 = fig.add_axes([0.62, 0.1, 0.36, 0.76]); a2.axis("off"); a2.set_xlim(0, 6.6); a2.set_ylim(0, 7.2); a2.set_aspect("equal")
        tahta_ciz(a2, "X........", 0.1, 3.6, 0.9); tahta_ciz(a2, "X...O....", 3.5, 3.6, 0.9)
        a2.text(0.1, 6.6, "ilk hamle: 9 seçenek → ikinci: 8", fontsize=20)
        a2.text(0, 2.6, f"Bütün oyunlar: {sum(s.values())}", fontsize=26, weight="bold")
        a2.text(0, 1.9, f"X kazanır {s['X']} · O kazanır {s['O']}", fontsize=21)
        a2.text(0, 1.3, f"berabere {s['berabere']} · farklı tahta {ns['tahta']}", fontsize=21)
    grafik("3.1", "agac-buyuklugu", "XOX: her hamlede oyun ağacı dallanır", ciz)
    def en_kisa(t="." * 9, s="X", n=0):        # bir oyunun bitebileceği en az hamle
        if A.kazanan(t):
            return n
        return min((en_kisa(t[:i] + s + t[i + 1:], "O" if s == "X" else "X", n + 1) for i in range(9) if t[i] == "."), default=99)
    olc(d3_1_en_kisa=en_kisa(), d3_1_derinlik=d, d3_1_oyun=sum(s.values()), d3_1_x=s["X"], d3_1_o=s["O"], d3_1_berabere=s["berabere"], d3_1_tahta=ns["tahta"],
        d3_1_ilk=9, d3_1_iki_hamle=d[2], d3_1_uc_hamle=d[3])


# ---------- 3.2 XOX'ta Kaybetmeyen Robot (OOEZO.1.4.3–1.4.4 taktik ve strateji) ----------
def ders_3_2():
    ns = oturum("3.2", "minimaks", """
import random
import arac
arac.xox_deger("." * 9, "X")        # iki taraf da en iyi oynarsa: 1 X, 0 berabere, -1 O
t = "XX.OO...."                    # sıra X'te: kazanan hamle var mı?
arac.xox_robot(t, "X")             # robotun seçtiği kare (0'dan sayılır)
t = "XX..O...."                    # sıra O'da: engellemesi gerek
arac.xox_robot(t, "O")
rng = random.Random(2026)
sonuc = [arac.xox_mac("X", rng) for _ in range(1000)]
{s: sonuc.count(s) for s in ("X", "berabere", "O")}     # robot X, rakip rastgele
sonuc = [arac.xox_mac("O", rng) for _ in range(1000)]
{s: sonuc.count(s) for s in ("O", "berabere", "X")}     # robot O, rakip rastgele
""")
    rng = random.Random(2026)
    sx = [A.xox_mac("X", rng) for _ in range(1000)]
    so = [A.xox_mac("O", rng) for _ in range(1000)]
    rx = {s: sx.count(s) for s in ("X", "berabere", "O")}
    ro = {s: so.count(s) for s in ("O", "berabere", "X")}
    kazan = A.xox_robot("XX.OO....", "X"); engel = A.xox_robot("XX..O....", "O")

    def ciz(fig):
        a1 = fig.add_axes([0.02, 0.1, 0.46, 0.74]); a1.axis("off"); a1.set_xlim(0, 8); a1.set_ylim(0, 5.6); a1.set_aspect("equal")
        tahta_ciz(a1, "XX.OO....", 0.3, 1.2, 1.1, vurgu={kazan}); tahta_ciz(a1, "XX..O....", 4.3, 1.2, 1.1, vurgu={engel})
        a1.text(1.95, 4.9, "1. kural:\nkazanabiliyorsan kazan", ha="center", fontsize=18, weight="bold")
        a1.text(5.95, 4.9, "2. kural:\nrakibin kazancını kapat", ha="center", fontsize=18, weight="bold")
        a1.text(1.95, 0.5, f"robot X: sarı kare", ha="center", fontsize=18, color=MAVI)
        a1.text(5.95, 0.5, f"robot O: sarı kare", ha="center", fontsize=18, color=TURUNCU)
        a2 = fig.add_axes([0.63, 0.16, 0.35, 0.58])
        ad = ["robot X", "robot O"]
        k = [rx["X"], ro["O"]]; b = [rx["berabere"], ro["berabere"]]; y = [rx["O"], ro["X"]]
        a2.barh(ad, k, color=YESIL, label="robot kazandı")
        a2.barh(ad, b, left=k, color=GRI, label="berabere")
        a2.barh(ad, y, left=[i + j for i, j in zip(k, b)], color=TURUNCU, label="robot kaybetti")
        for i in range(2):
            a2.text(k[i] / 2, i, str(k[i]), ha="center", va="center", color="white", fontsize=24, weight="bold")
            if b[i] > 60:
                a2.text(k[i] + b[i] / 2, i, str(b[i]), ha="center", va="center", color="white", fontsize=22, weight="bold")
            else:
                a2.text(990, i - 0.48, f"berabere {b[i]}", ha="right", va="center", color=GRI, fontsize=18)
        a2.set_xlim(0, 1000); a2.set_xlabel("1000 oyunda (rakip rastgele oynuyor)"); fig.text(0.63, 0.83, "yeşil: robot kazandı", fontsize=20, color=YESIL, weight="bold")
        fig.text(0.80, 0.83, "gri: berabere", fontsize=20, color=GRI, weight="bold")
        fig.text(0.63, 0.79, f"robot kaybetti: {y[0] + y[1]} oyun", fontsize=22, color=TURUNCU, weight="bold")
    grafik("3.2", "robot-mac", "Her hamleyi sonuna kadar düşünen robot hiç kaybetmez", ciz)
    olc(d3_2_deger=A.xox_deger("." * 9, "X"), d3_2_kazan_kare=kazan, d3_2_engel_kare=engel, d3_2_robot_x=rx, d3_2_robot_o=ro,
        d3_2_kayip=rx["O"] + ro["X"], d3_2_mac=1000)


# ---------- 3.3 Alma Oyunu (Nim) (OOEZO.1.4.3 · M.4.1.5 bölme, kalan) ----------
def ders_3_3():
    ns = oturum("3.3", "nim", """
import random
import arac
kazanir = arac.nim_tablo(20, en_cok=3)          # her sırada 1, 2 ya da 3 şeker küpü, sonuncuyu alan kazanır
[k for k in range(1, 21) if not kazanir[k]]       # sırası gelenin kaybettiği sayılar
15 % 4                                           # robot başta kaç alır?
arac.nim_robot(15)
rng = random.Random(2026)
sonuc = [arac.nim_mac(15, rng) for _ in range(1000)]
sonuc.count("robot"), sonuc.count("rakip")
""")
    kaz = A.nim_tablo(20)
    kaybet = [k for k in range(1, 21) if not kaz[k]]
    rng = random.Random(2026)
    sonuc = [A.nim_mac(15, rng) for _ in range(1000)]

    def ciz(fig):
        ax = fig.add_axes([0.03, 0.42, 0.94, 0.38]); ax.axis("off"); ax.set_xlim(0, 21); ax.set_ylim(-1.2, 1.6)
        for k in range(1, 21):
            r = TURUNCU if not kaz[k] else YESIL
            ax.add_patch(Rectangle((k - 0.42, 0), 0.84, 0.84, fc=r, ec="none"))
            ax.text(k, 0.42, str(k), ha="center", va="center", color="white", fontsize=22, weight="bold")
        ax.text(0.6, 1.25, "Masada kaç küp kaldı? Yeşil: sırası gelen kazanır · turuncu: sırası gelen kaybeder", fontsize=21)
        ax.text(0.6, -0.8, "Turuncular dördün katları: 4, 8, 12, 16, 20 — rakibe hep dördün katını bırak", fontsize=21, color=TURUNCU)
        a2 = fig.add_axes([0.03, 0.06, 0.94, 0.3]); a2.axis("off"); a2.set_xlim(0, 21); a2.set_ylim(0, 3)
        k, sira, y = 15, "robot", 2.2
        r2 = random.Random(7)
        x = 0.6
        while k:
            a = A.nim_robot(k) if sira == "robot" else r2.randint(1, min(3, k))
            a2.text(x, y, f"{k}", fontsize=24, weight="bold")
            a2.text(x + 0.9, y, f"−{a}", fontsize=20, color=MAVI if sira == "robot" else GRI)
            k -= a; x += 2.1; sira = "rakip" if sira == "robot" else "robot"
        a2.text(x, y, "0", fontsize=24, weight="bold")
        a2.text(0.6, 0.9, f"15 küple robot başlar, mavi: robot alır, gri: rakip alır · 1000 oyunda robot {sonuc.count('robot')} kez kazandı",
                fontsize=20, color=GRI)
    grafik("3.3", "nim-tablosu", "Şeker küpü oyunu: kazanmanın sırrı dördün katları", ciz)
    olc(d3_3_kaybet=kaybet, d3_3_basla=15, d3_3_ilk_al=A.nim_robot(15), d3_3_kalan=15 - A.nim_robot(15),
        d3_3_robot=sonuc.count("robot"), d3_3_rakip=sonuc.count("rakip"), d3_3_en_cok=3, d3_3_kat=4)


# ---------- 3.4 Mangala (OOEZO.1.4.1–1.4.4 mangala · kaynaklar.py mangala_kural) ----------
def mangala_ciz(ax, t, x0, y0, vurgu=None, baslik=None):
    ax.add_patch(FancyBboxPatch((x0, y0), 8, 2.6, boxstyle="round,pad=0.05,rounding_size=0.4", fc="#d6b48a", ec="#7c5a33", lw=3))
    for i in range(6):
        for (idx, yy) in ((i, y0 + 0.75), (12 - i, y0 + 1.85)):
            ax.add_patch(Circle((x0 + 1.5 + i, yy), 0.42, fc="#fff7ed" if vurgu != idx else "#fde68a", ec="#7c5a33", lw=2))
            ax.text(x0 + 1.5 + i, yy, str(t[idx]), ha="center", va="center", fontsize=22, weight="bold")
    for idx, xx, ad in ((6, x0 + 7.5, "A"), (13, x0 + 0.5, "B")):
        ax.add_patch(Ellipse((xx, y0 + 1.3), 0.8, 2.1, fc="#fff7ed" if vurgu != idx else "#fde68a", ec="#7c5a33", lw=2))
        ax.text(xx, y0 + 1.3, str(t[idx]), ha="center", va="center", fontsize=24, weight="bold")
        ax.text(xx, y0 - 0.35, f"{ad} hazinesi", ha="center", fontsize=15, color=GRI)
    if baslik:
        ax.text(x0 + 4, y0 + 3.0, baslik, ha="center", fontsize=20, weight="bold")


def ders_3_4():
    ns = oturum("3.4", "mangala-acilis", """
import arac
tahta = arac.mangala_bas()          # 12 kuyu, her kuyuda 4 taş, iki hazine boş
sum(tahta)
for kuyu in range(6):               # A oyuncusunun 1–6. kuyusu
    yeni, son, tekrar, alinan = arac.mangala_hamle(tahta, 0, kuyu)
    print(f"{kuyu + 1}. kuyu → son taş {arac.mangala_yer(son)}", "· TEKRAR OYNAR" if tekrar else "")
arac.mangala_durum_say(4)           # ilk 1, 2, 3, 4 hamlede farklı tahta sayısı
""")
    t0 = A.mangala_bas()
    acilis = [A.mangala_hamle(t0, 0, k) for k in range(6)]
    tekrar_kuyu = [k + 1 for k in range(6) if acilis[k][2]]
    t1 = acilis[3][0]
    # tekrar oynama hakkıyla en iyi ikinci hamle: hazinede en çok taş
    ikinci = [(A.mangala_hamle(t1, 0, k)[0][6], k + 1) for k in range(6) if t1[k]]
    en_iyi = max(ikinci)
    t2 = A.mangala_hamle(t1, 0, en_iyi[1] - 1)[0]
    durum = A.mangala_durum_say(4)

    def ciz(fig):
        ax = fig.add_axes([0.02, 0.05, 0.96, 0.8]); ax.axis("off"); ax.set_xlim(0, 27); ax.set_ylim(0, 8.2)
        mangala_ciz(ax, t0, 0.3, 4.3, baslik="Başlangıç: her kuyuda 4 taş")
        mangala_ciz(ax, t1, 9.5, 4.3, vurgu=6, baslik="A 4. kuyudan oynar: son taş hazinede")
        mangala_ciz(ax, t2, 18.7, 4.3, vurgu=6, baslik=f"Tekrar oynar: {en_iyi[1]}. kuyu")
        ax.text(0.3, 2.6, "A'nın kuyuları altta, soldan sağa 1–6 · taşlar sağa doğru dağıtılır, ilk taş aldığın kuyuya", fontsize=19)
        ax.text(0.3, 1.8, f"Açılışta altı kuyudan yalnız {tekrar_kuyu[0]}. kuyu tekrar oynama hakkı verir", fontsize=21, color=MAVI, weight="bold")
        ax.text(0.3, 1.0, f"İlk dört hamlede farklı tahta: {durum[0]} → {durum[1]} → {durum[2]} → {durum[3]}", fontsize=21)
        ax.text(0.3, 0.2, "Kurallar: Mangala Turnuva Kuralları (Tüm Akıl ve Zekâ Oyunları Federasyonu), dört temel kural", fontsize=17, color=GRI)
    grafik("3.4", "mangala", "Mangala: hangi kuyudan oynarsam tekrar oynarım?", ciz)
    olc(d3_4_tas=sum(t0), d3_4_kuyu=12, d3_4_kuyu_tas=4, d3_4_son_yer=[A.mangala_yer(a[1]) for a in acilis], d3_4_tekrar_kuyu=tekrar_kuyu,
        d3_4_ikinci_kuyu=en_iyi[1], d3_4_ikinci_hazine=en_iyi[0], d3_4_hazine_1=t1[6], d3_4_durum=durum)


if __name__ == "__main__":
    ders_3_1(); ders_3_2(); ders_3_3(); ders_3_4()
    print("hafta 3 tamam")

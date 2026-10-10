"""Zekâ Oyunları ve Robot Bulmacaları — bulmaca çözücüler (derslerin ortak hesapları).
Her işlev bir bulmacayı GERÇEKTEN çözer ya da sayar; ders oturumları bunları çağırır, sonuçlar OLCUMLER.json'a gider.

  kafe_izgarasi()          : kafe ızgarası (0,5 m kareler) — başlangıç ve bitiş bardağın benzetim kaydındaki ilk ve son konumu
  bfs(izgara, bas, son)    : en kısa yol uzunluğu, en kısa yol sayısı, incelenen kare sayısı (genişlik öncelikli arama)
  en_kisa_yollar(...)      : bütün en kısa yollar (liste)
  kartlar(yol)             : yolu İLERİ / SAĞA DÖN / SOLA DÖN kartlarına çevirir (robot doğuya bakarak başlar)
  sudoku_coz / sudoku_say  : 4 × 4 mini sudoku (satır, sütun ve 2 × 2 kutuda her simge bir kez)
  gecis_bfs()              : kedi, fare ve peynir bulmacası (robot elinde bir şey taşır)
  xox_agac() / xox_deger() : XOX oyun ağacının tamamı ve en iyi hamle (minimaks)
  nim_tablo(n, en_cok)     : alma oyunu (sonuncuyu alan kazanır) — kazanan / kaybeden durumlar
  mangala_hamle(...)       : mangala dört temel kuralı (kaynaklar.py mangala_kural)
  polyomino(n)             : n kareli parçalar (pentomino n = 5, hekzomino n = 6), döndürme ve yansıma birleştirilir
  doseme_say(...)          : bir dikdörtgeni parçalarla döşeme sayısı (her parça bir kez)
  kup_acinimi_mi(parca)    : altı kare katlanınca küp oluyor mu (küp yuvarlama yöntemi)
Kayıtta olmayan değerler (masaların yeri, bulmaca ipuçları) her kullanıldığı yerde ÖRNEK diye işaretlenir."""
from collections import deque
import itertools, random

# ---------- yol bulma ----------
HUCRE_M = 0.5                                   # ÖRNEK ızgara adımı: yarım metre
MASALAR = [(2, 1), (2, 2), (4, 2), (4, 3), (1, 3), (5, 0)]   # ÖRNEK masa kareleri (kayıtta masa yeri yok)
YON = {(1, 0): "doğu", (0, 1): "kuzey", (-1, 0): "batı", (0, -1): "güney"}


def kafe_izgarasi(kayit=None):
    """Izgaranın boyu bardağın kayıttaki yer değiştirmesinden: doğuya ve kuzeye kaç yarım metre."""
    from ortak import kayit as _k
    k = kayit or _k()
    dx = round((k["bardak_x_m"][-1] - k["bardak_x_m"][0]) / HUCRE_M)
    dy = round((k["bardak_y_m"][-1] - k["bardak_y_m"][0]) / HUCRE_M)
    return dict(en=dx + 1, boy=dy + 1, bas=(0, 0), son=(dx, dy), masalar=list(MASALAR))


def komsular(iz, p, engel=True):
    for d in YON:
        q = (p[0] + d[0], p[1] + d[1])
        if 0 <= q[0] < iz["en"] and 0 <= q[1] < iz["boy"] and not (engel and q in iz["masalar"]):
            yield q


def bfs(iz, engel=True):
    """Genişlik öncelikli arama: her kareye en az kaç adımda varılır ve kaç farklı en kısa yoldan."""
    bas, son = iz["bas"], iz["son"]
    uz, say, sira, incelenen = {bas: 0}, {bas: 1}, deque([bas]), 0
    while sira:
        p = sira.popleft(); incelenen += 1
        for q in komsular(iz, p, engel):
            if q not in uz:
                uz[q] = uz[p] + 1; say[q] = say[p]; sira.append(q)
            elif uz[q] == uz[p] + 1:
                say[q] += say[p]
    return uz.get(son), say.get(son, 0), incelenen, uz


def en_kisa_yollar(iz, engel=True):
    n, _, _, uz = bfs(iz, engel)
    yollar = []

    def git(p, yol):
        if p == iz["son"]:
            yollar.append(yol); return
        for q in komsular(iz, p, engel):
            if uz.get(q) == uz[p] + 1:
                git(q, yol + [q])
    git(iz["bas"], [iz["bas"]])
    return yollar


def kartlar(yol, bakis=(1, 0)):
    """Robot 'bakis' yönüne bakar. Her adım: gerekirse dönüş kartı, sonra İLERİ."""
    out = []
    for a, b in zip(yol, yol[1:]):
        d = (b[0] - a[0], b[1] - a[1])
        if d != bakis:
            sol = (-bakis[1], bakis[0])
            out.append("SOLA DÖN" if d == sol else "SAĞA DÖN")
            bakis = d
        out.append("İLERİ")
    return out


def sikistir(kart):
    """Art arda gelen aynı kartları 'TEKRARLA' kartıyla birleştirir: İLERİ İLERİ İLERİ → 3 × İLERİ."""
    out = []
    for k, g in itertools.groupby(kart):
        n = len(list(g))
        out.append(f"{n} × {k}" if n > 1 else k)
    return out


# ---------- mini sudoku ----------
def _uygun(t, r, c, v):
    if v in t[r] or v in (t[i][c] for i in range(4)):
        return False
    br, bc = r // 2 * 2, c // 2 * 2
    return all(t[i][j] != v for i in range(br, br + 2) for j in range(bc, bc + 2))


def sudoku_coz(ipucu, hepsi=False):
    """Geri izleme. Dönüş: (çözümler, deneme sayısı). ipucu: 4 × 4, boş = 0."""
    t = [row[:] for row in ipucu]
    cozum, deneme = [], [0]

    def git(i):
        if i == 16:
            cozum.append([row[:] for row in t]); return not hepsi
        r, c = divmod(i, 4)
        if t[r][c]:
            return git(i + 1)
        for v in range(1, 5):
            deneme[0] += 1
            if _uygun(t, r, c, v):
                t[r][c] = v
                if git(i + 1):
                    return True
                t[r][c] = 0
        return False
    git(0)
    return cozum, deneme[0]


def sudoku_say():
    return len(sudoku_coz([[0] * 4 for _ in range(4)], hepsi=True)[0])


# ---------- kedi, fare ve peynir ----------
ESYA = ("kedi", "fare", "peynir")
TEHLIKE = [{"kedi", "fare"}, {"fare", "peynir"}]


def _guvenli(taraf):
    return not any(t <= taraf for t in TEHLIKE)


def gecis_bfs():
    """Durum: (robotun tarafı, mutfaktaki eşyalar). Robot her geçişte elinde en çok bir eşya taşır."""
    bas = (0, frozenset(ESYA)); son = (1, frozenset())
    onceki, sira, gecerli = {bas: None}, deque([bas]), {bas}
    yol_say = {bas: 1}; uz = {bas: 0}
    while sira:
        d = sira.popleft()
        r, mutfak = d
        bahce = frozenset(ESYA) - mutfak
        yaninda = mutfak if r == 0 else bahce
        for e in [None] + sorted(yaninda):
            yeni_m = set(mutfak)
            if e:
                (yeni_m.remove(e) if r == 0 else yeni_m.add(e))
            yeni = (1 - r, frozenset(yeni_m))
            geride = yeni[1] if yeni[0] == 1 else frozenset(ESYA) - yeni[1]
            if not _guvenli(set(geride)):
                continue
            gecerli.add(yeni)
            if yeni not in uz:
                uz[yeni] = uz[d] + 1; yol_say[yeni] = yol_say[d]; onceki[yeni] = (d, e); sira.append(yeni)
            elif uz[yeni] == uz[d] + 1:
                yol_say[yeni] += yol_say[d]
    adim, d = [], son
    while onceki[d]:
        d, e = onceki[d]; adim.append(e or "boş el")
    return uz[son], yol_say[son], len(gecerli), adim[::-1]


# ---------- XOX ----------
CIZGI = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]


def kazanan(t):
    for a, b, c in CIZGI:
        if t[a] != "." and t[a] == t[b] == t[c]:
            return t[a]
    return None


def xox_agac():
    """Bütün oyunları sayar: her derinlikteki düğüm, biten oyun sonuçları ve farklı tahta sayısı."""
    derinlik = [0] * 10; sonuc = {"X": 0, "O": 0, "berabere": 0}; tahtalar = set()

    def git(t, s, d):
        tahtalar.add(t); derinlik[d] += 1
        k = kazanan(t)
        if k or d == 9:
            sonuc[k or "berabere"] += 1; return
        for i in range(9):
            if t[i] == ".":
                git(t[:i] + s + t[i + 1:], "O" if s == "X" else "X", d + 1)
    git("." * 9, "X", 0)
    return derinlik, sonuc, len(tahtalar)


_bellek = {}


def xox_deger(t, s):
    """Minimaks: +1 X kazanır, 0 berabere, −1 O kazanır (iki taraf da en iyi oynarsa)."""
    if (t, s) in _bellek:
        return _bellek[(t, s)]
    k = kazanan(t)
    if k:
        v = 1 if k == "X" else -1
    elif "." not in t:
        v = 0
    else:
        dg = [xox_deger(t[:i] + s + t[i + 1:], "O" if s == "X" else "X") for i in range(9) if t[i] == "."]
        v = max(dg) if s == "X" else min(dg)
    _bellek[(t, s)] = v
    return v


def xox_robot(t, s):
    bos = [i for i in range(9) if t[i] == "."]
    dg = {i: xox_deger(t[:i] + s + t[i + 1:], "O" if s == "X" else "X") for i in bos}
    en = max(dg.values()) if s == "X" else min(dg.values())
    return min(i for i in bos if dg[i] == en)


def xox_mac(robot, rng):
    """robot: 'X' ya da 'O'. Öteki oyuncu rastgele oynar. Dönüş: kazanan ya da 'berabere'."""
    t, s = "." * 9, "X"
    while not kazanan(t) and "." in t:
        i = xox_robot(t, s) if s == robot else rng.choice([j for j in range(9) if t[j] == "."])
        t = t[:i] + s + t[i + 1:]; s = "O" if s == "X" else "X"
    return kazanan(t) or "berabere"


# ---------- alma oyunu (Nim) ----------
def nim_tablo(n, en_cok=3):
    """kazanir[k]: sırası gelen oyuncu k küp varken (en iyi oynarsa) kazanır mı? Sonuncuyu alan kazanır."""
    kazanir = [False] * (n + 1)
    for k in range(1, n + 1):
        kazanir[k] = any(not kazanir[k - a] for a in range(1, min(en_cok, k) + 1))
    return kazanir


def nim_robot(k, en_cok=3):
    a = k % (en_cok + 1)
    return a if a else 1


def nim_mac(n, rng, en_cok=3):
    """Robot başlar ve kuralla oynar, rakip rastgele alır. Dönüş: kazanan."""
    k, sira = n, "robot"
    while True:
        a = nim_robot(k, en_cok) if sira == "robot" else rng.randint(1, min(en_cok, k))
        k -= a
        if k == 0:
            return sira
        sira = "rakip" if sira == "robot" else "robot"


# ---------- mangala (kaynaklar.py mangala_kural: dört temel kural) ----------
# Dizin: 0–5 A oyuncusunun kuyuları (soldan sağa), 6 A'nın hazinesi, 7–12 B'nin kuyuları, 13 B'nin hazinesi.
def mangala_bas():
    return [4] * 6 + [0] + [4] * 6 + [0]


def mangala_yer(i):
    """Dizini okunur ada çevirir: 0–5 → 'A 1. kuyu'…, 6 → 'A hazinesi', 7–12 → 'B 1. kuyu'…, 13 → 'B hazinesi'."""
    return "A hazinesi" if i == 6 else "B hazinesi" if i == 13 else (f"A {i + 1}. kuyu" if i < 6 else f"B {i - 6}. kuyu")


def mangala_hamle(tahta, oyuncu, kuyu):
    """oyuncu 0 (A) ya da 1 (B), kuyu 0–5. Dönüş: (yeni tahta, son taşın yeri, tekrar oynar mı, alınan taş)."""
    t = tahta[:]
    bas = kuyu + (0 if oyuncu == 0 else 7)
    hazine, rakip_hazine = (6, 13) if oyuncu == 0 else (13, 6)
    tas = t[bas]
    assert tas > 0
    t[bas] = 0
    if tas == 1:                       # 1. kural: tek taş sağdaki kuyuya
        yer = (bas + 1) % 14
        t[yer] += 1
    else:                              # 1. kural: bir taş aldığı kuyuya, kalanlar sağa doğru
        yer = bas; t[yer] += 1; tas -= 1
        while tas:
            yer = (yer + 1) % 14
            if yer == rakip_hazine:    # 2. kural: rakibin hazinesine taş bırakılmaz
                continue
            t[yer] += 1; tas -= 1
    if yer == hazine:
        return t, yer, True, 0
    alinan = 0
    kendi = range(0, 6) if oyuncu == 0 else range(7, 13)
    if yer not in kendi and t[yer] % 2 == 0:          # 2. kural: rakip kuyusu çift olursa hepsi alınır
        alinan = t[yer]; t[hazine] += alinan; t[yer] = 0
    elif yer in kendi and t[yer] == 1:                # 3. kural: kendi boş kuyusu, karşısı doluysa
        karsi = 12 - yer
        if t[karsi]:
            alinan = t[karsi] + 1; t[hazine] += alinan; t[karsi] = 0; t[yer] = 0
    return t, yer, False, alinan


def mangala_durum_say(derinlik):
    """İlk 'derinlik' hamlede (tekrar oynama dahil her taş dağıtımı bir hamle) kaç farklı tahta oluşur."""
    katman = {(tuple(mangala_bas()), 0)}
    sayilar = []
    for _ in range(derinlik):
        yeni = set()
        for t, o in katman:
            for k in range(6):
                if t[k + (0 if o == 0 else 7)]:
                    nt, _, tekrar, _ = mangala_hamle(list(t), o, k)
                    yeni.add((tuple(nt), o if tekrar else 1 - o))
        katman = yeni
        sayilar.append(len(katman))
    return sayilar


# ---------- kareli parçalar ----------
def _normal(h):
    mx = min(x for x, y in h); my = min(y for x, y in h)
    return tuple(sorted((x - mx, y - my) for x, y in h))


def _donusler(h, yansima=True):
    out = set()
    for f in ((1, 1), (-1, 1)) if yansima else ((1, 1),):
        g = [(x * f[0], y * f[1]) for x, y in h]
        for _ in range(4):
            g = [(y, -x) for x, y in g]
            out.add(_normal(g))
    return out


def polyomino(n, serbest=True):
    """n kareli bütün parçalar. serbest=True: döndürme ve yansıma aynı sayılır; False: yalnız aynı duruş aynı."""
    parca = {((0, 0),)}
    for _ in range(n - 1):
        yeni = set()
        for p in parca:
            for x, y in p:
                for dx, dy in YON:
                    q = (x + dx, y + dy)
                    if q not in p:
                        yeni.add(_normal(p + (q,)))
        parca = yeni
    if not serbest:
        return sorted(parca)
    temsil = {}
    for p in parca:
        temsil.setdefault(min(_donusler(p)), p)
    return sorted(temsil)


def ayna_dogrusu(p):
    """Parçanın kaç ayna simetrisi doğrusu var (dikey, yatay ve iki köşegen)."""
    p = set(_normal(p)); n = 0
    for f in (lambda x, y: (-x, y), lambda x, y: (x, -y), lambda x, y: (y, x), lambda x, y: (-y, -x)):
        if set(_normal([f(x, y) for x, y in p])) == p:
            n += 1
    return n


def doseme_say(en, boy, parcalar, limit=None):
    """Dikdörtgeni her parçayı tam bir kez kullanarak döşer. Dönüş: (döşeme sayısı, ilk döşeme)."""
    duruslar = [sorted(_donusler(p)) for p in parcalar]
    tahta = {}
    ilk, say = [None], [0]

    def bos():
        for x in range(en):
            for y in range(boy):
                if (x, y) not in tahta:
                    return x, y
        return None

    kalan = set(range(len(parcalar)))

    def git():
        b = bos()
        if b is None:
            say[0] += 1
            if ilk[0] is None:
                ilk[0] = dict(tahta)
            return
        if limit and say[0] >= limit:
            return
        bx, by = b
        for i in sorted(kalan):
            for d in duruslar[i]:
                ax, ay = min(d)                     # sol-alt kare boş kareye otursun
                hs = [(bx + x - ax, by + y - ay) for x, y in d]
                if all(0 <= x < en and 0 <= y < boy and (x, y) not in tahta for x, y in hs):
                    for h in hs:
                        tahta[h] = i
                    kalan.remove(i)
                    git()
                    kalan.add(i)
                    for h in hs:
                        del tahta[h]
    git()
    return say[0], ilk[0]


def kup_acinimi_mi(p):
    """Küpü açınımın bir karesine koyup komşu karelere yuvarlarız; altı kare küpün altı farklı yüzüne değmeli."""
    p = set(p); bas = min(p)
    # küp yönü: (alt, üst, kuzey, güney, doğu, batı) yüzlerinin numaraları
    yuz = {bas: (0, 1, 2, 3, 4, 5)[0]}
    sira = deque([(bas, (0, 1, 2, 3, 4, 5))])
    gorulen = {bas}
    while sira:
        (x, y), (a, u, k, g, d, b) = sira.popleft()
        for (dx, dy), yeni in (((1, 0), (d, b, k, g, u, a)), ((-1, 0), (b, d, k, g, a, u)),
                               ((0, 1), (k, g, u, a, d, b)), ((0, -1), (g, k, a, u, d, b))):
            q = (x + dx, y + dy)
            if q in p and q not in gorulen:
                gorulen.add(q); yuz[q] = yeni[0]; sira.append((q, yeni))
    return len(set(yuz.values())) == 6


# ---------- hafıza oyunu ----------
def hafiza_oyunu(cift, rng, bellek=True):
    """2 × cift kart. Her hamlede iki kart açılır. Dönüş: bütün çiftler bulunana kadar hamle sayısı."""
    kart = list(range(cift)) * 2; rng.shuffle(kart)
    kapali, bilinen, hamle = set(range(len(kart))), {}, 0
    while kapali:
        hamle += 1
        if bellek:
            cift_bil = [(i, j) for i in kapali for j in kapali if i < j and i in bilinen and j in bilinen and kart[i] == kart[j]]
            if cift_bil:
                i, j = cift_bil[0]
            else:
                bilinmeyen = [i for i in kapali if i not in bilinen]
                i = rng.choice(bilinmeyen); bilinen[i] = kart[i]
                es = [j for j in kapali if j != i and j in bilinen and kart[j] == kart[i]]
                if es:
                    j = es[0]
                else:
                    kalan = [j for j in bilinmeyen if j != i]
                    j = rng.choice(kalan); bilinen[j] = kart[j]
        else:
            i, j = rng.sample(sorted(kapali), 2)
        if kart[i] == kart[j]:
            kapali -= {i, j}
    return hamle

"""Zekâ Oyunları ve Robot Bulmacaları — lab ortak araçları.
Veri: veri/cay_servisi_kaydi.csv (insansı robotun kafede çay servisi BENZETİM KAYDI, saniyede 50 örnek),
veri/sag_kol_parametre.csv (sağ kol eklem sınırları) ve veri/sag_kol_kutle.csv (sağ kol parça kütleleri),
ikisi de benzetim parametre dosyası. Bunlardan ya da kaynaklar.py'deki gerçek kaynaklardan gelmeyen her sayı ÖRNEK'tir.
Bulmacalar (yol bulma, mini sudoku, XOX, mangala, pentomino, küp açınımı) Python ile gerçekten çözülür ve sayılır.

  oturum(ders, ad, kod)          : kodu Python etkileşimli oturumu gibi çalıştırır → ekran/<ders>/<ad>.txt
  grafik(ders, ad, baslik, ciz)  : Matplotlib çizimi → ekran/<ders>/<ad>.png ("Gerçek koşum çıktısı" etiketiyle)
  olc(anahtar=değer)             : ölçümü OLCUMLER.json'a yazar (derslerdeki bütün sayılar buradan gelir)
"""
import ast, contextlib, io, json, os, pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

LAB = pathlib.Path(__file__).resolve().parent
OLC = LAB / "OLCUMLER.json"
os.chdir(LAB)   # oturumlardaki göreli yollar (veri/…) lab klasörüne göredir
np.set_printoptions(precision=3, suppress=True, linewidth=88)
plt.rcParams.update({"font.size": 22, "font.family": "DejaVu Sans", "axes.grid": True, "grid.alpha": 0.3})

MAVI, TURUNCU, YESIL, MOR, GRI = "#2563eb", "#ea580c", "#16a34a", "#7c3aed", "#6b7280"


def kayit():
    """Çay servisi benzetim kaydı: sütun adı → dizi."""
    d = np.genfromtxt(LAB / "veri/cay_servisi_kaydi.csv", delimiter=",", names=True)
    return {k: d[k] for k in d.dtype.names}


def parametre():
    """Sağ kol eklem parametreleri (benzetim parametre dosyası): kısa ad → sözlük."""
    d = np.genfromtxt(LAB / "veri/sag_kol_parametre.csv", delimiter=",", names=True, dtype=None, encoding="utf-8")
    return {str(r["ad"]): {k: r[k] for k in d.dtype.names} for r in d}


def kutle():
    """Sağ kol parça kütleleri (benzetim parametre dosyası): parça adı → sözlük."""
    d = np.genfromtxt(LAB / "veri/sag_kol_kutle.csv", delimiter=",", names=True, dtype=None, encoding="utf-8")
    return {str(r["parca"]): {k: r[k] for k in d.dtype.names} for r in d}


def evreler(k=None, esik=0.02):
    """Bardağın yatay hızına göre evreler: hızın eşiği ilk aştığı ve son kez aştığı an (saniye)."""
    k = k or kayit()
    t, x, y = k["zaman_s"], k["bardak_x_m"], k["bardak_y_m"]
    # bir saniyelik pencerelerle yatay hız (gürültüyü yumuşatmak için)
    n = 50
    v = np.hypot(x[n:] - x[:-n], y[n:] - y[:-n]) / (t[n:] - t[:-n])
    hareket = np.where(v > esik)[0]
    bas, son = t[hareket[0]], t[hareket[-1] + n]
    return float(round(bas, 2)), float(round(son, 2))


def _j(v):
    if isinstance(v, np.ndarray):
        return [_j(x) for x in v.tolist()]
    if isinstance(v, (list, tuple)):
        return [_j(x) for x in v]
    if isinstance(v, dict):
        return {k: _j(x) for k, x in v.items()}
    if isinstance(v, (float, np.floating)):
        return round(float(v), 4)
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, np.bool_):
        return bool(v)
    return v


def olc(**kw):
    d = json.loads(OLC.read_text()) if OLC.exists() else {}
    d.update({k: _j(v) for k, v in kw.items()})
    OLC.write_text(json.dumps(d, ensure_ascii=False, indent=1))


def oturum(ders, ad, kod, ns=None):
    """Kodu etkileşimli Python oturumu gibi çalıştırır: ifadenin değeri yazdırılır, atama sessizdir."""
    ns = {} if ns is None else ns
    ns.setdefault("__name__", "__oturum__")
    kod = kod.strip("\n")
    agac = ast.parse(kod)
    satirlar = kod.splitlines()
    out = []
    for st in agac.body:
        parca = satirlar[st.lineno - 1: st.end_lineno]
        out.append(">>> " + parca[0])
        out += ["... " + l for l in parca[1:]]
        if len(parca) > 1:
            out.append("...")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            if isinstance(st, ast.Expr):
                v = eval(compile(ast.Expression(st.value), "<oturum>", "eval"), ns)
                if v is not None:
                    print(repr(v))
            else:
                exec(compile(ast.Module([st], []), "<oturum>", "exec"), ns)
        out += buf.getvalue().rstrip("\n").splitlines() if buf.getvalue() else []
    yol = LAB / "ekran" / ders / f"{ad}.txt"
    yol.parent.mkdir(parents=True, exist_ok=True)
    yol.write_text("\n".join(out) + "\n", encoding="utf-8")
    return ns


def grafik(ders, ad, baslik, ciz, kaynak="Matplotlib", alt=None):
    """ciz(fig) ile çizilen şekli 1920 × 1080 PNG'ye yazar; üst şeritte 'Gerçek koşum çıktısı' etiketi."""
    fig = plt.figure(figsize=(19.2, 10.8), dpi=100)
    fig.patch.set_facecolor("white")
    ciz(fig)
    fig.patches.append(matplotlib.patches.Rectangle((0, 0.925), 1, 0.075, transform=fig.transFigure, fc="#1f2a37", zorder=0))
    fig.text(0.016, 0.962, baslik, color="white", fontsize=26, va="center", ha="left")
    fig.text(0.984, 0.962, f"Gerçek koşum çıktısı · ders {ders}", color="#c7d7ea", fontsize=19, va="center", ha="right")
    fig.text(0.016, 0.895, alt or f"Python 3.12 · NumPy → {kaynak}", color=GRI, fontsize=17, va="center", ha="left")
    yol = LAB / "ekran" / ders / f"{ad}.png"
    yol.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(yol, dpi=100, facecolor="white")
    plt.close(fig)
    return yol


def eksen(fig, sol=0.08, alt=0.1, en=0.88, boy=0.72):
    return fig.add_axes([sol, alt, en, boy])


def tr(x, basamak=1):
    return f"{x:.{basamak}f}".replace(".", ",")

import json, glob, pathlib
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
H = pathlib.Path(__file__).parent
for f in glob.glob("/usr/share/fonts/opentype/inter/Inter-*.otf"): fm.fontManager.addfont(f)
plt.rcParams.update({"font.family": "Inter", "font.size": 8.5, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#9aa3ad", "xtick.color": "#4a5563", "ytick.color": "#2b3440"})
F = json.load(open(H / "fac.json"))
units = [("t1", "inspire", "INSPIRE ← MIMIC-IV + eICU-CRD"), ("t1", "mimic", "MIMIC-IV ← INSPIRE + eICU-CRD"),
         ("t1", "eicu", "eICU-CRD ← INSPIRE + MIMIC-IV"), ("t1", "NWICU (mimic+eicu)", "NWICU ← MIMIC-IV + eICU-CRD"),
         ("t1", "NWICU (inspire+eicu)", "NWICU ← INSPIRE + eICU-CRD"), ("t1", "NWICU (inspire+mimic)", "NWICU ← INSPIRE + MIMIC-IV"),
         ("t2", "aki", "PRAM setting · AKI"), ("t2", "death", "PRAM setting · 168-h mortality")]
cfg = [("kNN alone · diagonal NCA (PERISIM)", {"t1": "home", "t2": "UI"}, "#3F7D2B", "o"),
       ("kNN alone · full-matrix NCA", {"t1": "I", "t2": "U"}, "#8DC971", "s"),
       ("mixture · diagonal NCA", {"t1": "U", "t2": "I"}, "#5B62C0", "D"),
       ("mixture · full-matrix NCA (PRAM)", {"t1": "UI", "t2": "home"}, "#C0185A", "^")]
fig, ax = plt.subplots(figsize=(7.2, 4.1))
n = len(units)
for i, (t, u, lab) in enumerate(units):
    y = n - 1 - i + (0 if t == "t1" else -0.6)
    for j, (cl, m, col, mk) in enumerate(cfg):
        d, lo, hi = F[t][u][m[t]]; yy = y + 0.27 - j * 0.18
        ax.plot([lo, hi], [yy, yy], color=col, lw=1.3); ax.plot(d, yy, mk, color=col, ms=4.5, label=cl if i == 0 else None)
ys = [n - 1 - i + (0 if t == "t1" else -0.6) for i, (t, _, _) in enumerate(units)]
ax.set_yticks(ys); ax.set_yticklabels([u[2] for u in units])
ax.axvline(0, color="#7a8591", lw=0.9)
ax.axhline(1.2, color="#c7ced6", lw=0.8, ls="--")
ax.text(-0.0235, 0.98, "Tier 2: PRAM's setting rebuilt (MIMIC-IV → eICU-CRD)", fontsize=7, color="#4a5563", ha="left")
ax.text(-0.0235, n - 0.55, "Tier 1: PERISIM's setting (4 databases)", fontsize=7, color="#4a5563", ha="left")
ax.set_xlabel("Δ AUROC = learned metric (NCA) − cosine, 95 % CI;  > 0: the learned metric is better")
ax.legend(fontsize=7, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2)
ax.set_xlim(-0.024, 0.040)
plt.tight_layout(); plt.savefig(H / "figure1.svg"); plt.savefig(H / "figure1.png", dpi=250); plt.close(); print("ok")

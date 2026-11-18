import re, json, pathlib
H = pathlib.Path(__file__).parent
P = H.parent / 'results' / 'pram'
def parse(md, key):
    out, cur = {}, None
    sec = md.split("## Rule (pre-specified)")[1].split("##")[0]
    for line in sec.splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 5 or c[0] in ("target", "outcome") or (c[0] and set(c[0]) <= set("-")): continue
        if c[0]: cur = c[0]; out[cur] = {"home": c[1]}
        out[cur][c[2]] = c[3]
    num = lambda s: [float(x) for x in re.findall(r"[+-]?\d\.\d{4}", s)[:3]]
    return {u: {k: num(v) for k, v in d.items() if k in ("home", "U", "I", "UI")} for u, d in out.items()}
t1 = parse(open(P / "tier1.md").read(), "target")
t2 = parse(open(P / "tier2.md").read(), "outcome")
json.dump({"t1": t1, "t2": t2}, open(H / "fac.json", "w"), indent=1); print("fac.json written")

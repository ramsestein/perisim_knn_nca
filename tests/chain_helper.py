"""Shared synthetic chain for script tests: landmarks, CV, freeze and the external stage (from PERISIM's tests)."""

def _chain(tmp_path, monkeypatch, parts):
    from hypo.config import load
    from test_hypo_external import _xframe

    cfg = load()
    monkeypatch.setenv("PERISIM_WORKDIR", str(tmp_path))
    d = tmp_path / "experiments" / "hypo" / "landmarks"
    d.mkdir(parents=True)
    frames = {}
    for i, c in enumerate(cfg["cohorts"]):
        frames[c] = _xframe(c, 120, 4, 10 + i)
        frames[c].write_parquet(d / f"{c}.parquet")
    from hypo.cv import run
    from hypo.external import Stage
    from hypo.frozen import final, freeze

    run(cfg["cohorts"], ["prevalence", "euclidean", "lightgbm"], None, quick=False, threads=1)
    final(quick=True, threads=1)
    freeze("TEST", no_git=True, quick=True)
    Stage(quick=True, threads=1).run(["eicu"], folds=[0, 1], parts=parts)
    return frames



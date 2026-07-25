# scripts/divergence — randomizer divergence analysis tooling

Tooling to diagnose why the Platinum **zone-accessibility** model diverges from
the reference **`main`** (flat-accessibility) model for a given seed, so the two
can be made byte-identical.

Quick start:

```bash
# Classify the first divergence for a seed (records current tree + main worktree).
python scripts/divergence/analyze.py compare --seed 1

# Why is a map reachable / not? Run in both checkouts and compare.
python scripts/divergence/inspect_reach.py replay 1 37 Map_Celestic_Town_00

# Show a map's warp + zone/rules structure.
python scripts/divergence/inspect_reach.py dumpmap Map_Route_210_05
```

Full explanation of the system, the workflow, the divergence kinds, and the
common root causes with their zone-native fixes is in **[SKILL.md](../../.github/skills/divergence/SKILL.md)**.

Files:
- `analyze.py` — orchestrator/CLI (`compare`, `record`, `diff`).
- `record_seed.py` — self-contained per-step recorder (start/end, PRNG advances,
  reachable pool, ends/connects). Copied into the reference worktree by `analyze.py`.
- `inspect_reach.py` — self-contained `replay` (reachability at a step) and
  `dumpmap` (map structure) inspector.


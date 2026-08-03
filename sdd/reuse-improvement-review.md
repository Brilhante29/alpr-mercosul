# Reuse Improvement Review

Project: `5 - alpr-mercosul`

## Review Points

- [x] after scaffold
- [x] after architecture decision
- [x] after first working slice
- [x] after benchmark result
- [x] before publication

## Findings

| Finding | Classification | Kit Area | Action | Status |
|---|---|---|---|---|
| Run repetition was incorrectly used as measured workload size. | `patch_now` | benchmark producer and skill | separate `repeat` from explicit or derived work-item counts | completed in kit `6f557a0` |
| Published evidence must be validated from committed source rather than mutable worktree files. | `patch_now` | central validator | read publication inputs from Git `HEAD` and report dirt independently | completed in kit `16a3622` |
| Image-only prediction needs a negative label-leakage test. | `backlog` | CV benchmark guidance | extract a generic rule only after a second labeled CV project proves the same boundary | recorded |
| ALPR glyph rendering and fixed-cell matcher should move into the kit. | `reject` | project implementation | keep domain-specific rendering and OCR local | rejected |

## Reuse Applied

- Synchronized `generate-publication-benchmark.py` and matching Codex/Claude `publish-benchmark-evidence` skills.
- Reused V2 provenance, clean-source, image-digest and measured-workload contracts.
- Kept the workload config and pixel matcher project-owned.

## Final Gate

- [x] Reusable improvements were patched or recorded.
- [x] Project-specific implementation was not moved into the kit.
- [x] Validation reflects the image-only OCR and 100-plate V2 workload contract.

# Reuse Map: #5 alpr-mercosul

| Kit input or delta | Use | Resolution |
|---|---|---|
| benchmark V2 contract and producer | bind source, image, workload and raw result | reused |
| Python computer-vision profile | package, Docker and test conventions | reused |
| workload repetition semantics | distinguish runs from 100 measured plates | improved kit |
| plate renderer, glyphs and matcher | specific to the synthetic OCR claim | keep local |
| real-road ALPR architecture | unsupported by current evidence | reject until a new workload exists |

Reuse preserves evidence semantics without pretending the project-specific OCR implementation is a general framework.

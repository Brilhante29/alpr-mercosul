# Decision Register: #5 alpr-mercosul

| Decision | Selected option | Reason | Revisit trigger |
|---|---|---|---|
| Architecture | image-generation -> OCR -> evaluation pipeline | directional stages and label isolation dominate | transport or infrastructure boundaries appear |
| OCR | deterministic template matcher | proves image-derived prediction without downloads | real-road dataset becomes available |
| Interface | CLI | benchmark and demo are offline artifacts | online serving becomes a separate claim |
| Dataset | seeded synthetic fixed layout | transparent and reproducible first workload | detection or generalization becomes the claim |
| Messaging/cloud/storage | none | no matching semantics exist | a measured requirement is introduced |

Perfect synthetic accuracy is never described as real-road accuracy. Any new renderer, data source or OCR backend requires a new workload version and comparability key.

---
name: deployment-automation
description: Diseño de scripts Python reproducibles para Git, GitHub, QA y despliegues controlados sin depender de Codex.
---

# Deployment automation

Aplicar este skill cuando se modifiquen los scripts de `03_DEPLOYMENT`.

1. Usar `argparse`, validaciones y códigos de salida.
2. Usar `subprocess` con listas y sin `shell=True` cuando sea posible.
3. Mantener `--help`, modo seguro y confirmación para cambios externos.
4. No guardar credenciales ni ejecutar producción.
5. Verificar respaldos, reversión y estado previo antes de habilitar un despliegue autorizado.

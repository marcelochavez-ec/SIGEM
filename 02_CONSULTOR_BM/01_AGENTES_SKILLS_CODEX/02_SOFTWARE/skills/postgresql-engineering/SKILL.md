---
name: postgresql-engineering
description: Inspección, documentación y validación no destructiva de PostgreSQL y su relación con Django.
---

# PostgreSQL engineering

Aplicar este skill cuando se revisen esquemas, tablas, vistas, consultas, índices o relaciones PostgreSQL.

1. Confirmar conexión y nombres reales antes de asumir columnas.
2. Usar consultas de lectura y explicar schema.tabla.
3. No ejecutar `DROP`, `TRUNCATE`, `DELETE` ni migraciones remotas sin autorización.
4. Verificar duplicados antes de proponer unicidad.
5. Documentar impacto, rendimiento y dependencia con los modelos Django.

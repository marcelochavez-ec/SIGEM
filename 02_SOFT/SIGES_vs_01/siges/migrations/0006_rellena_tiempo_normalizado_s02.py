from django.db import migrations


class Migration(migrations.Migration):
    """Rellena horas y minutos normalizados sin alterar respuestas historicas."""

    # Depende de la creacion de columnas normalizadas.
    dependencies = [
        ("siges", "0005_normaliza_tiempo_s02"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE respuesta_s02 DROP CONSTRAINT IF EXISTS ck_respuesta_s02_am04_rango_unidad;
            ALTER TABLE respuesta_s02 DROP CONSTRAINT IF EXISTS ck_respuesta_s02_am05_categoria;

            UPDATE respuesta_s02
            SET
                s02_am04_horas = CASE
                    WHEN s02_am04_unidad = 'Horas'
                        THEN FLOOR(s02_am04)::integer
                            + CASE
                                WHEN ROUND((s02_am04 - FLOOR(s02_am04)) * 60) = 60 THEN 1
                                ELSE 0
                              END
                    ELSE 0
                END,
                s02_am04_minutos = CASE
                    WHEN s02_am04_unidad = 'Horas'
                        THEN CASE
                            WHEN ROUND((s02_am04 - FLOOR(s02_am04)) * 60) = 60 THEN 0
                            ELSE ROUND((s02_am04 - FLOOR(s02_am04)) * 60)::integer
                        END
                    WHEN s02_am04_unidad = 'Minutos'
                         AND s02_am04 = FLOOR(s02_am04)
                         AND s02_am04 BETWEEN 1 AND 59
                        THEN s02_am04::integer
                    ELSE s02_am04_minutos
                END
            WHERE s02_am04 IS NOT NULL;

            ALTER TABLE respuesta_s02
            ADD CONSTRAINT ck_respuesta_s02_am04_rango_unidad
            CHECK (
                (s02_am04_unidad = 'Horas' AND s02_am04 >= 1)
                OR (
                    s02_am04_unidad = 'Minutos'
                    AND s02_am04 >= 1
                    AND s02_am04 <= 59
                    AND s02_am04 = FLOOR(s02_am04)
                )
            ) NOT VALID;

            ALTER TABLE respuesta_s02
            ADD CONSTRAINT ck_respuesta_s02_am05_categoria
            CHECK (UPPER(TRIM(s02_am05)) IN ('URBANO', 'RURAL')) NOT VALID;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

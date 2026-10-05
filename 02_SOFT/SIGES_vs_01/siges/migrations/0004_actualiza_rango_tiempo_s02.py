from django.db import migrations


class Migration(migrations.Migration):
    """Actualiza la regla de tiempo de traslado de S02 en bases ya migradas."""

    # La migracion parte de la ultima estructura registrada para el aplicativo.
    dependencies = [
        ("siges", "0003_establecimientoingresado"),
    ]

    # RunSQL modifica restricciones fisicas sin alterar columnas ni datos.
    operations = [
        migrations.RunSQL(
            sql="""
            -- Se retiran restricciones anteriores porque permitian cero o no validaban horas.
            ALTER TABLE respuesta_s02 DROP CONSTRAINT IF EXISTS ck_respuesta_s02_am04_no_negativo;
            ALTER TABLE respuesta_s02 DROP CONSTRAINT IF EXISTS ck_respuesta_s02_am04_minutos;
            ALTER TABLE respuesta_s02 DROP CONSTRAINT IF EXISTS ck_respuesta_s02_am04_rango_unidad;
            -- La regla vigente exige horas >= 1 y minutos entre 1 y 59.
            ALTER TABLE respuesta_s02
            ADD CONSTRAINT ck_respuesta_s02_am04_rango_unidad
            CHECK (
                (s02_am04_unidad = 'Horas' AND s02_am04 >= 1)
                OR (s02_am04_unidad = 'Minutos' AND s02_am04 >= 1 AND s02_am04 <= 59)
            ) NOT VALID;
            """,
            # No se define reversa para evitar restaurar una regla funcional obsoleta.
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]

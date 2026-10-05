from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("siges", "0001_initial"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    sql="""
                    ALTER TABLE siges_formulario
                    ADD COLUMN IF NOT EXISTS nivel_atencion varchar(80) NOT NULL DEFAULT 'I NIVEL DE ATENCION';

                    CREATE INDEX IF NOT EXISTS siges_formulario_nivel_atencion_idx
                    ON siges_formulario (nivel_atencion);
                    """,
                    reverse_sql="""
                    DROP INDEX IF EXISTS siges_formulario_nivel_atencion_idx;
                    ALTER TABLE siges_formulario DROP COLUMN IF EXISTS nivel_atencion;
                    """,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="sigesformulario",
                    name="nivel_atencion",
                    field=models.CharField(db_index=True, default="I NIVEL DE ATENCION", max_length=80),
                ),
            ],
        ),
    ]



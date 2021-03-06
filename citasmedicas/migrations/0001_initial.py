# Generated by Django 2.2.6 on 2019-12-11 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='especialidad',
            fields=[
                ('especialidad_ak', models.AutoField(primary_key=True, serialize=False)),
                ('especialidad_nombre', models.CharField(max_length=50)),
                ('especialidad_abrev', models.CharField(max_length=7)),
            ],
            options={
                'db_table': 'especialidad',
            },
        ),
        migrations.CreateModel(
            name='paciente',
            fields=[
                ('paciente_ak', models.AutoField(primary_key=True, serialize=False)),
                ('paciente_dni', models.CharField(max_length=8)),
                ('paciente_nombres', models.CharField(max_length=50)),
                ('paciente_appaterno', models.CharField(max_length=50)),
                ('paciente_apmaterno', models.CharField(max_length=50)),
                ('paciente_telefono', models.IntegerField()),
            ],
            options={
                'db_table': 'paciente',
            },
        ),
        migrations.CreateModel(
            name='medico',
            fields=[
                ('medico_ak', models.AutoField(primary_key=True, serialize=False)),
                ('medico_nombres', models.CharField(max_length=50)),
                ('medico_appaterno', models.CharField(max_length=50)),
                ('medico_apmaterno', models.CharField(max_length=50)),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citasmedicas.paciente')),
            ],
            options={
                'db_table': 'medico',
            },
        ),
        migrations.CreateModel(
            name='horario',
            fields=[
                ('horario_ak', models.AutoField(primary_key=True, serialize=False)),
                ('horario_dia', models.CharField(max_length=15)),
                ('horario_ingreso', models.TimeField()),
                ('horario_salida', models.TimeField()),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citasmedicas.medico')),
            ],
            options={
                'db_table': 'horario',
            },
        ),
        migrations.CreateModel(
            name='cita',
            fields=[
                ('cita_ak', models.AutoField(primary_key=True, serialize=False)),
                ('cita_fecha', models.DateField()),
                ('cita_hora', models.TimeField()),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citasmedicas.medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citasmedicas.paciente')),
            ],
            options={
                'db_table': 'cita',
            },
        ),
    ]

# Generated by Django 5.0.14 on 2025-07-07 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reuniones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=50, unique=True, verbose_name='DNI')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('establecimiento', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre de la IPRESS')),
                ('codigo', models.CharField(blank=True, max_length=20, null=True, verbose_name='Código de la IPRESS')),
                ('categoria', models.CharField(blank=True, max_length=100, null=True, verbose_name='Categoría')),
                ('departamento', models.CharField(blank=True, max_length=100, null=True, verbose_name='Departamento')),
                ('provincia', models.CharField(blank=True, max_length=100, null=True, verbose_name='Provincia')),
                ('distrito', models.CharField(blank=True, max_length=100, null=True, verbose_name='Distrito')),
                ('disa', models.CharField(blank=True, max_length=100, null=True, verbose_name='DISA')),
                ('institucion', models.CharField(blank=True, max_length=100, null=True, verbose_name='Institucion')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('eventos', models.ManyToManyField(blank=True, related_name='participantes', to='reuniones.evento')),
            ],
        ),
    ]

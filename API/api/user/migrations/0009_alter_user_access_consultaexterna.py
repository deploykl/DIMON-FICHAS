# Generated by Django 5.0.14 on 2025-07-16 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_remove_perfilestablecimiento_establecimiento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='access_ConsultaExterna',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 5.0.14 on 2025-06-25 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ficha', '0017_seguimientomatrizcompromiso_usuario_creacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='matrizcompromiso',
            name='alertas_enviadas',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='matrizcompromiso',
            name='proxima_alerta',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='matrizcompromiso',
            name='ultima_alerta_enviada',
            field=models.DateField(blank=True, null=True),
        ),
    ]

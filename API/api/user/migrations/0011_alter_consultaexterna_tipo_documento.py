# Generated by Django 5.0.14 on 2025-07-16 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_consultaexterna_tipo_seguro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultaexterna',
            name='tipo_documento',
            field=models.CharField(max_length=50),
        ),
    ]

# Generated by Django 5.0.14 on 2025-06-19 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ficha', '0009_matrizcompromiso_funcionario_d_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matrizcompromiso',
            old_name='funcionario_eo',
            new_name='funcionario_e',
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-04 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appejemplares', '0002_alter_libro_options_alter_libro_categoria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='autor',
            field=models.CharField(max_length=100, null='False', verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='titulo',
            field=models.CharField(max_length=100, null='False', verbose_name='Título'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='ubicacion',
            field=models.CharField(max_length=20, null='False', verbose_name='Ubicación'),
        ),
    ]

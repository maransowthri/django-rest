# Generated by Django 3.1.7 on 2021-02-25 04:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='tag',
            new_name='tags',
        ),
    ]

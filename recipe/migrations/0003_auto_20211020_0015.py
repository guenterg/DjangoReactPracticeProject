# Generated by Django 3.2.8 on 2021-10-20 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_detailedrecipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailedrecipe',
            name='calories',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='detailedrecipe',
            name='origin_id',
            field=models.OneToOneField(default=-1, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='recipe.recipe'),
        ),
    ]
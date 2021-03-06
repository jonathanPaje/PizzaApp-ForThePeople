# Generated by Django 3.1.7 on 2021-03-05 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizza',
            name='name',
        ),
        migrations.AddField(
            model_name='pizza',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pizza.user'),
        ),
    ]

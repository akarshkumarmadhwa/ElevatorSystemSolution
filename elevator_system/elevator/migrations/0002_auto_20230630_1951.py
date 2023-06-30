# Generated by Django 3.2.19 on 2023-06-30 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elevator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elevator',
            name='elevator_system',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='elevator', to='elevator.elevatorsystem'),
        ),
        migrations.AlterField(
            model_name='elevatorrequest',
            name='elevator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='elevator_request', to='elevator.elevator'),
        ),
    ]
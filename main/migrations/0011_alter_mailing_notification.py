# Generated by Django 4.2 on 2024-08-07 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_mailing_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='notification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.notification', verbose_name='Сообщение'),
        ),
    ]

# Generated by Django 4.2 on 2024-08-06 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blog_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='published',
            field=models.BooleanField(default=True, verbose_name='Признак публикации'),
        ),
    ]
# Generated by Django 4.1.7 on 2023-02-18 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='historico',
            name='hour',
            field=models.CharField(max_length=30, null=True),
        ),
    ]

# Generated by Django 4.1.2 on 2022-11-24 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0009_audiofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofile',
            name='upload',
            field=models.FileField(upload_to='file'),
        ),
    ]
# Generated by Django 4.1.2 on 2022-11-22 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_alter_externalfile_filetype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='externalfile',
            name='upload',
            field=models.ImageField(upload_to='file'),
        ),
    ]
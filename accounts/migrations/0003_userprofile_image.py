# Generated by Django 4.1.13 on 2024-08-05 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile_kayphone'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='accounts/24/07/29/home4.png', upload_to='accounts/%y/%m/%d'),
        ),
    ]

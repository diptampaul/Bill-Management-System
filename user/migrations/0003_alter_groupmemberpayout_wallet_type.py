# Generated by Django 4.0.6 on 2022-08-02 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_rename_paytm_number_groupmemberpayout_wallet_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupmemberpayout',
            name='wallet_type',
            field=models.CharField(max_length=2, null=True),
        ),
    ]

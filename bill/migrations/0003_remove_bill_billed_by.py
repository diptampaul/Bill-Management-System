# Generated by Django 4.0.6 on 2022-07-28 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bill', '0002_alter_bill_billed_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='billed_by',
        ),
    ]
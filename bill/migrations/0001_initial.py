# Generated by Django 4.0.6 on 2022-07-28 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('photo', models.FileField(upload_to='bills/')),
                ('bid', models.IntegerField(primary_key=True, serialize=False)),
                ('billed_for', models.CharField(max_length=400)),
                ('billed_by', models.CharField(blank=True, max_length=400, null=True)),
                ('amount', models.FloatField()),
                ('status', models.CharField(max_length=2)),
                ('upvote', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('gid', models.IntegerField()),
                ('mid', models.IntegerField(default=0)),
            ],
        ),
    ]

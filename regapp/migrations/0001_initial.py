# Generated by Django 4.0.4 on 2022-05-23 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentname', models.CharField(max_length=30)),
                ('studentplace', models.CharField(max_length=30)),
            ],
        ),
    ]

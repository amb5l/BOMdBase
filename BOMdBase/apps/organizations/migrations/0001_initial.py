# Generated by Django 3.1.7 on 2021-02-22 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('manufacturer', models.BooleanField(blank=True, null=True)),
                ('supplier', models.BooleanField(blank=True, null=True)),
                ('url', models.URLField(blank=True, max_length=100)),
                ('notes', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
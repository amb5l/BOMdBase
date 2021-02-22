# Generated by Django 3.1.7 on 2021-02-22 20:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('logical_parts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BOM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BOMItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('references', models.TextField(blank=True)),
                ('bom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', related_query_name='item', to='boms.bom')),
                ('logical_part', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bom_items', related_query_name='bom_item', to='logical_parts.logicalpart')),
            ],
        ),
    ]

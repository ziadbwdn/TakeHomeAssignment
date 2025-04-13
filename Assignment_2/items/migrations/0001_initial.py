# Generated by Django 5.2 on 2025-04-13 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=20)),
                ('description', models.TextField(blank=True)),
                ('stock', models.IntegerField(default=0)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

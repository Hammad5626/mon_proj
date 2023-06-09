# Generated by Django 4.2.2 on 2023-07-06 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('is_favorite', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('time', models.DateTimeField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('volume', models.FloatField(blank=True, null=True)),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('opening_price', models.FloatField(blank=True, null=True)),
                ('volume_spent', models.FloatField(blank=True, null=True)),
                ('closing_time', models.DateTimeField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('commision', models.FloatField(blank=True, null=True)),
                ('swap', models.FloatField(blank=True, null=True)),
                ('profit', models.FloatField(blank=True, null=True)),
                ('net_profit', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.usermodel')),
            ],
            options={
                'ordering': ('closing_time',),
            },
        ),
    ]

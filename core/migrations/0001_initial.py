# Generated by Django 4.2.1 on 2023-06-02 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataModel',
            fields=[
                ('opening_time', models.DateTimeField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100)),
                ('volume', models.FloatField(null=True)),
                ('symbol', models.CharField(max_length=100, null=True)),
                ('opening_price', models.FloatField(null=True)),
                ('volumn_spent', models.FloatField(null=True)),
                ('closing_time', models.DateTimeField(null=True)),
                ('price', models.FloatField(null=True)),
                ('profit', models.FloatField(null=True)),
            ],
            options={
                'ordering': ('-opening_time',),
            },
        ),
        migrations.AddConstraint(
            model_name='datamodel',
            constraint=models.UniqueConstraint(fields=('opening_time', 'profit'), name='composite_pk'),
        ),
    ]

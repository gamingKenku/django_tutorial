# Generated by Django 4.1.1 on 2022-10-11 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('release_date', models.DateField()),
            ],
            options={
                'db_table': 'book',
            },
        ),
    ]

# Generated by Django 3.0.7 on 2020-10-19 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_basketlist_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketlist',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]

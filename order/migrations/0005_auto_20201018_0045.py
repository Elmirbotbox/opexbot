# Generated by Django 3.0.7 on 2020-10-17 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20201016_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketlist',
            name='status',
            field=models.IntegerField(choices=[(0, 'Rejected'), (1, 'Waiting Incoming'), (2, 'Accepted (Outgoing)'), (3, 'Being_Delivered(Ready)'), (4, 'Completed')], default=1, verbose_name='status'),
        ),
    ]

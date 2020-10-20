# Generated by Django 3.0.7 on 2020-10-18 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_remove_basketlist_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketlist',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='basketlist',
            name='status',
            field=models.IntegerField(choices=[(0, 'Rejected'), (1, 'Waiting Payment'), (2, 'Waiting Incoming'), (3, 'Accepted (Outgoing)'), (4, 'Being_Delivered(Ready)'), (5, 'Completed')], default=1, verbose_name='status'),
        ),
    ]

# Generated by Django 3.1.1 on 2020-11-26 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'default_permissions': ('add',), 'permissions': (('give_refund', 'Can refund customers'), ('can_hire', 'Can hire employees'))},
        ),
    ]
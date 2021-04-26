# Generated by Django 2.2.19 on 2021-04-18 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officeAttender', '0010_auto_20210418_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='isManagement',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.CharField(blank=True, choices=[('on my way', 'on my way'), ('on my way in five', 'on my way in five'), ('going home', 'going home'), ('stuck in traffic', 'stuck in traffic'), ('at the office', 'at the office'), ('sick at home', 'sick at home'), ('in a meeting', 'in a meeting'), ('in a staff meeting', 'in a staff meeting'), ('in a management meeting', 'in a management meeting'), ('coffee break', 'coffee break'), ('lunch time', 'lunch time'), ('in a parallel workspace', 'in a parallel workspace'), ('working from home', 'working from home')], default=None, max_length=50, null=True),
        ),
    ]

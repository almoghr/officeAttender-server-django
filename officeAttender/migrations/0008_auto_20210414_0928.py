# Generated by Django 2.2.19 on 2021-04-14 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('officeAttender', '0007_auto_20210413_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='workspace',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='officeAttender.WorkSpace'),
        ),
    ]

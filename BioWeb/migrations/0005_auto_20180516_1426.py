# Generated by Django 2.0.3 on 2018-05-16 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BioWeb', '0004_auto_20180516_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update_file',
            name='CDS',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='update_file',
            name='DEFINITION',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='update_file',
            name='LOCUS',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='update_file',
            name='ORIGIN',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='update_file',
            name='translation',
            field=models.TextField(default=''),
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-25 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_timesheet_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='OvertimeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
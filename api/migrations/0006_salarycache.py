# Generated by Django 2.1.3 on 2018-12-04 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20181126_1923'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalaryCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.PositiveSmallIntegerField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Person')),
            ],
        ),
    ]

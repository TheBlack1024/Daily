# Generated by Django 2.2.3 on 2019-08-10 02:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daily', '0004_auto_20190809_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daily.Employees', verbose_name='汇报人'),
        ),
    ]
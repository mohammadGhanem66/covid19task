# Generated by Django 4.1.4 on 2022-12-17 19:03

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('covidtask', '0004_alter_country_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='confirmed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='death',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='recoverd',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='subscription',
            field=models.ManyToManyField(blank=True, db_table='Subscription', null=True, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='subscriptions'),
        ),
    ]
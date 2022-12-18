# Generated by Django 4.1.4 on 2022-12-17 17:36

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('covidtask', '0003_country_subscription_alter_country_confirmed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='subscription',
            field=models.ManyToManyField(db_table='Subscription', related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='subscriptions'),
        ),
    ]
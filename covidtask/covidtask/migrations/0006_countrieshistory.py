# Generated by Django 4.1.4 on 2022-12-18 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covidtask', '0005_alter_country_confirmed_alter_country_death_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountriesHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmed', models.IntegerField(blank=True, null=True)),
                ('death', models.IntegerField(blank=True, null=True)),
                ('recoverd', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='covidtask.country')),
            ],
        ),
    ]
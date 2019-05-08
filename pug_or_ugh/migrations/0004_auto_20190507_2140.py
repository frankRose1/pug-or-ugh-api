# Generated by Django 2.1.7 on 2019-05-08 01:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pug_or_ugh', '0003_auto_20190504_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='gender',
            field=models.CharField(choices=[('f', 'Female'), ('m', 'Male'), ('u', 'Unknown')], max_length=1),
        ),
        migrations.AlterField(
            model_name='dog',
            name='size',
            field=models.CharField(choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large'), ('u', 'Unknown')], max_length=2),
        ),
        migrations.AlterField(
            model_name='userdog',
            name='dog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pug_or_ugh.Dog'),
        ),
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(choices=[('l', 'Like'), ('d', 'Dislike'), ('u', 'Undecided')], max_length=1),
        ),
        migrations.AlterField(
            model_name='userdog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='age',
            field=models.CharField(choices=[('b', 'Baby'), ('y', 'Young'), ('a', 'Adult'), ('s', 'Senior')], max_length=1),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='gender',
            field=models.CharField(choices=[('f', 'Female'), ('m', 'Male')], max_length=1),
        ),
        migrations.AlterField(
            model_name='userpreference',
            name='size',
            field=models.CharField(choices=[('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('xl', 'Extra Large'), ('u', 'Unknown')], max_length=2),
        ),
    ]
# Generated by Django 5.1.3 on 2024-11-15 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='date',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='training_sessions',
        ),
        migrations.CreateModel(
            name='DateTimeTrain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_sessions', models.CharField(default='')),
                ('date', models.DateField(default='', null=True)),
                ('users', models.ManyToManyField(to='app.userprofile')),
            ],
        ),
    ]
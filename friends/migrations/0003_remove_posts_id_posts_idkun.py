# Generated by Django 4.2.3 on 2023-08-23 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0002_posts_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posts',
            name='id',
        ),
        migrations.AddField(
            model_name='posts',
            name='idkun',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
    ]

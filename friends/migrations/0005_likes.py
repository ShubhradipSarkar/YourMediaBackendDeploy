# Generated by Django 4.2.3 on 2023-08-23 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0004_alter_posts_idkun'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.IntegerField()),
                ('liker_id', models.IntegerField()),
            ],
            options={
                'unique_together': {('post_id', 'liker_id')},
            },
        ),
    ]

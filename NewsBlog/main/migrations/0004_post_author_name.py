# Generated by Django 4.0.3 on 2022-04-27 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_post_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author_name',
            field=models.CharField(default='dhruv', max_length=100),
        ),
    ]
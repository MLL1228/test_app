# Generated by Django 2.1.5 on 2019-02-28 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0004_remove_teacher_cls'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='cls',
            field=models.ManyToManyField(to='myblog.Classes'),
        ),
    ]

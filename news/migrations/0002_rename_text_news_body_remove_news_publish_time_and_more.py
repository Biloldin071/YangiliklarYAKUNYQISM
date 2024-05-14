
# Generated by Django 4.2.7 on 2024-02-03 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='news',
            old_name='text',
            new_name='body',
        ),
        migrations.RemoveField(
            model_name='news',
            name='publish_time',
        ),
        migrations.AlterField(
            model_name='news',
            name='status',
            field=models.CharField(choices=[('DR', 'Draft'), ('PB', 'Published')], default='DR', max_length=2),
        ),
    ]

# Generated by Django 3.1 on 2020-08-20 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cmspost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_post', models.CharField(max_length=50)),
                ('matn_post', models.TextField()),
                ('date_post', models.DateTimeField()),
            ],
        ),
    ]
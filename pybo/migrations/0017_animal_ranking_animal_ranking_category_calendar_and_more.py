# Generated by Django 4.2.1 on 2023-05-18 12:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pybo', '0016_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='animal_ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modify_date', models.DateTimeField(blank=True, null=True)),
                ('subject', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('create_date', models.DateTimeField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animal_ranking_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='animal_ranking_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('has_answer', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('month', models.IntegerField()),
                ('year', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('time', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Fullcalender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_title', models.CharField(max_length=200)),
                ('reservation_detail', models.CharField(max_length=200)),
                ('reservation_date', models.DateTimeField()),
                ('reservation_time', models.CharField(max_length=200)),
                ('reservation_idx', models.IntegerField(null=True)),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Fullcalender_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pet2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(null=True, upload_to='photos/%Y/%m/%d/')),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.AddField(
            model_name='calendar',
            name='events',
            field=models.ManyToManyField(to='pybo.event'),
        ),
        migrations.AddField(
            model_name='animal_ranking',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='animal_ranking_category', to='pybo.animal_ranking_category'),
        ),
        migrations.AddField(
            model_name='animal_ranking',
            name='pet',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pet2', to='pybo.pet2'),
        ),
        migrations.AddField(
            model_name='animal_ranking',
            name='voter',
            field=models.ManyToManyField(related_name='voter_animal_question', to=settings.AUTH_USER_MODEL),
        ),
    ]

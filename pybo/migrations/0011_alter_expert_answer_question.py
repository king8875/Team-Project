# Generated by Django 4.1.5 on 2023-03-18 13:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pybo", "0010_expert_answer"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expert_answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="expert_answers",
                to="pybo.expert",
            ),
        ),
    ]

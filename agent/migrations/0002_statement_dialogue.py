# Generated by Django 2.1.2 on 2018-11-05 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='dialogue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dialogue', to='agent.Dialogue'),
        ),
    ]

# Generated by Django 3.2.6 on 2024-02-16 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.CharField(max_length=250)),
                ('round', models.IntegerField()),
                ('number', models.IntegerField()),
                ('question', models.CharField(max_length=2500)),
                ('answer', models.CharField(max_length=2500)),
            ],
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('session_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=250)),
                ('answer', models.CharField(max_length=2500)),
                ('timestamp', models.DateTimeField()),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TriviaNight.sessions')),
            ],
        ),
    ]

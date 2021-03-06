# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-02-22 19:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('insurer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('field_type', models.CharField(choices=[('text', 'text'), ('number', 'number'), ('date', 'date'), ('enum', 'enum')], max_length=20)),
                ('ordering', models.IntegerField(default=1)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('schema', models.TextField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='RiskType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_published', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('insurer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risk_model', to='insurer.Insurer')),
            ],
        ),
        migrations.AddField(
            model_name='risk',
            name='risk_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risks', to='risk_type.RiskType'),
        ),
        migrations.AddField(
            model_name='risk',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fieldtype',
            name='risk_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='field_types', to='risk_type.RiskType'),
        ),
        migrations.AlterUniqueTogether(
            name='risktype',
            unique_together=set([('insurer', 'name')]),
        ),
    ]

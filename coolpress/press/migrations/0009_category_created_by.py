# Generated by Django 3.2.7 on 2022-11-13 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('press', '0008_auto_20221113_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='press.cooluser', null=True),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.5 on 2023-12-28 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_auto_20231227_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='difficulty_level',
            field=models.CharField(choices=[('hieu', 'Hiểu'), ('biet', 'Biết'), ('van_dung_thap', 'Vận dụng thấp'), ('van_dung_cao', 'Vận dụng cao')], default='Hiểu', max_length=20),
        ),
    ]

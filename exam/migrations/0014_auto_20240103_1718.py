# Generated by Django 3.0.5 on 2024-01-03 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0013_examcontent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examcontent',
            name='exam_requirement',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='question',
            name='difficulty_level',
            field=models.CharField(choices=[('biet', 'Biết'), ('hieu', 'Hiểu'), ('van_dung_thap', 'Vận dụng thấp'), ('van_dung_cao', 'Vận dụng cao')], default='biet', max_length=20),
        ),
    ]
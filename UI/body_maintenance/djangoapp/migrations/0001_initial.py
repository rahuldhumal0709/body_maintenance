# Generated by Django 4.2.11 on 2024-04-15 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='bm_date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='bm_person_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('height', models.FloatField(help_text='Height in cm')),
                ('education', models.CharField(max_length=100)),
                ('permanent_address', models.CharField(max_length=255)),
                ('current_address', models.CharField(max_length=255)),
                ('marital_status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='bm_subject_names',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='bm_weight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField(default=0, help_text='Weight in kg')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
        migrations.CreateModel(
            name='bm_total_calories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_calories', models.IntegerField()),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
        migrations.CreateModel(
            name='bm_subject_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('topic', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('efforts', models.DecimalField(decimal_places=2, max_digits=5)),
                ('is_any_que_solved', models.BooleanField(default=False)),
                ('how_many_que', models.IntegerField()),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
                ('subject_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_subject_names')),
            ],
        ),
        migrations.CreateModel(
            name='bm_office',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('work', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('efforts', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
        migrations.CreateModel(
            name='bm_lunch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lunch_menu', models.CharField(max_length=100)),
                ('quantity', models.CharField(max_length=100)),
                ('dish_calories', models.IntegerField()),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
        migrations.CreateModel(
            name='bm_job_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('is_referral', models.BooleanField(default=False)),
                ('referral_person_name', models.CharField(max_length=100, null=True)),
                ('platform_name', models.CharField(max_length=100, null=True)),
                ('for_which_role', models.CharField(max_length=100, null=True)),
                ('resume', models.FileField(default='', upload_to='resume')),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
        migrations.CreateModel(
            name='bm_exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('sets_of_parts', models.JSONField()),
                ('efforts', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
        migrations.CreateModel(
            name='bm_dinner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dinner_menu', models.CharField(max_length=100)),
                ('quantity', models.CharField(max_length=100)),
                ('dish_calories', models.IntegerField()),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
        migrations.CreateModel(
            name='bm_daily_wakeup_sleep_time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wakeup_time', models.TimeField()),
                ('sleep_time', models.TimeField(null=True)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
        migrations.CreateModel(
            name='bm_breakfast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breakfast_meal', models.CharField(max_length=100)),
                ('quantity', models.CharField(max_length=100)),
                ('dish_calories', models.IntegerField()),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
        migrations.CreateModel(
            name='bm_bmi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField(help_text='Height in cm')),
                ('weight', models.FloatField(help_text='Weight in kg')),
                ('bmi', models.FloatField(help_text='BMI in kg/m2')),
                ('result', models.CharField(max_length=100)),
                ('date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_date')),
                ('person_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.bm_person_info')),
            ],
        ),
    ]
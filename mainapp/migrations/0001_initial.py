# Generated by Django 2.0 on 2018-03-17 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('ID', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('mobile_no', models.CharField(max_length=10)),
                ('designation', models.CharField(choices=[('ASSP', 'Assistant Professor'), ('ASOP', 'Associate Professor'), ('PROF', 'Professor'), ('LABT', 'Lab Technician'), ('ACCO', 'Accountant'), ('PROJ', 'Project Officer')], default='ASSP', max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('ID', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('mobile_no', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=30, unique=True)),
                ('authenticated', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='approvalentity',
            name='approval_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Employee'),
        ),
        migrations.AddField(
            model_name='approvalentity',
            name='user_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='approvalentity',
            unique_together={('user_ID', 'approval_ID', 'category')},
        ),
    ]
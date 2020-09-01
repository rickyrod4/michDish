# Generated by Django 3.0.8 on 2020-08-30 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0002_comment_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='rating',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='dish_directory_path'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='categories',
            field=models.ManyToManyField(help_text='Select all categories that apply.', related_name='dishes', to='dish.Category'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='cook_time',
            field=models.IntegerField(help_text='Cook time in minutes.'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='description',
            field=models.TextField(blank=True, help_text='Describe the dish, its history and why you were inspired to make it.'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='ingredients',
            field=models.TextField(help_text='Add each ingredient on a new line.'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='prep_time',
            field=models.IntegerField(help_text='Prep time in minutes.'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='profile_pic',
            field=models.ImageField(blank=True, default='dishes/blank-dish.jpg', null=True, upload_to='dish_directory_path'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='recipe',
            field=models.TextField(help_text='Instructions for how to make the dish.'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, help_text='Tell us about yourself, chef!'),
        ),
    ]
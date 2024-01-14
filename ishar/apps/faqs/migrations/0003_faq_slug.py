# Generated by Django 4.2.9 on 2024-01-14 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faqs', '0002_alter_faq_question_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='faq',
            name='slug',
            field=models.SlugField(default=None, help_text='Short (slug) name for the HTML anchor/URL.', max_length=16, unique=True, verbose_name='(Slug) Name'),
        ),
    ]

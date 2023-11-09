# Generated by Django 4.2.7 on 2023-11-09 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MUDClientCategory',
            fields=[
                ('category_id', models.AutoField(db_column='category_id', help_text='Auto-generated ID number of the MUD client category.', primary_key=True, serialize=False, verbose_name='MUD Client Category ID')),
                ('name', models.SlugField(db_column='name', help_text='Name of the MUD client category.', verbose_name='Category Name')),
                ('is_visible', models.BooleanField(db_column='is_visible', default=True, help_text='Should the MUD client category be visible publicly?', verbose_name='Visible?')),
                ('display_order', models.PositiveIntegerField(db_column='display_order', help_text='What is the numeric display order of the MUD client category?', unique=True, verbose_name='Display Order')),
            ],
            options={
                'verbose_name': 'MUD Client Category',
                'verbose_name_plural': 'MUD Categories',
                'db_table': 'mud_client_categories',
                'ordering': ('display_order',),
                'managed': True,
                'default_related_name': 'mud_client_categories',
            },
        ),
        migrations.CreateModel(
            name='MUDClient',
            fields=[
                ('client_id', models.AutoField(help_text='Auto-generated ID number of the MUD client.', primary_key=True, serialize=False, verbose_name='FAQ ID')),
                ('name', models.SlugField(db_column='name', help_text='Name of the MUD client.', max_length=64, unique=True, verbose_name='Name')),
                ('url', models.URLField(db_column='url', help_text='URL of the MUD client.', verbose_name='URL')),
                ('is_visible', models.BooleanField(db_column='is_visible', default=True, help_text='Should the MUD client be visible publicly?', verbose_name='Visible?')),
                ('display_order', models.PositiveIntegerField(db_column='display_order', help_text='What is the numeric display order of the MUD client?', unique=True, verbose_name='Display Order')),
                ('category', models.ForeignKey(db_column='category_id', help_text='Category of the MUD client.', on_delete=django.db.models.deletion.PROTECT, related_name='clients', related_query_name='client', to='clients.mudclientcategory', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'MUD Client',
                'verbose_name_plural': 'MUD Clients',
                'db_table': 'mud_clients',
                'ordering': ('display_order',),
                'managed': True,
                'default_related_name': 'mud_clients',
            },
        ),
    ]

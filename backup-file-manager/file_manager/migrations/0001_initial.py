# Generated by Django 3.1.1 on 2020-10-01 16:24

from django.db import migrations, models
import extras.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('ip_address', extras.fields.IPAddressField(blank=True, help_text='IPv4 or IPv6 address (with mask)', null=True)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('server_type', models.PositiveSmallIntegerField(choices=[(1, 'System Server'), (2, 'User Server')])),
            ],
            options={
                'verbose_name': 'Upload Server',
                'verbose_name_plural': 'Upload Servers',
                'ordering': ('name', 'slug'),
            },
        ),
    ]
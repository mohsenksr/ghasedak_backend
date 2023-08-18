# Generated by Django 4.0.6 on 2023-08-16 15:17

import apps.account.models.user
from django.conf import settings
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(regex='^(09)[0-9]{9}$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('cc_number', models.CharField(blank=True, max_length=32, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text='designates whether the user can log into this admin site.')),
                ('national_id', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='designates whether this user should be treated as active. unselect this instead of deleting accounts.')),
                ('role', models.CharField(choices=[('CUSTOMER', 'customer'), ('ADMIN', 'admin')], max_length=32)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('credit', models.PositiveBigIntegerField(default=0)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='users', related_query_name='user', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='users', related_query_name='user', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', apps.account.models.user.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('phone', models.CharField(db_index=True, max_length=16, validators=[django.core.validators.RegexValidator(regex='^(09)[0-9]{9}$')])),
                ('email', models.EmailField(blank=True, db_index=True, max_length=254, null=True)),
                ('cc_number', models.CharField(blank=True, max_length=32, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text='designates whether the user can log into this admin site.')),
                ('national_id', models.CharField(blank=True, max_length=20, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='designates whether this user should be treated as active. unselect this instead of deleting accounts.')),
                ('role', models.CharField(choices=[('CUSTOMER', 'customer'), ('ADMIN', 'admin')], max_length=32)),
                ('created_date', models.DateTimeField(blank=True, editable=False)),
                ('modified_date', models.DateTimeField(blank=True, editable=False)),
                ('credit', models.PositiveBigIntegerField(default=0)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical user',
                'verbose_name_plural': 'historical users',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]

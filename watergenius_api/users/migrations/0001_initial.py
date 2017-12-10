# Generated by Django 2.0 on 2017-12-10 16:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_email', models.EmailField(db_index=True, max_length=254, primary_key=True, serialize=False, unique=True)),
                ('user_name', models.CharField(max_length=100)),
                ('user_passwd', models.CharField(max_length=50)),
                ('user_admin', models.BooleanField()),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CentralNode',
            fields=[
                ('node_id', models.AutoField(primary_key=True, serialize=False)),
                ('node_ip', models.GenericIPAddressField()),
            ],
        ),
        migrations.CreateModel(
            name='DayPlan',
            fields=[
                ('dayplan_id', models.AutoField(primary_key=True, serialize=False)),
                ('dayplan_gen_time', models.DateField(auto_now=True)),
                ('dayplan_time', models.DateField()),
                ('dayplan_water_qtd', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EmbededSystem',
            fields=[
                ('esys_id', models.AutoField(primary_key=True, serialize=False)),
                ('esys_state', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='IrrigationTime',
            fields=[
                ('irrigation_time_id', models.AutoField(primary_key=True, serialize=False)),
                ('irrigation_time_date', models.DateField()),
                ('irrigation_time_qtd', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Localization',
            fields=[
                ('local_id', models.AutoField(primary_key=True, serialize=False)),
                ('local_long', models.FloatField()),
                ('local_lat', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PlantType',
            fields=[
                ('plant_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('plant_type_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('prop_id', models.AutoField(primary_key=True, serialize=False)),
                ('prop_name', models.CharField(max_length=50)),
                ('prop_description', models.CharField(max_length=250)),
                ('prop_address', models.CharField(max_length=100)),
                ('prop_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owned_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Read',
            fields=[
                ('read_id', models.AutoField(primary_key=True, serialize=False)),
                ('read_timestamp', models.DateField(auto_now=True)),
                ('read_value', models.IntegerField()),
                ('read_dayplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to_dayplan', to='users.DayPlan')),
            ],
        ),
        migrations.CreateModel(
            name='ReadType',
            fields=[
                ('read_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('read_type_name', models.CharField(max_length=50)),
                ('read_type_units', models.CharField(max_length=3)),
                ('read_type_coef', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_id', models.AutoField(primary_key=True, serialize=False)),
                ('sensor_state', models.IntegerField()),
                ('sensor_timerate', models.IntegerField()),
                ('sensor_depth', models.IntegerField()),
                ('sensor_sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to_subspace', to='users.EmbededSystem')),
            ],
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('sensor_type_id', models.AutoField(primary_key=True, serialize=False)),
                ('sensor_type_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('space_id', models.AutoField(primary_key=True, serialize=False)),
                ('space_name', models.CharField(max_length=50)),
                ('space_description', models.CharField(max_length=150)),
                ('space_irrigation_hour', models.IntegerField()),
                ('space_plant_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_plant_type', to='users.PlantType')),
                ('space_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to_property', to='users.Property')),
            ],
        ),
        migrations.CreateModel(
            name='SubSpace',
            fields=[
                ('sub', models.AutoField(primary_key=True, serialize=False)),
                ('sub_name', models.CharField(max_length=50)),
                ('sub_description', models.CharField(max_length=150)),
                ('sub_space_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to_space', to='users.Space')),
            ],
        ),
        migrations.CreateModel(
            name='TimeRestrition',
            fields=[
                ('time_restrition_id', models.AutoField(primary_key=True, serialize=False)),
                ('time_begin', models.DateTimeField()),
                ('time_duration', models.DurationField()),
                ('time_restrition_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to_spaceid', to='users.Space')),
            ],
        ),
        migrations.CreateModel(
            name='UserHasProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prop_has_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prop', to='users.Property')),
                ('user_has_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Warnings',
            fields=[
                ('warning_id', models.AutoField(primary_key=True, serialize=False)),
                ('warning_description', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_type', to='users.SensorType'),
        ),
        migrations.AddField(
            model_name='readtype',
            name='read_type_sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_belongs_to', to='users.Sensor'),
        ),
        migrations.AddField(
            model_name='read',
            name='read_sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to_sensor', to='users.Sensor'),
        ),
        migrations.AddField(
            model_name='read',
            name='read_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='has_readtype', to='users.ReadType'),
        ),
        migrations.AddField(
            model_name='irrigationtime',
            name='irrigation_time_sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refers_to', to='users.SubSpace'),
        ),
        migrations.AddField(
            model_name='embededsystem',
            name='esys_local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_localization', to='users.Localization'),
        ),
        migrations.AddField(
            model_name='embededsystem',
            name='esys_sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to_sub', to='users.SubSpace'),
        ),
        migrations.AddField(
            model_name='dayplan',
            name='dayplan_sub',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='belongs_to_subspa', to='users.SubSpace'),
        ),
        migrations.AddField(
            model_name='centralnode',
            name='node_local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='is_in_local', to='users.Localization'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_props',
            field=models.ManyToManyField(through='users.UserHasProperty', to='users.Property'),
        ),
    ]

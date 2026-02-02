# Generated migration for MyntraRegistration model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor', '0002_sponsors_order_sponsors_sponsor_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyntraRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anwesha_user_id', models.CharField(blank=True, db_index=True, max_length=10, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('last_synced', models.DateTimeField(auto_now=True)),
                ('raw_data', models.JSONField(blank=True, default=dict)),
            ],
            options={
                'verbose_name': 'Myntra Registration',
                'verbose_name_plural': 'Myntra Registrations',
            },
        ),
        migrations.RunSQL(
            "ALTER TABLE sponsor_myntraregistration ADD CONSTRAINT sponsor_myntraregistration_anwesha_user_id_fk FOREIGN KEY (anwesha_user_id) REFERENCES user_user(anwesha_id)",
            "ALTER TABLE sponsor_myntraregistration DROP FOREIGN KEY sponsor_myntraregistration_anwesha_user_id_fk",
        ),
    ]

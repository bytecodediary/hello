from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_appointment_verification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="user_type",
            field=models.CharField(choices=[("customer", "customer"), ("agent", "agent"), ("proplord", "property_lord"), ("landlord", "landlord")], default="customer", max_length=20),
        ),
        migrations.AddField(
            model_name="customuser",
            name="provider_status",
            field=models.CharField(choices=[("none", "None"), ("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="none", max_length=20),
        ),
        migrations.AddField(
            model_name="customuser",
            name="requested_provider_type",
            field=models.CharField(blank=True, choices=[("customer", "customer"), ("agent", "agent"), ("proplord", "property_lord"), ("landlord", "landlord")], max_length=20),
        ),
        migrations.RunSQL(
            "UPDATE user_customuser SET provider_status = 'approved' WHERE user_type IN ('agent', 'proplord', 'landlord')",
            migrations.RunSQL.noop,
        ),
    ]

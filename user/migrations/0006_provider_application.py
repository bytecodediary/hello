from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_align_legacy_fields"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProviderApplication",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("requested_type", models.CharField(choices=[("agent", "Agent"), ("landlord", "Landlord")], max_length=20)),
                ("organization_name", models.CharField(blank=True, max_length=120)),
                ("phone_number", phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ("message", models.TextField(blank=True, max_length=2000)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("approved", "Approved"), ("rejected", "Rejected")], default="pending", max_length=20)),
                ("review_notes", models.TextField(blank=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("reviewed_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="reviewed_provider_applications", to=settings.AUTH_USER_MODEL)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="provider_applications", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="providerapplication",
            index=models.Index(fields=["status", "created_at"], name="user_provid_status_9fe4bc_idx"),
        ),
        migrations.AddIndex(
            model_name="providerapplication",
            index=models.Index(fields=["user", "status"], name="user_provid_user_id_6f990e_idx"),
        ),
    ]

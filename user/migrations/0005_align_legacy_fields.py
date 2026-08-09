import uuid

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0004_provider_state"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tenant",
            name="lease_agreement",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="tenant",
            name="name",
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="tenant_profile", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name="tenant",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name="tenant",
            name="rent_status",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="tenant_profiles", to="payment.payment"),
        ),
        migrations.AlterField(
            model_name="verification",
            name="token",
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

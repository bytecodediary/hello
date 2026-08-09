from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("listing", "0004_alter_propertyfeature_property"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="property",
            name="area_sqm",
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name="property",
            name="bathrooms",
            field=models.DecimalField(decimal_places=1, default=0, max_digits=4),
        ),
        migrations.AddField(
            model_name="property",
            name="bedrooms",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="property",
            name="county",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="property",
            name="created_by",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="created_listings", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="property",
            name="currency",
            field=models.CharField(default="KES", max_length=3),
        ),
        migrations.AddField(
            model_name="property",
            name="is_featured",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="property",
            name="listing_type",
            field=models.CharField(choices=[("sale", "For sale"), ("rent", "For rent")], default="sale", max_length=10),
        ),
        migrations.AddField(
            model_name="property",
            name="moderated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="property",
            name="moderated_by",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="moderated_listings", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="property",
            name="moderation_status",
            field=models.CharField(choices=[("draft", "Draft"), ("pending_review", "Pending review"), ("published", "Published"), ("rejected", "Rejected"), ("archived", "Archived")], default="published", max_length=20),
        ),
        migrations.AddField(
            model_name="property",
            name="neighborhood",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="property",
            name="property_type",
            field=models.CharField(choices=[("house", "House"), ("apartment", "Apartment"), ("townhouse", "Townhouse"), ("land", "Land"), ("commercial", "Commercial"), ("other", "Other")], default="house", max_length=20),
        ),
        migrations.AlterField(
            model_name="property",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
        migrations.AddField(
            model_name="image",
            name="display_order",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="image",
            name="is_cover",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="image",
            name="image",
            field=models.ImageField(upload_to="properties/%Y/%m/"),
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("property", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorited_by", to="listing.property")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
                "constraints": [models.UniqueConstraint(fields=("user", "property"), name="unique_user_property_favorite")],
            },
        ),
        migrations.CreateModel(
            name="Inquiry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("inquiry_type", models.CharField(choices=[("inquiry", "Inquiry"), ("viewing", "Viewing request")], default="inquiry", max_length=20)),
                ("message", models.TextField(max_length=2000)),
                ("preferred_start", models.DateTimeField(blank=True, null=True)),
                ("preferred_end", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(choices=[("new", "New"), ("contacted", "Contacted"), ("scheduled", "Scheduled"), ("completed", "Completed"), ("declined", "Declined"), ("closed", "Closed")], default="new", max_length=20)),
                ("provider_response", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("property", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="inquiries", to="listing.property")),
                ("seeker", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="property_inquiries", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="property",
            index=models.Index(fields=["moderation_status", "listing_type"], name="listing_pro_moderat_0c57d5_idx"),
        ),
        migrations.AddIndex(
            model_name="property",
            index=models.Index(fields=["city", "county"], name="listing_pro_city_5d4b4a_idx"),
        ),
        migrations.AddIndex(
            model_name="property",
            index=models.Index(fields=["price"], name="listing_pro_price_73c7e8_idx"),
        ),
        migrations.AddIndex(
            model_name="property",
            index=models.Index(fields=["created_by"], name="listing_pro_created_4b6f77_idx"),
        ),
    ]

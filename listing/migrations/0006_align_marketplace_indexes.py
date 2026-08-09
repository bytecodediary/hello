from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("listing", "0005_marketplace_foundation"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="property",
            new_name="listing_pro_moderat_a339c8_idx",
            old_name="listing_pro_moderat_0c57d5_idx",
        ),
        migrations.RenameIndex(
            model_name="property",
            new_name="listing_pro_city_783349_idx",
            old_name="listing_pro_city_5d4b4a_idx",
        ),
        migrations.RenameIndex(
            model_name="property",
            new_name="listing_pro_price_9c797b_idx",
            old_name="listing_pro_price_73c7e8_idx",
        ),
        migrations.RenameIndex(
            model_name="property",
            new_name="listing_pro_created_1c5843_idx",
            old_name="listing_pro_created_4b6f77_idx",
        ),
        migrations.AddIndex(
            model_name="inquiry",
            index=models.Index(fields=["property", "status"], name="listing_inq_propert_22a3ae_idx"),
        ),
        migrations.AddIndex(
            model_name="inquiry",
            index=models.Index(fields=["seeker", "status"], name="listing_inq_seeker__a4e45c_idx"),
        ),
    ]

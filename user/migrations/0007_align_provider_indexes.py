from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0006_provider_application"),
    ]

    operations = [
        migrations.RenameIndex(
            model_name="providerapplication",
            new_name="user_provid_status_a63683_idx",
            old_name="user_provid_status_9fe4bc_idx",
        ),
        migrations.RenameIndex(
            model_name="providerapplication",
            new_name="user_provid_user_id_48abc3_idx",
            old_name="user_provid_user_id_6f990e_idx",
        ),
    ]

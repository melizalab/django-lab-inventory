# Generated by Django 4.1.5 on 2023-07-20 17:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0005_rename_ptao_account_alter_account_options_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="ptao",
            new_name="account",
        ),
    ]

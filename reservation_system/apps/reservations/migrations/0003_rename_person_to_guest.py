from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reservations", "0002_reservation_price"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Person",
            new_name="Guest",
        ),
        migrations.AlterField(
            model_name="reservation",
            name="guests",
            field=models.ManyToManyField(related_name="reservations", to="reservations.guest"),
        ),
    ]

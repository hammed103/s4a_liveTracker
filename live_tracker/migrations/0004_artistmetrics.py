# Generated by Django 4.2.2 on 2023-06-25 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("live_tracker", "0003_remove_artist_genre_alter_artist_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtistMetrics",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("artist_name", models.CharField(max_length=100)),
                ("artist_id", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("listeners", models.IntegerField()),
                ("streams", models.IntegerField()),
                ("streams_per_listener", models.FloatField()),
                ("saves", models.IntegerField()),
                ("playlist_adds", models.IntegerField()),
                ("followers", models.IntegerField()),
                ("total_active_audience", models.IntegerField()),
                ("super_listeners", models.IntegerField()),
                ("moderate_listeners", models.IntegerField()),
                ("light_listeners", models.IntegerField()),
            ],
        ),
    ]

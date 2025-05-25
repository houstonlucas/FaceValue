from django.db import migrations, models
import django.utils.text


def populate_slugs(apps, schema_editor):
    Puzzle = apps.get_model('facevalue', 'Puzzle')
    for p in Puzzle.objects.all():
        if not p.slug:
            p.slug = django.utils.text.slugify(p.name)
            p.save()


class Migration(migrations.Migration):
    dependencies = [
        ('facevalue', '0003_tag_comment_parent_comment_updated_at_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='puzzle',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]

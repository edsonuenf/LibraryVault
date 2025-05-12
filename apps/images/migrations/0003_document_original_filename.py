from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('images', '0002_image_file_460'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='original_filename',
            field=models.CharField(max_length=255, blank=True, verbose_name='Nome original do arquivo'),
        ),
    ]

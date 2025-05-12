from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('images', '0003_document_original_filename'),
    ]
    operations = [
        migrations.AddField(
            model_name='audio',
            name='original_filename',
            field=models.CharField(max_length=255, blank=True, verbose_name='Nome original do arquivo'),
        ),
        migrations.AddField(
            model_name='video',
            name='original_filename',
            field=models.CharField(max_length=255, blank=True, verbose_name='Nome original do arquivo'),
        ),
        migrations.AddField(
            model_name='image',
            name='original_filename',
            field=models.CharField(max_length=255, blank=True, verbose_name='Nome original do arquivo'),
        ),
    ]

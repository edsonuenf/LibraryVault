from django.db import models

class DatabaseConfig(models.Model):
    DB_CHOICES = [
        ('sqlite', 'SQLite'),
        ('mysql', 'MySQL'),
        ('postgres', 'PostgreSQL'),
        ('mongodb', 'MongoDB'),
    ]
    db_engine = models.CharField(max_length=20, choices=DB_CHOICES, default='sqlite')
    db_name = models.CharField(max_length=100, blank=True)
    db_user = models.CharField(max_length=100, blank=True)
    db_password = models.CharField(max_length=100, blank=True)
    db_host = models.CharField(max_length=100, blank=True)
    db_port = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.get_db_engine_display()} ({self.db_name})"

from django.db import models

class AuditableModel(models.Model):
    """
    Abstract base model that includes created.
    """
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

from django.db import models
import random

class Certificate(models.Model):
    certificate_id = models.CharField(max_length=12, primary_key=True, unique=True, editable=False)
    recipient_name = models.CharField(max_length=100)
    course_name = models.CharField(max_length=100)
    completion_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            self.certificate_id = self.generate_certificate_id()
        super(Certificate, self).save(*args, **kwargs)

    def generate_certificate_id(self):
        # Generate a random 12-digit certificate ID
        return str(random.randint(100000000000, 999999999999))

    def __str__(self):
        return f"Certificate {self.certificate_id} - {self.recipient_name}"

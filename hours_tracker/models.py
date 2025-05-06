from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class Hours(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return f"Hours for {self.start_time.date()}"
    
    def clean(self):

        super().clean()
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("End time cannot be before start time")

class Breaks(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return f"Breaks for {self.start_time.date()}"

    def clean(self):

        super().clean()
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("End time cannot be before start time")
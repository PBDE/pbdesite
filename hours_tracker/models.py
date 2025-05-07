from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class BaseHours(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True)

    class Meta:
        abstract = True
        ordering = ["-start_time"]
    
    def clean(self):
        super().clean()
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError("End time cannot be before start time")
            
class TargetTime(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    target_time = models.DurationField()

    def __str__(self):
        return f"Target time of length {self.target_time}"
            
class ActiveHours(BaseHours):

    target_time = models.ForeignKey(TargetTime, on_delete=models.PROTECT) # need to consider on delete

    def __str__(self):
        return f"Hours for {self.start_time.date()}"

class Breaks(BaseHours):

    def __str__(self):
        return f"Breaks for {self.start_time.date()}"

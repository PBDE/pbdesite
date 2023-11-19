from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

WORD_MAX_LENGTH = 64

class KnownLanguageNoun(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    known_language_noun = models.CharField(max_length=WORD_MAX_LENGTH)
    
    class Meta:
        abstract = True
        ordering = ["known_language_noun"]

    def __str__(self):
        return f"{self.known_language_noun}"
    
    
class TargetLanguageNoun(models.Model):

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    target_language_noun = models.CharField(max_length=WORD_MAX_LENGTH)
    last_test = models.DateField(auto_now=True)
    number_of_tests = models.PositiveIntegerField(default=0)
    correct_tests = models.PositiveIntegerField(default=0)
    percentage_correct = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)])

    class Meta:
        abstract = True
        ordering = ["target_language_noun"]
    

class EnglishNoun(KnownLanguageNoun):
    
    ARTICLES = [
        ("The", "The")
        ]
    article = models.CharField(max_length=3, default="The")


class GermanNoun(TargetLanguageNoun):
    
    ARTICLES = [
        ("Der", "Der"),
        ("Die", "Die"),
        ("Das", "Das")
    ]
    article = models.CharField(max_length=3, choices=ARTICLES)
    translations = models.ManyToManyField(EnglishNoun)

    def __str__(self):
        return f"{self.article} {self.target_language_noun}"
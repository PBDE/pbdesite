from django import forms
from django.core.exceptions import ValidationError

import re

GERMAN_ARTICLES=[
    ("Der", "Der"),
    ("Die", "Die"),
    ("Das", "Das")
    ]

ENGLISH_ARTICLE=[
    ("The", "The")
]

TEXT_FIELD_WIDGETS = forms.TextInput(attrs={'autocomplete': 'off'})


class KnownNounField(forms.CharField):

    def validate(self, value):
        super().validate(value)
        if not re.search(r"[a-z]+", value):
            raise ValidationError("Only valid alphabet values allowed")


class TargetNounField(forms.CharField):

    def validate(self, value):
        super().validate(value)
        if not re.search(r"[a-z]+", value):
            raise ValidationError("Only valid alphabet values allowed")


class NewNounForm(forms.Form):

    WORD_MAX_LENGTH = 64

    target_article = forms.ChoiceField(label="German article", choices=GERMAN_ARTICLES)
    target_noun = TargetNounField(label="German noun", widget=TEXT_FIELD_WIDGETS, max_length=WORD_MAX_LENGTH) 
    known_article = forms.ChoiceField(label="English article", choices=ENGLISH_ARTICLE)
    known_noun = KnownNounField(label="English translation", widget=TEXT_FIELD_WIDGETS, max_length=WORD_MAX_LENGTH)


class TranslateNoun(forms.Form):

    translation_to = forms.CharField(widget=forms.HiddenInput())
    question_article = forms.CharField(widget=forms.HiddenInput())
    question_noun = forms.CharField(widget=forms.HiddenInput())


class TranslateToTarget(TranslateNoun):

    response_article = forms.ChoiceField(
        label="Article", 
        choices=GERMAN_ARTICLES
        )
    response_noun = forms.CharField(
        label="German translation", 
        required=False, 
        widget=TEXT_FIELD_WIDGETS
        )


class TranslateToKnown(TranslateNoun):

    response_article = forms.ChoiceField(choices=ENGLISH_ARTICLE)
    response_noun = forms.CharField(
        label="English translation", 
        required=False, 
        widget=TEXT_FIELD_WIDGETS
        )

from django.shortcuts import render
from .models import GermanNoun
from django.contrib.auth.models import User
from .language_forms import NewNounForm, TranslateToKnown, TranslateToTarget
from .language_queries import add_noun_to_db, select_noun_to_test, check_user_answer, update_answer_stats, create_test_response_dict

INDEX_TEMPLATE = "vocab_trainer/index.html"
ADD_TEMPLATE = "vocab_trainer/add.html"
TEST_TEMPLATE = "vocab_trainer/test.html"
TRANSLATIONS_TEMPLATE = "vocab_trainer/translations.html"

def index(request):
    return render(request, INDEX_TEMPLATE)


def add(request):
    user = request.user
    if request.method == "POST" and user.is_authenticated:
        new_noun_form = NewNounForm(request.POST)

        if new_noun_form.is_valid():
            _, message = add_noun_to_db(new_noun_form, user)
            return render(request, ADD_TEMPLATE, {
                "form": NewNounForm(),
                "message": message
            })
        else:
            return render(request, ADD_TEMPLATE, {
                "form": new_noun_form
            })
    return render(request, ADD_TEMPLATE, {
        "form": NewNounForm()
    })


def test(request):

    user = request.user

    if not user.is_authenticated:
        user = User.objects.get(username="GuestUser")

    if request.method == "POST":

        if request.POST["translation_to"] == "to_known":
            to_known = True
            answer_form = TranslateToKnown(request.POST)

        elif request.POST["translation_to"] == "to_target":
            to_known = False
            answer_form = TranslateToTarget(request.POST)

        if answer_form.is_valid():
            translations, user_answer_correct = check_user_answer(answer_form, user)

            if not user.username == "GuestUser":
                update_answer_stats(answer_form,
                                    user_answer_correct,
                                    to_known, user)

            if not user_answer_correct:
                return render(
                    request, 
                    TEST_TEMPLATE, 
                    create_test_response_dict(answer_form, translations, to_known, valid_submission=True)
                )
        else:
            return render(
                request, 
                TEST_TEMPLATE,
                create_test_response_dict(answer_form, translations, to_known, valid_submission=False)
            )

    return render(request, TEST_TEMPLATE, select_noun_to_test(user))


def translations_table(request):

    if request.user.is_authenticated:
        german_nouns = GermanNoun.objects.filter(user=request.user).values()
        return render(request, TRANSLATIONS_TEMPLATE, {
            "nouns": german_nouns
        })
    else:
        return render(request, TRANSLATIONS_TEMPLATE)


def reference_tables(request):
    ...

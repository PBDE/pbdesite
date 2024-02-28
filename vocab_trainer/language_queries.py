from random import choice, randint
from .models import GermanNoun, EnglishNoun
from .language_forms import TranslateToTarget, TranslateToKnown

def add_noun_to_db(form, user):

    '''
    Add the user's input vocabulary to the database.

    :param form: The form object containing the user's input
    :type form: form
    :param user: The user object identifing the user
    :type user: user
    :return: A tuple containing a status message and a message for the user
    '''

    ALREADY_PRESENT_MESSAGE = "Both the German noun and its English translation are already present"
    SUCCESSFULLY_ADDED_MESSAGE_START = "Successfully added "

    form_article = form.cleaned_data["target_article"]
    form_target_noun = form.cleaned_data["target_noun"].title().strip()
    form_known_noun = form.cleaned_data["known_noun"].title().strip()

    target_noun_already_exists = (GermanNoun.objects
                                  .filter(target_language_noun=form_target_noun)
                                  .filter(article=form_article)
                                  .filter(user=user)
                                  .exists())
    known_noun_already_exists = (EnglishNoun.objects
                                 .filter(known_language_noun=form_known_noun)
                                 .filter(user=user)
                                 .exists())
    
    message = None

    if target_noun_already_exists and known_noun_already_exists:
        status = "Both present"
        message = ALREADY_PRESENT_MESSAGE

    if target_noun_already_exists and not known_noun_already_exists:
        status = "Target present. Known not present"
        new_known_noun = EnglishNoun(known_language_noun=form_known_noun)
        new_known_noun.user = user
        new_known_noun.save()
        (GermanNoun.objects
         .filter(target_language_noun=form_target_noun)
         .filter(article=form_article)
         .first()
         .translations
         .add(new_known_noun))

    if not target_noun_already_exists and known_noun_already_exists:
        status = "Target not present. Known present"
        known_noun_from_db = EnglishNoun.objects.filter(known_language_noun=form_known_noun).first()
        new_target_noun = GermanNoun(
            article=form_article,
            target_language_noun=form_target_noun, 
            )
        new_target_noun.user = user
        new_target_noun.save()
        new_target_noun.translations.add(known_noun_from_db)

    if not target_noun_already_exists and not known_noun_already_exists:
        status = "Neither present"
        new_known_noun = EnglishNoun(known_language_noun=form_known_noun)
        new_known_noun.user = user
        new_known_noun.save()
        new_target_noun = GermanNoun(
            article=form_article, 
            target_language_noun=form_target_noun, 
            )
        new_target_noun.user = user
        new_target_noun.save()
        new_target_noun.translations.add(new_known_noun)

    if message is None:
        message=SUCCESSFULLY_ADDED_MESSAGE_START + f"{form_article} {form_target_noun}/{form_known_noun}"

    return status, message


def select_noun_to_test(user):

    '''
    Select one of the user's words from the database for the vocabulary test.

    :param user: The user object identifing the user
    :type user: user
    :return: A dictionary containing information about the word to be tested
    '''

    # MIN_ACCURACY_PERCENTAGE = 10
    # MAX_ACCURACY_PERCENTAGE = 91
    # ACCURACY_INCREMENT = 10

    is_translation_to_known = choice([True, False])

    # for percentage_correct_cut_off in range(
    #     MIN_ACCURACY_PERCENTAGE, 
    #     MAX_ACCURACY_PERCENTAGE, 
    #     ACCURACY_INCREMENT):

    #     test_group = (GermanNoun.objects
    #                     .filter(user=user)
    #                     .filter(percentage_correct__lte=percentage_correct_cut_off))

    #     if len(test_group) > 0:
    #         break

    # if len(test_group) == 0:
        # print("Selecting by date")

    test_group = (GermanNoun.objects
                .filter(user=user)
                .all()
                .order_by("percentage_correct", "last_test")[0:10])
    
    if len(test_group) == 0:
        return {"no_vocabulary": True, "response_message": "Add vocabulary before testing"}

    random_index = randint(0, len(test_group)-1)
    test_single = test_group[random_index]
    
    if is_translation_to_known:
        test_article = test_single.article
        target_test_noun = test_single.target_language_noun
        test_dict = {
            "question_article": test_article,
            "question_noun": target_test_noun, 
            "answer_form": TranslateToKnown(initial={
                "translation_to": "to_known",
                "question_article": test_article, 
                "question_noun": target_test_noun})
            }
    else:
        test_single =  test_single.translations.first()
        test_article = test_single.article
        known_test_noun = test_single.known_language_noun
        test_dict = {
            "question_article": test_article,
            "question_noun": known_test_noun,
            "answer_form": TranslateToTarget(initial={
                "translation_to": "to_target",
                "question_article": test_article,
                "question_noun": known_test_noun})
            }
        
    if user.username == "GuestUser":
        test_dict["guest_user"] = True

    return {"is_translation_to_known": is_translation_to_known, "add_check_answer_button": True} | test_dict


def get_translation(is_translation_to_known, translate_word, translate_article, user):

    '''
    Get the translation of a word from the database.

    :param is_translation_to_known: Bool indicating whether the translation is to the user's known language
    :type is_translation_to_known: bool
    :param translate_word: The word to be translated
    :type translate_word: string
    :param translate_article: The article associated with the word to be translated
    :type translate_article: string
    :param user: The user object identifying the user
    :type user: user
    :return: A list of the user's translations for the tested word 
    '''

    if is_translation_to_known:
        tested_word_from_db = (GermanNoun.objects
                               .filter(user=user)
                               .filter(target_language_noun=translate_word)
                               .filter(article=translate_article)
                               .first())
        translations = [(translation.article, translation.known_language_noun) for translation in tested_word_from_db.translations.all()]
    else:
        tested_word_from_db = (EnglishNoun.objects
                               .filter(user=user)
                               .filter(known_language_noun=translate_word)
                               .first())
        translations_query_set = (GermanNoun.objects
                                  .filter(user=user)
                                  .filter(translations=tested_word_from_db))
        translations = [(translation.article, translation.target_language_noun) for translation in translations_query_set]

    return translations


def check_user_answer(answer_form, user):

    '''
    Check if the user's answer is correct.

    :param answer_form: The form object containing the user's answer
    :type answer_form: form
    :param user: The user object identifying the user
    :type user: user
    :return: A tuple containing a list of translations and a bool indicating whether the user is correct
    '''

    is_translation_to_known = True if answer_form.cleaned_data["translation_to"] == "to_known" else False

    answered_article = answer_form.cleaned_data["response_article"].title()
    answered_word = answer_form.cleaned_data["response_noun"].title()
    tested_article = answer_form.cleaned_data["question_article"].title()
    tested_word = answer_form.cleaned_data["question_noun"].title()
    translations = get_translation(is_translation_to_known, tested_word, tested_article, user)

    if (answered_article, answered_word) in translations:
        user_answer_correct = True
    else:
        user_answer_correct = False

    return translations, user_answer_correct


def update_answer_stats(answer_form, answer_correct, to_known, user):

    '''
    Update the database with the stats regarding the tested word.

    :param answer_form: The answer form containing the user's response
    :type answer_form: form
    :param answer_correct: Bool indicating whether the user translated the word correctly
    :type answer_correct: bool
    :param to_known: Bool indicating whether the translation was to the user's known language
    :type to_known: bool
    :param user: The user object identifying the user
    :type user: user
    :return: None
    '''

    if not to_known:
        if answer_correct:
            answered_article = answer_form.cleaned_data["response_article"]
            answered_word = answer_form.cleaned_data["response_noun"].title()
            tested_word_from_db = (GermanNoun.objects
                                   .filter(user=user)
                                   .filter(target_language_noun=answered_word)
                                   .filter(article=answered_article).first())
        else:
            tested_word = answer_form.cleaned_data["question_noun"].title()    
            known_language_translation = (EnglishNoun.objects
                                          .filter(user=user)
                                          .filter(known_language_noun=tested_word)
                                          .first())
            translation_query_set = (GermanNoun.objects
                                     .filter(user=user)
                                     .filter(translations=known_language_translation))
            tested_word_article_noun = [(translation.article, translation.target_language_noun) for translation in translation_query_set][0]
            tested_word_from_db = (GermanNoun.objects
                                   .filter(user=user)
                                   .filter(target_language_noun=tested_word_article_noun[1])
                                   .filter(article=tested_word_article_noun[0])
                                   .first())
    else:
        tested_article = answer_form.cleaned_data["question_article"]
        tested_word = answer_form.cleaned_data["question_noun"]
        tested_word_from_db = (GermanNoun.objects
                               .filter(user=user)
                               .filter(target_language_noun=tested_word)
                               .filter(article=tested_article)
                               .first())

    number_of_tests = tested_word_from_db.number_of_tests
    number_of_tests += 1
    correct_tests = tested_word_from_db.correct_tests

    if answer_correct:
        correct_tests += 1

    percentage_correct = int(round(correct_tests/number_of_tests * 100))
    tested_word_from_db.number_of_tests = number_of_tests
    tested_word_from_db.correct_tests = correct_tests
    tested_word_from_db.percentage_correct = percentage_correct
    tested_word_from_db.save()


def create_test_response_dict(answer_form, translations, to_known, valid_submission):

    '''
    Create a dictionary containing information regarding the user's response to the test.

    :param answer_form: The answer form containing the user's response
    :type answer_form: form
    :param translations: A list of correct translations
    :type translations: lsit
    :param to_known: Bool indicating whether the translation was to the user's known language
    :type to_known: bool
    :param valid_submission: Bool indicating whether the user's submission was valid
    :type valid_submission: bool
    :return: Dictionary containing information about the user's response to the test
    '''

    INVALID_SUBMISSION_MESSAGE = "Please provide a valid submission"
    INCORRECT_MESSAGE_START = "Incorrect. The correct answer is "
    
    if valid_submission:
        response_message = INCORRECT_MESSAGE_START + f"{translations[0][0]} {translations[0][1]}"
    else:
        response_message = INVALID_SUBMISSION_MESSAGE

    return answer_form.cleaned_data | {
        "to native": to_known,
        "answer_form": answer_form,
        "response_message": response_message,
        "add_check_answer_button": not valid_submission
    }

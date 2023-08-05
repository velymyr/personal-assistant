import json

# Словник перекладів зберігається у форматі JSON
translations = {
    'en': {
        'greeting': 'Hello, {name}!',
        'apple': {
            'one': 'One apple',
            'many': 'Many apples'
        },
    },
    'es': {
        'greeting': '¡Hola, {name}!',
        'apple': {
            'one': 'Una manzana',
            'many': 'Muchas manzanas'
        },
    }
}

# Вибір мови користувача (на прикладі англійської та іспанської)
language = 'en'
# language = 'es'

# Функція для отримання перекладу


def _(key, *args, **kwargs):
    if language in translations and key in translations[language]:
        translation = translations[language][key]
        if isinstance(translation, dict):
            count = kwargs.get('count', 1)
            return translation['many'] if count != 1 else translation['one']
        else:
            return translation.format(*args, **kwargs)
    return key


# Ваші рядки для перекладу
print(_('greeting', name='Alice'))
print(_('apple', count=3))

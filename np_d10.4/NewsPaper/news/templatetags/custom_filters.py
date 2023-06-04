from django import template

register = template.Library()

# @register.filter(name='dateField')
# def censor(val, arg):
#     bannedList = ['идиот', 'придурок', 'черт', 'козел']
#     text = val
#     result = ''


@register.filter(name='censor')
def censor(val, arg):
    bannedList = ['идиот', 'придурок', 'черт', 'козел']
    text = val
    result = ''

    for word in bannedList:
        data = text.lower().replace(word, arg * len(word))
        text = data

    for i in range(len(val)):
        if val[i] != text[i]:
            result += text[i].upper()
        else:
            result += text[i]

    return result

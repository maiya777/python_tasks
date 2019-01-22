alphabet = "abcdefghijklmnopqrstuvwxyz"

def is_pangramm(phrase):
    for ch in alphabet:
        if ch not in phrase.lower():
            return False
    else:
        return True


def is_pangramm2(phrase):
    return all([ch in phrase.lower() for ch in alphabet])

# print(is_pangramm2('Brick quiz whangs jumpy veldt fox!'))
# print(is_pangramm2("Sphinx of black quartz judge my vow!"))
# print(is_pangramm2("hello, world!"))

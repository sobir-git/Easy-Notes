def encode(s, key):
    mod = len(key)
    return ''.join(chr(ord(i) + key[pos % mod]) for pos, i in enumerate(s))


def decode(s, key):
    return encode(s, [-i for i in key])


def encrypt_file(filename, password):
    key = [ord(i) for i in password]
    with open(filename, 'r', encoding='utf-8') as f:
        text = encode(f.read(), key)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


def decrypt_file(filename, password):
    key = [ord(i) for i in password]
    with open(filename, 'r', encoding='utf-8') as f:
        text = decode(f.read(), key)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)


def is_encrypted(filename, *keywords):
    '''Check if the file contains all keywords in it
    '''
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not keywords:
                return False

            found_words = []
            for word in keywords:
                if word in line:
                    found_words.append(word)

            for word in found_words:
                keywords.remove(word)

    return True


# print(is_encrypted("old_notes.json", "date_created", "date_modified"))
# encrypt_file('old_notes.json', '123sobir')
# decrypt_file('old_notes.json', '123sobir')

def loop_size(pub_key_value):
    value = 1

    ii = 0
    while value != pub_key_value:
        value *= 7
        value %= 20201227
        ii += 1
    return ii

def transform(subject, n):
    val = 1
    for _ in range(n):
        val *= subject
        val %= 20201227
    return val


card_pubkey = 3469259
door_pubkey = 13170438


print(transform(card_pubkey, loop_size(door_pubkey)))
from hashids import Hashids
hashids = Hashids("secretsaltysaltines")

def encode_oracle(number):
    return hashids.encode(number)

before_first_shuffle = 'abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890'
after_first_shuffle = ''
for i in range(44):
    # First letter is output after shuffling the alphabet once,
    # so by requesting the first 43 letters we obtain the alphabet
    # after it has been shuffled once.
    after_first_shuffle += encode_oracle(i)[0]

# We expect the alphabet to be 43 characters long, and wrap
# on character 44.
if encode_oracle(44)[0] != after_first_shuffle[0]:
    raise RuntimeError("The alphabet length is different than expected.")

salt = ''
for idx in range(0, 43):
    char = after_first_shuffle[-1 - idx]
    original_pos = before_first_shuffle.index(char)
    new_pos = 47 - idx
    print(f"{char}: {original_pos} -> {new_pos}")
    print(f"2 x salt[{idx}] = {original_pos} mod {new_pos}")

    request = (42 - idx) * 44 + 43
    result = encode_oracle(request)
    print(f"{request} -> {result}")
    char = result[1]
    original_pos = after_first_shuffle.index(char)
    new_pos = 43 - idx
    lottery = result[0]
    print(f"2 x salt[{idx}] = {original_pos} mod {new_pos}")

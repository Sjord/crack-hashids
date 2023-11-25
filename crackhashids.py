from hashids import Hashids

hashids = Hashids("secretsaltysaltines")
oracle_query_count = 0


def encode_oracle(number):
    """
    An encryption oracle. This exposes the hashids from which we determine the secret key.
    """
    global oracle_query_count
    oracle_query_count += 1
    return hashids.encode(number)


def solve_dual_mod(eqs):
    """
    Finds solutions for multiple equations in the form `2 × a = b mod c`.
    """
    results = []
    for i in range(0, 512, 2):  # 2a is always even, and a is in byte range
        matches_all = True
        for val, mod in eqs:
            if i % mod != val:
                matches_all = False
        if matches_all:
            results.append(i // 2)
    return results


before_first_shuffle = 'abdegjklmnopqrvwxyzABDEGJKLMNOPQRVWXYZ1234567890'  # default alphabet
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

salt = ""
for idx in range(0, 42):
    equations = []

    # first shuffle
    char = after_first_shuffle[-1 - idx]
    original_pos = before_first_shuffle.index(char)
    new_pos = 47 - idx
    integer_sum = sum([ord(c) for c in salt[0:idx]])
    salt_sum = (original_pos - integer_sum - idx) % new_pos
    print(f"{char}: {original_pos} -> {new_pos}")
    print(f"2 x salt[{idx}] = {original_pos} - {integer_sum} - {idx} = {salt_sum} mod {new_pos}")
    equations.append((salt_sum, new_pos))

    # second shuffle
    request = (42 - idx) * 44 + 43
    result = encode_oracle(request)
    print(f"{request} -> {result}")
    char = result[1]
    original_pos = after_first_shuffle.index(char)
    new_pos = 43 - idx
    mod = new_pos - 1
    lottery = result[0]
    integer_sum = ord(lottery) + sum([ord(c) for c in salt[0:idx]])
    salt_sum = (original_pos - integer_sum - idx - 1) % mod
    print(f"2 x salt[{idx}] = {original_pos} - {integer_sum} - {idx + 1} = {salt_sum} mod {mod}")
    equations.append((salt_sum, mod))

    # combine
    candidates = solve_dual_mod(equations)
    if len(candidates) == 1:
        salt += chr(candidates[0])
        print(f"salt: {salt}")
    else:
        print(f"No single solution found. Candidates: {candidates}")
        print(f"salt so far: {salt}")
        break

print(f"{oracle_query_count} oracle queries")

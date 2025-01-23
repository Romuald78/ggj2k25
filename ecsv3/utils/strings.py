

def get_next_number_name(name: str, nb_digits: int = 1, increase: int = 1) -> str:
    # Locals
    n = ''
    # Get number value at the end of the string
    for c in name[-1::-1]:
        if c.isdigit():
            n = c + n
        else:
            break
    # compute existing number length and update nb_digits if needed
    l = len(n)
    if l > nb_digits:
        nb_digits = l
    # remove the digits from the name (if there are some)
    # else set current number to 1
    if l > 0:
        name = name.replace(n, '')
    else:
        n = '1'
    # increase number
    n = str(int(n) + increase)
    # put nb '0' in front of result and cut
    l = max(len(n), nb_digits)
    n = '0' * l + n
    n = n[-l:]
    # reconstruct final name
    name += n
    return name

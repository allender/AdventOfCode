import sys

# predefine the range since we need this multiple times
r1 = range(0,6)

class DigitDict(dict):
    def __missing__(self, key):
        return 0

def isvalid(num):
    str_num = str(num)

    # check for numbers that are increasing
    for index in range(0, 5):
        if (str_num[index] > str_num[index+1]):
            return False

    # check for at least two consecutive digits the same
    # but only in pairs (can't have three or five for instance)
    counts = DigitDict()

    for index in range(0, 5):
        if (str_num[index] == str_num[index+1]):
            counts[str_num[index]] += 1

    for value in counts.values():
        if value == 1:
            return True

    return False

# returns the next valid number
def nextvalid(num):
    digits = [ (num // (10**i)) % 10 for i in range(5, -1, -1) ]
    prev_digit = digits[0]
    for index, digit in enumerate(digits[1:]):
        if (digit < prev_digit):
            for i in range(index+1, 6):
                digits[i] = prev_digit
            break
        prev_digit = digit

    return int(''.join(map(str, digits)))

numValid = 0
start = 372037
end = 905158
x = start
while x <= end:
    x = nextvalid(x)
    valid = isvalid(x)
    if (valid is True):
        numValid += 1

    x += 1

print (numValid)

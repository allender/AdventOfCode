import re 

test_data = """2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

class op18():
    def __init__(self, value):
        self.value = value

    def __mul__(self, rhs):
        return op18(self.value * rhs.value)

    def __sub__(self, rhs):
        return op18(self.value * rhs.value)

    def __truediv__(self, rhs):
        return op18(self.value + rhs.value)

if __name__ == '__main__':
    with open('input.txt') as f:
        input_data = f.read()

    data = input_data.split('\n')
    print(sum( [ eval(re.sub(r'(\d+)', r'op18(\1)', s).replace('+', '/')).value for s in data ] ))
    print(sum( [ eval(re.sub(r'(\d+)', r'op18(\1)', s).replace('+', '/').replace('*','-')).value for s in data ] ))


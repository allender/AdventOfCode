import sys


def calc_fuel(mass):
    fuel_total = 0
    current_mass = mass
    while (True):
        current_fuel = (int(current_mass) // 3) - 2
        if (current_fuel <= 0):
            break
        fuel_total += current_fuel
        current_mass = current_fuel

    return fuel_total
    

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read().splitlines()

    result = 0
    for d in data:
        result += calc_fuel(d)

    print (result)

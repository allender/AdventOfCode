from aocd import lines
from collections import Counter
from typing import List

test_lines = [
    '3,4,3,1,2'
]

def age_fish(age_data : List, days) -> List:
    for _ in range(days):
        # take first element of the list (age 0), add
        # in a new fish if need
        fish_age = age_data.pop(0)
        age_data.append(fish_age)
        age_data[6] += data[-1]
        
    return age_data
        

if __name__ == '__main__': 
    numbers = list(map(int, lines[0].split(',')))

    # create Counter object to keep track of the count
    # of fish at a given age.  and then convert to
    # list that has the counts at the age locations
    age_counter = Counter(numbers)
    data = [ age_counter[i] for i in range(9) ]
    print(sum(age_fish(data, 18)))
    print(sum(age_fish(data, 256)))

import re
import sys
import collections
import queue

sys.path.append('../..')

import utils

test_data = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

test_data1 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

# returns list of bags that can contein the contained_bag
# (contained_bag is a string).  Returns a
def containing_bags(all_bags, contained_bag):
    containing =  []
    for bag, contents in all_bags.items():
        for bag_color, count in contents.items():
            if bag_color == contained_bag:
                containing.append(bag)

    return containing

if __name__ == '__main__':
    with open('input.txt') as f:
        data = f.read()

    data = data.split('\n');

    exp = re.compile("(?P<color>\w+ \w+) bags contain (?P<contents>.*)\.")
    count_exp = re.compile("\s*(?P<count>\d+) (?P<color>\w+ \w+) bag[s]*")

    container_dict = {}
    for l in data:
        color_match = exp.match(l)
        if color_match == None:
            continue
        count_dict = {}
        for count, color in count_exp.findall(color_match.group('contents')):
            count_dict[color] = count
        container_dict[color_match.group('color')] = count_dict


    all_bags = []
    bag_queue = queue.SimpleQueue( )
    bag_queue.put("shiny gold")
    while bag_queue.empty() == False:
        bag = bag_queue.get()
        other_bags = containing_bags(container_dict, bag)
        all_bags.extend(other_bags)
        for l in other_bags:
            bag_queue.put(l)

    print(len(set(all_bags)))

    total_count = 0
    bag_queue.put("shiny gold")
    while bag_queue.empty() == False:
        bag = bag_queue.get()
        other_bags = container_dict[bag]
        for color, count in other_bags.items():
            for i in range(0, int(count)):
                total_count += 1
                bag_queue.put(color)

    print (total_count)



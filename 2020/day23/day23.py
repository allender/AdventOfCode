import array

test_data="""389125467"""
data="""394618527"""

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self, max_cups):
        self.head = None
        self.end = None
        self.val_dict = {}

    def insert(self, node):
        if self.head == None:
            self.head = node
            self.end = node
        else:
            self.end.next = node

        self.end = node
        self.end.next = self.head
        self.val_dict[node.value] = node

    def print(self, current = None):
        node = self.head
        while True:
            if node == current:
                print(f'({node.value})', end='')
            else:
                print(node.value, end='')
            node = node.next
            if node == self.head:
                break
        print('')

    def get_node(self, card):
        return self.val_dict[card]

    def insert_node(self, current, insert, start):
        end.next = insert.next
        insert.next = current.next


def play_game(cups, iterations, max_cups = 9):
    ll = LinkedList(max_cups)
    for c in cups:
        ll.insert(Node(int(c)))
    if max_cups > len(cups):
        for i in range(len(cups) + 1, max_cups + 1):
            ll.insert(Node(i))

    current_cup = ll.head
    for idx in range(1, iterations + 1):
        removed_cup = current_cup.next
        current_cup.next = removed_cup.next.next.next

        next_cup_value = current_cup.value - 1 if current_cup.value > 1 else max_cups
        while next_cup_value == removed_cup.value or next_cup_value == removed_cup.next.value or next_cup_value == removed_cup.next.next.value:
            next_cup_value = next_cup_value - 1 if next_cup_value != 1 else max_cups

        insert_cup = ll.get_node(next_cup_value)
        removed_cup.next.next.next = insert_cup.next
        insert_cup.next = removed_cup

        current_cup = current_cup.next

    cup_one = ll.get_node(1)
    if max_cups == 9:
        ll.print()
    else:
        print(cup_one.next.value, cup_one.next.next.value, cup_one.next.value * cup_one.next.next.value)

if __name__ == '__main__':
    play_game(data, 100)
    play_game(data, 10_000_000, 1_000_000)
  
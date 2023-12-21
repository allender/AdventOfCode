from aocd.models import Puzzle
from collections import OrderedDict, defaultdict
from math import lcm

puzzle = Puzzle(2023, 20)

inputs = puzzle.input_data.strip().split('\n')
# inputs = puzzle.examples[0][0].split('\n')

class Module(object):
    def __init__(self, label, outputs, initial_state):
        self.name = label
        self.dest_modules = [x.strip() for x in outputs.split(',')]
        self.state = initial_state 

class FlipFlop(Module):
    def pulse(self, src, state):
        if not state:
            self.state ^= 1
            return self.state
        
        return None

class Conjunction(Module):
    def __init__(self, labels, outputs, initial_state):
        super(Conjunction, self).__init__(labels, outputs, initial_state)
        self.input_states = {} 
        self.inputs_flipped = {} 

    def pulse(self, src, state):
        self.input_states[src.name] = state
        if all(self.input_states.values()):
            return 0
        return 1
            
class Broadcast(Module):
    def pulse(self, src, state):
        return state

class Button(Module):
    def __init__(self, label, outputs, initial_state):
        super(Button,self).__init__(label, outputs, initial_state)
        self.num_presses = 0

    def pulse(self, src, state):
        self.num_presses += 1
        return state

class Output(Module):
    def pulse(self, src, state):
        self.state = state

class System(object):
    def __init__(self):
        self.modules = {}
        self.counts = defaultdict(int) 
        self.conjunctions = []
        self.button = None
        self.final_conjunction = None
        self.final_output = None

    def add_module(self, label, outputs):
        if label == 'broadcaster':
            module = Broadcast(label, outputs, 0)
        elif label == 'button':
            module = Button(label, outputs, 0)
            self.button = module
        elif label[0] == '%':
            module = FlipFlop(label[1:], outputs, 0)
        elif label[0] == '&':
            module = Conjunction(label[1:], outputs, 0)
            self.conjunctions.append(module)
        else:
            module = Output(label, outputs, 0)
            if label == 'rx':
                self.final_output = module

        self.modules[module.name] = module
        return module

    def process_pulses(self):
        modules_to_process = [ (None, self.button, 0) ]
        while modules_to_process:
            src, dest, state = modules_to_process.pop(0)
            self.counts[state] += 1
            new_state = dest.pulse(src, state)
            if new_state is not None:
                # see if we rolled conjunction input
                if dest in self.conjunctions and state and src not in dest.inputs_flipped:
                    dest.inputs_flipped[src] = self.button.num_presses
                for x in dest.dest_modules:
                    modules_to_process.append((dest, x, new_state))

        if self.final_output is not None and self.final_output.state == 1 and len(self.final_conjunction.inputs_flipped) == len(self.final_conjunction.input_states):
            num_presses = lcm(*(self.final_conjunction.inputs_flipped.values()))
            print('Part2: ' + str(num_presses))
            return False
        
        return True

    def connect_system(self):
        new_modules = [ self.add_module(x, '') for m in self.modules.copy().values() for x in m.dest_modules if x not in self.modules ] 
        for m in self.modules.values():
            m.dest_modules = [ self.modules[x] for x in m.dest_modules if x in self.modules ]

        for m in self.modules.values():
            for dest in m.dest_modules:
                if dest.name == 'rx':
                    self.final_conjunction = m
                if dest in self.conjunctions:
                    dest.input_states[m.name] = 0

system = System()
for l in inputs:
    label, outputs = [ x.strip() for x in l.split('->') ]
    system.add_module(label, outputs)

button = system.add_module('button', 'broadcaster')
system.connect_system()

while system.process_pulses():
    if system.button.num_presses == 1000:
        print(system.counts[0] * system.counts[1])

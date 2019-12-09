import sys
from enum import Enum

class AddresssingMode(Enum):
    NONE = -1
    POSITION = 0
    IMMEDIATE = 1

class Machine():

    def reset(self, s):
        self.memory = [ int(x) for x in s.split(',') ]
        self.ip = 0

    def put_num(self, num, mode):
        self.memory[self.memory[self.ip]] = num
        self.ip += 1

    def get_num(self, mode):
        num = self.memory[self.ip]
        if (mode == AddresssingMode.POSITION.value):
            num = self.memory[num]
        self.ip += 1
        return num

    def process_opcode(self):
        opcode = self.memory[self.ip]
        machine.ip += 1

        command = opcode % 100
        mode1 = (opcode // 100) % 10
        mode2 = (opcode // 1000) % 10
        mode3 = (opcode // 10000) % 10
        
        #print(mode3, mode2, mode1, command)
        return command, mode1, mode2, mode3

    def opadd(self, mode1, mode2, mode3):
        num1 = self.get_num(mode1)
        num2 = self.get_num(mode2)
        assert(mode3 != AddresssingMode.IMMEDIATE)
        self.put_num(num1 + num2, mode3)

    def opmult(self, mode1, mode2, mode3):
        num1 = self.get_num(mode1)
        num2 = self.get_num(mode2)
        assert(mode3 != AddresssingMode.IMMEDIATE)
        self.put_num(num1 * num2, mode3)

    def opinput(self, mode):
        # get input and store it 
        input = 5
        self.put_num(input, mode)

    def opoutput(self, mode):
        value = self.get_num(mode)
        print(value)
        
    def opjumpiftrue(self, mode1, mode2):
        value = self.get_num(mode1)
        if (value != 0):
            self.ip = self.get_num(mode2)
        else:
            self.ip += 1

    def opjumpiffalse(self, mode1, mode2):
        value = self.get_num(mode1)
        if (value == 0):
            self.ip = self.get_num(mode2)
        else:
            self.ip += 1

    def oplessthan(self, mode1, mode2, mode3):
        value1 = self.get_num(mode1)
        value2 = self.get_num(mode2)
        if (value1 < value2):
            self.put_num(1, mode3)
        else:
            self.put_num(0, mode3)

    def opequals(self, mode1, mode2, mode3):
        value1 = self.get_num(mode1)
        value2 = self.get_num(mode2)
        if (value1 == value2):
            self.put_num(1, mode3)
        else:
            self.put_num(0, mode3)

    def run(self):
        while (True):
            opcode, mode1, mode2, mode3 = self.process_opcode()
            if (opcode == 1):
                self.opadd(mode1, mode2, mode3)
            elif (opcode == 2):
                self.opmult(mode1, mode2, mode3)
            elif (opcode == 3):
                self.opinput(mode1)
            elif (opcode == 4):
                self.opoutput(mode1)
            elif (opcode == 5):
                self.opjumpiftrue(mode1, mode2)
            elif (opcode == 6):
                self.opjumpiffalse(mode1, mode2)
            elif (opcode == 7):
                self.oplessthan(mode1, mode2, mode3)
            elif (opcode == 8):
                self.opequals(mode1, mode2, mode3)
            elif (opcode == 99):
                break
            else:
                print("bad opcode {0}".format(opcode))
                sys.exit(-1)


machine = Machine()

if __name__ == '__main__':
    with open('input.txt') as f:
        s = f.read()

    machine.reset(s)
    machine.run()



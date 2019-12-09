import sys

from enum import Enum

class AddresssingMode(Enum):
    NONE = -1
    POSITION = 0
    IMMEDIATE = 1

class IntComputer():

    def __init__(self, program):
        self._memory = [ int(x) for x in program.split(',') ]
        self.reset( )

    def reset(self):
        # reset the memory used for the program
        self.memory = self._memory.copy( )
        self.inputs = [ ]
        self.output = 0
        self.ip = 0
        self.is_running = False

    def _put_num(self, num, mode):
        self.memory[self.memory[self.ip]] = num
        self.ip += 1

    def _get_num(self, mode):
        num = self.memory[self.ip]
        if mode == AddresssingMode.POSITION.value:
            num = self.memory[num]
        self.ip += 1
        return num

    def _process_opcode(self):
        opcode = self.memory[self.ip]
        self.ip += 1

        command = opcode % 100
        mode1 = (opcode // 100) % 10
        mode2 = (opcode // 1000) % 10
        mode3 = (opcode // 10000) % 10

        #print(mode3, mode2, mode1, command)
        return command, mode1, mode2, mode3

    def _opadd(self, mode1, mode2, mode3):
        num1 = self._get_num(mode1)
        num2 = self._get_num(mode2)
        assert mode3 != AddresssingMode.IMMEDIATE
        self._put_num(num1 + num2, mode3)

    def _opmult(self, mode1, mode2, mode3):
        num1 = self._get_num(mode1)
        num2 = self._get_num(mode2)
        assert mode3 != AddresssingMode.IMMEDIATE
        self._put_num(num1 * num2, mode3)

    def _opinput(self, mode):
        # get input and store it
        input = self.inputs.pop(0)
        self._put_num(input, mode)

    def _opoutput(self, mode):
        value = self._get_num(mode)
        self.output = value

    def _opjumpiftrue(self, mode1, mode2):
        value = self._get_num(mode1)
        if value != 0:
            self.ip = self._get_num(mode2)
        else:
            self.ip += 1

    def _opjumpiffalse(self, mode1, mode2):
        value = self._get_num(mode1)
        if value == 0:
            self.ip = self._get_num(mode2)
        else:
            self.ip += 1

    def _oplessthan(self, mode1, mode2, mode3):
        value1 = self._get_num(mode1)
        value2 = self._get_num(mode2)
        if value1 < value2:
            self._put_num(1, mode3)
        else:
            self._put_num(0, mode3)

    def _opequals(self, mode1, mode2, mode3):
        value1 = self._get_num(mode1)
        value2 = self._get_num(mode2)
        if value1 == value2:
            self._put_num(1, mode3)
        else:
            self._put_num(0, mode3)

    def run(self):
        self.is_running = True
        while True:
            opcode, mode1, mode2, mode3 = self._process_opcode()
            if opcode == 1:
                self._opadd(mode1, mode2, mode3)
            elif opcode == 2:
                self._opmult(mode1, mode2, mode3)
            elif opcode == 3:
                if not self.inputs:
                    # go back one instruction so we process
                    # the input again
                    self.ip -= 1
                    break
                self._opinput(mode1)
            elif opcode == 4:
                self._opoutput(mode1)
            elif opcode == 5:
                self._opjumpiftrue(mode1, mode2)
            elif opcode == 6:
                self._opjumpiffalse(mode1, mode2)
            elif opcode == 7:
                self._oplessthan(mode1, mode2, mode3)
            elif opcode == 8:
                self._opequals(mode1, mode2, mode3)
            elif opcode == 99:
                self.is_running = False
                break
            else:
                print("bad opcode {0}".format(opcode))
                sys.exit(-1)


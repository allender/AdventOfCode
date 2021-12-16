from aocd import lines
from typing import List
from functools import reduce
from operator import mul

def parse_input(lines: List) -> List:
    bits = []
    for c in lines[0]:
        num = format(int(c, 16), '04b')
        bits.extend( [ b for b in num] )

    return bits 

class Packet():
    bitstream = None
    listpos = 0

    def __init__(self, stream = None):
        if stream is not None:
            Packet.bitstream = stream

        self.packet_version = self.parse(3)
        self.packet_type = self.parse(3)
        self.subpackets = []
        self.value = None

        if self.packet_type == 4:
            self.value = self.parse_literal()
        else:
            # operator packet 
            id = self.parse(1)
            if id == 0:
                packet_length = self.parse(15)
                cur_pos = Packet.listpos
                while Packet.listpos < cur_pos + packet_length:
                    self.subpackets.append( Packet() )
            elif id == 1:
                num_packets = self.parse(11)
                for _ in range(num_packets):
                    self.subpackets.append( Packet() )

            values = [ x.value for x in self.subpackets ]
            if self.packet_type == 0:
                self.value = sum( values )
            elif self.packet_type == 1:
                self.value = reduce(mul, values, 1)
            elif self.packet_type == 2:
                self.value = min(values)
            elif self.packet_type == 3:
                self.value = max(values)
            elif self.packet_type == 5:
                self.value = int(self.subpackets[0].value > self.subpackets[1].value)
            elif self.packet_type == 6:
                self.value = int(self.subpackets[0].value < self.subpackets[1].value)
            elif self.packet_type == 7:
                self.value = int(self.subpackets[0].value == self.subpackets[1].value)

    def parse(self, num_bits: int) -> int:
        val = int(''.join(Packet.bitstream[Packet.listpos:Packet.listpos + num_bits]), 2)
        Packet.listpos += num_bits
        return val

    def parse_literal(self) -> int:
        literal = [] 
        while True:
            keep_reading = int(Packet.bitstream[Packet.listpos], 2)
            Packet.listpos += 1
            literal.extend(Packet.bitstream[Packet.listpos:self.listpos + 4])
            Packet.listpos += 4

            if keep_reading == 0:
                break

        val = int(''.join(literal), 2)
        return val


def parse_packets(bitstream: List) -> Packet: 
    return Packet(bitstream)

def count_versions(packet: Packet) -> int:
    version = packet.packet_version
    for p in packet.subpackets:
        version += count_versions(p)

    return version

if __name__ == '__main__': 
    bitstream = parse_input(lines)
    packets = parse_packets(bitstream)
    print(count_versions(packets))
    print(packets.value)

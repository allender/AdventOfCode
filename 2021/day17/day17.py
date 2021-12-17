from aocd import lines
import re

test_lines = [
	'target area: x=20..30, y=-10..-5'
]

def part2(xmin, xmax, ymin, ymax):
    total = 0

	# loop through reduced search space
    for starting_v_x in range(1, xmax + 1):
        for startying_v_Y in range(ymin, -ymin):
            x, y = 0, 0
            vx, vy = starting_v_x, startying_v_Y

            while x <= xmax and y >= ymin:
                if x >= xmin and y <= ymax:
                    total += 1
                    break

                x, y = (x + vx, y + vy)
                vy -= 1
                if vx > 0:
                    vx -= 1

    return total
	
def part1(ymin: int, ymax: int) -> int:
	return ymin * (ymin + 1) // 2

if __name__ == '__main__': 
	mo = re.match( 'target area: x=([-]?\d+)\.\.([-]?\d+), y=([-]?\d+)\.\.([-]?\d+)', lines[0] )
	(xmin, xmax) = int(mo.group(1)), int(mo.group(2))
	(ymin, ymax) = int(mo.group(3)), int(mo.group(4))

	print(part1(ymin, ymax))
	print(part2(xmin, xmax, ymin, ymax))

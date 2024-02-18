#<root>/src/main.py

"""
!!!DISCLAIMER!!!
Naive implementation of the Brainfuck algorithm
Not done in the most pythonic way so take it with a pinch of salt
"""

import sys

RAW_CODE_FILE = '../examples/hell_no_world.bf'
OPERATIONS    = ''

instructions        = ''
memory_cells        = [0]
memory_pointer      = 0
instruction_pointer = 0
execution_step      = 0
next_count	    = 5
lines_count    	    = 1
output_strip	    = []
input_strip	    = []
is_loop		    = False
loops_pointers      = []

class Operations:
	MPR 	  = '>'     # 62 - increment memory pointer (Memory Pointer Right)
	MPL 	  = '<'     # 93 - decrement memory pointer (Memory Pointer Left)
	ADD 	  = '+'     # 43 - increment memory cell value by 1
	SUB 	  = '-'     # 44 - decrement memory cell value by 1
	ICH 	  = ','     # 46 - input character and store at memory pointer (Input CHaracter)
	OCH 	  = '.'     # 45 - output memory as character (Output CHaracter)
	JZR 	  = '['     # 91 - start loop (jump to end on 0) (Jump on Zero Right)
	JNL 	  = ']'     # 60 - end loop (jump to start on != 0)	(Jump on Non-zero Left)

	count_mpr = 0
	count_mpl = 0
	count_add = 0
	count_sub = 0
	count_ich = 0
	count_och = 0
	count_jzr = 0
	count_jnl = 0

def clear_line(lines = 1):
	LINE_UP = '\033[1A'
	LINE_CLEAR = '\x1b[2K'
	for idx in range(lines):
		print(LINE_UP, end=LINE_CLEAR)

def next_instructions(index, instructions_set, count=1):
	next_set = []
	for idx in range(1, count + 1):
		if index + idx < len(instructions):
			next_set.append(chr(instructions_set[index + idx]))
	return next_set

def memory_colors(head, memory):
	formated_output = f'\033[31m[\033[0m '
	for idx, value in enumerate(memory):
		if idx == head:
			formated_output += f'\033[32m{value}\033[0m '
		else:
			formated_output += f'\033[93m{value}\033[0m '
	formated_output += f'\033[31m]\033[0m'
	return formated_output

with open(RAW_CODE_FILE, 'rb') as file:
	instructions = file.read().replace(b'\n', b'')

OPERATIONS = set(instructions)

print(f"[+] The BF program has: \033[93m{len(instructions)}\033[0m instruction(s)")
print(f"[+] Operands in the given code: \033[32m{[chr(value) for value in OPERATIONS]}\033[0m")

while instruction_pointer < len(instructions):
	execution_step += 1
	if len(loops_pointers) > 0:
		is_loop = True
	else:
		is_loop = False

	print(f"-" * 50)
	print(f"Execution Step : \033[93m{execution_step:<6}\033[0m")
	print(f"-" * 50)
	print(f"Current memory values	 : {memory_colors(memory_pointer, memory_cells)}")
	print(f"Current Instruction      : \033[31m{chr(instructions[instruction_pointer])}\033[0m")
	print(f"Instruction Pointer      : \033[32m{instruction_pointer}\033[0m")
	print(f"Current Head Position    : \033[93m{memory_pointer}\033[0m")
	print(f"Current Value at Head    : \033[93m{memory_cells[memory_pointer]}\033[0m")
	print(f"Memory Length            : \033[93m{len(memory_cells)}\033[0m")
	print(f"In a loop                : \033[93m{is_loop}\033[0m")
	print(f"Loops pointers           : \033[93m{loops_pointers}\033[0m")
	print(f"Input Strip              : \033[93m{input_strip}\033[0m")
	print(f"Output Strip             : \033[93m{output_strip}\033[0m")
	print(f"Next Instruction(s) (\033[31m{next_count:>02}\033[0m) : \033[93m{next_instructions(instruction_pointer, instructions, count=next_count)}\033[0m")
	print(f"-" * 50)

	match chr(instructions[instruction_pointer]):
		case Operations.MPR:
			Operations.count_mpr += 1
			memory_pointer += 1
			if memory_pointer >= len(memory_cells):
				memory_cells.append(0)
		
		case Operations.MPL:
			Operations.count_mpl += 1
			memory_pointer -= 1
			if memory_pointer < 0:
				memory_pointer = 0
				memory_cells.insert(0, 0)

		case Operations.ADD:
			Operations.count_add += 1
			memory_cells[memory_pointer] = (memory_cells[memory_pointer] + 1 + 256) % 256

		case Operations.SUB:
			Operations.count_sub += 1
			memory_cells[memory_pointer] = (memory_cells[memory_pointer] - 1 + 256) % 256

		case Operations.ICH:
			Operations.count_ich += 1
			char_input = input(f"Enter char code:")
			
			# Input treated as is - be careful (0, 255)
			#memory_cells[memory_pointer] = int(char_input.strip())
			
			# Input treated as ASCII char (more than one char gives error)
			if len(char_input) > 1:
				char_input = char_input[0]
			if len(char_input) == 0:
				print(f"\033[31mInput is empty. Aborting...\033[0m")
				break
			memory_cells[memory_pointer] = ord(char_input.strip())
			input_strip.append(char_input)

		case Operations.OCH:
			Operations.count_och += 1
			output_strip.append(memory_cells[memory_pointer])

		case Operations.JZR:
			Operations.count_jzr += 1
			if memory_cells[memory_pointer] == 0:
				loop_counter = 1
				while instruction_pointer < len(instructions) - 1:
					instruction_pointer += 1
					if chr(instructions[instruction_pointer]) == Operations.JNL:
						if loop_counter == 1:
							#instruction_pointer -= 1
							if len(loops_pointers) > 0:
								del loops_pointers[-1]
							break
						else:
							loop_counter -= 1
					elif chr(instructions[instruction_pointer]) == Operations.JZR:
						loop_counter += 1
				else:
					print(f"\033[31mInstruction pointer overflow. Aborting...\033[0m")
					break
			else:
				if len(loops_pointers) > 0:
					if loops_pointers[-1] != instruction_pointer:
						loops_pointers.append(instruction_pointer)
				else:
					loops_pointers.append(instruction_pointer)

		case Operations.JNL:
			Operations.count_jnl += 1
			if memory_cells[memory_pointer] != 0:
				loop_counter = 1
				while instruction_pointer > 0:
					instruction_pointer -= 1
					if chr(instructions[instruction_pointer]) == Operations.JZR:
						if loop_counter == 1:
							instruction_pointer -= 1
							break
						else:
							loop_counter -= 1
					elif chr(instructions[instruction_pointer]) == Operations.JNL:
						loop_counter += 1
				else:
					print(f"\033[31mInstruction pointer underflow. Aborting...\033[0m")
					break
			else:
				if len(loops_pointers) > 0:
					del loops_pointers[-1]

		case _:
			print(f"\033[31mUnknown instruction '{chr(instructions[instruction_pointer])}'. Aborting...\033[0m")
			break


	instruction_pointer += 1
	#input(f"Press ENTER to continue...")
	clear_line(lines_count)

print(f"-" * 50)
print(f"[+] Number of operations per instruction:")
print(f"\t [-] \033[32m>\033[0m operations: \033[93m{Operations.count_mpr}\033[0m")
print(f"\t [-] \033[32m<\033[0m operations: \033[93m{Operations.count_mpl}\033[0m")
print(f"\t [-] \033[32m+\033[0m operations: \033[93m{Operations.count_add}\033[0m")
print(f"\t [-] \033[32m-\033[0m operations: \033[93m{Operations.count_sub}\033[0m")
print(f"\t [-] \033[32m.\033[0m operations: \033[93m{Operations.count_ich}\033[0m")
print(f"\t [-] \033[32m,\033[0m operations: \033[93m{Operations.count_och}\033[0m")
print(f"\t [-] \033[32m[\033[0m operations: \033[93m{Operations.count_jzr}\033[0m")
print(f"\t [-] \033[32m]\033[0m operations: \033[93m{Operations.count_jnl}\033[0m")

print(f"Memory length  : \033[93m{len(memory_cells)}\033[0m")
print(f"Memory pointer : \033[93m{memory_pointer}\033[0m")
print(f"Memory content : \033[93m{memory_colors(memory_pointer, memory_cells)}\033[0m")
print(f"Memory chars   : \033[93m{[chr(value) for value in memory_cells]}\033[0m")
print(f"Output length  : \033[93m{len(output_strip)}\033[0m")
print(f"Output         : \33[93m{[chr(value) for value in output_strip]}\033[0m")
print(f"Unified output : \033[32m{''.join([chr(value) for value in output_strip])} \033[0m")

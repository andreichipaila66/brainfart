# brainfart
Naive implementation of the Brainf**k esoteric programming language

Background

Brainfuck operates on an array of memory cells, initially all set to zero.
The memory array is conceptually infinite, although practical implementations may impose a finite limit.

Commands:

>: Move the memory pointer to the right (increment the memory pointer).
<: Move the memory pointer to the left (decrement the memory pointer).
+: Increment the byte at the memory pointer.
-: Decrement the byte at the memory pointer.
[: Jump past the matching ] if the byte at the memory pointer is zero (begin loop).
]: Jump back to the matching [ if the byte at the memory pointer is nonzero (end loop).
.: Output the byte at the memory pointer (as a character).
,: Input a byte and store it in the byte at the memory pointer.

Interpretation:

Brainfuck programs are interpreted sequentially, with each command being executed one after the other.
Loops (denoted by [ and ]) allow for conditional execution and looping constructs.
Memory Manipulation:

The < and > commands move the memory pointer left and right, respectively, allowing the program to access different memory cells.
The + and - commands increment and decrement the byte at the current memory cell, respectively.
Control Flow:

Loops in Brainfuck are implemented using the [ and ] commands.
The [ command begins a loop, and the ] command jumps back to the matching [ if the byte at the current memory cell is nonzero.
Input/Output:

The . command outputs the byte at the current memory cell as a character.
The , command reads a character of input and stores its ASCII value in the current memory cell.

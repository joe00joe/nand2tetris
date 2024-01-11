// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


@sum          //sum指代某个内存单元
M=0           //sum=0
(LOOP)
@1
D=M
@0
D=D-A         //r1=r1-0
@END
D;JLE         //If i <= 0 goto END
@0
D=M           //D=R0
@sum
M=D+M         //sum = sum + R0
@1
M=M-1         //R1 = R1 - 1
@LOOP
0;JMP         //goto LOOP
(END)
@sum
D=M
@2
M=D            //R2 = sum
(EXIT)
@EXIT
0;JMP         //无限循环


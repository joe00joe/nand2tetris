@256
D=A
@SP
M=D
@RETURN_SYS.INIT_1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@0
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Sys.init
0;JMP
(RETURN_SYS.INIT_1)
(init$END)
@init$END
0;JMP
//..\FunctionCalls\FibonacciElement\Main.vm
(Main.fibonacci)
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R14
D=M
@R15
A=M
D=D-A
@RET_TRUE1
D;JLT
D=0
@CONTINUE1
0;JMP
(RET_TRUE1)
D=-1
(CONTINUE1)
@R13
M=D
@R13
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@Main$IF_TRUE
D;JNE
@Main$IF_FALSE
0;JMP
(Main$IF_TRUE)
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R14
M=D
@R14
A=M
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@R14
A=M
A=A-1
A=A-1
D=M
@THIS
M=D
@R14
A=M
A=A-1
D=M
@THAT
M=D
@R14
A=M
A=A-1
A=A-1
A=A-1
D=M
@ARG
M=D
@R14
A=M
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@R13
A=M
0;JMP
(Main$IF_FALSE)
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R14
D=M
@R15
A=M
D=D-A
@R13
M=D
@R13
D=M
@SP
A=M
M=D
@SP
M=M+1
@RETURN_MAIN.FIBONACCI_2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_MAIN.FIBONACCI_2)
@ARG
A=M
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
@SP
A=M
D=M
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R14
D=M
@R15
A=M
D=D-A
@R13
M=D
@R13
D=M
@SP
A=M
M=D
@SP
M=M+1
@RETURN_MAIN.FIBONACCI_3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_MAIN.FIBONACCI_3)
@SP
M=M-1
@SP
A=M
D=M
@R15
M=D
@SP
M=M-1
@SP
A=M
D=M
@R14
M=D
@R14
D=M
@R15
A=M
D=D+A
@R13
M=D
@R13
D=M
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@R14
M=D
@R14
A=M
A=A-1
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@R13
M=D
@SP
M=M-1
@SP
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
D=D+1
@SP
M=D
@R14
A=M
A=A-1
A=A-1
D=M
@THIS
M=D
@R14
A=M
A=A-1
D=M
@THAT
M=D
@R14
A=M
A=A-1
A=A-1
A=A-1
D=M
@ARG
M=D
@R14
A=M
A=A-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@R13
A=M
0;JMP
//..\FunctionCalls\FibonacciElement\Sys.vm
(Sys.init)
@4
D=A
@SP
A=M
M=D
@SP
M=M+1
@RETURN_MAIN.FIBONACCI_4
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@1
D=D-A
@5
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(RETURN_MAIN.FIBONACCI_4)
(Sys$WHILE)
@Sys$WHILE
0;JMP
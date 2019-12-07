.global _start

_start:
	MOV R4, #10
loopstart:
	MOV R7, #4
	MOV R0, #1
	MOV R2, #5
	LDR R1, =msg
	SWI 0
	SUB R4, R4, #1
	CMP R4, #0
	BGT loopstart

end:
	MOV R7, #1
	SWI 0

.data
msg:
	.ascii "loop\n"


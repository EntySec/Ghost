.global _start
_start:
	ADR R3, numbers
	LDMIA R3, {R5-R8}
	MOV R0, R8

end:
	MOV R7, #1
	SWI 0

.align 2
numbers:
	.word 1, 2, 3, 4

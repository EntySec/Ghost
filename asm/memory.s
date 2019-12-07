.data
.balign 4
fifteen:
	.word 15

.balign 4
thirty:
	.word 30

.text
.global _start

_start:
	LDR R1, addr_fifteen
	LDR R1, [R1]
	LDR R2, addr_thirty
	LDR R2, [R2]
	ADD R0, R1, R2

end:
	MOV R7, #1
	SWI 0

addr_fifteen: .word fifteen
addr_thirty: .word thirty 


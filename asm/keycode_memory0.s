.data
.balign 4
fifteen:
	.word 0

.balign 4
thirty:
	.word 0

.text
.global _start

_start:
	LDR R1, addr_fifteen
	MOV R3, #15
	STR R3, [R1]
	
	LDR R2, addr_thirty
	MOV R3, #30
	STR R3, [R2]

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


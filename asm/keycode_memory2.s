.data
primes:
	.word 2
	.word 3
	.word 5
	.word 7

.text
.global _start
_start:
	LDR R3, =primes
	LDR R0, [R3, #100]

end:
	MOV R7, #1
	SWI 0

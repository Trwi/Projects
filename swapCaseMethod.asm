[BITS 32]
global _SwapCase

section .bss
single: resb 1

section .data

section .text

_SwapCase:

	push    	ebp				; establish a stack frame
    	mov    	 	ebp, esp			; establish a stack frame

	lea		ebx, [ebp + 8]			; Grab the correct spot for the string parameter on the stack and place it into ebx
	mov		ebx, [ebx]			; Grab the pointer to the string (address where string resides) back into ebx

loop1:
	
	mov		dl, byte [ebx]			; move a byte of the string into dl (lowest byte of edx)
	cmp		dl, 0				; compare the byte (character) to 0
	je		end				; jump to the end of the program if it is equal to 0, we found the end of the string
	cmp		dl, 65				; compare the byte to 65 (the decimal value for character 'A' in the ascii table)
	jge		loop2				; if the byte is greater than 65, we know it might be a character. Jump to loop2.
	jmp		reset				; jump to reset, the character was not a letter

loop2:
	
	cmp		dl, 90				; compare the byte to 90 (the decimal value for 'Z' in the ascii table)
	jg		loop3				; if the byte is greater than 90, it may be a lowercase character. jump to loop3
	add		dl, 32				; if the byte is less that 90, we know we have a capital letter. add 32 to turn into lowercase letter
	mov		byte [ebx], dl			; move the newly altered byte back into the correct memory location 
	jmp		reset				; jump to reset, we successfully altered the character

loop3:

	cmp		dl, 97				; compare the byte to 97 (the decimal value for 'a' in the ascii table)
	jl		reset				; jump to reset, the byte is not a letter
	cmp		dl, 122				; compare the byte to 122 (the decimal value for 'z' in the ascii table)
	jg		reset				; jump to reset, the byte is not a letter
	sub		dl, 32				; if the byte is between 97 and 122, we know we have a lowercase character, subtract 32 to make it uppercase
	mov		byte [ebx], dl			; move the newly altered byte back into the correct memory location
	jmp		reset				; jump to reset, we successfully altered the character

reset:
	
	inc		ebx				; increment the value of ebx to get the next byte (character)
	jmp		loop1				; jump to loop1 to start the process over/look at the next character

end:

	mov     esp, ebp            ; remove the stack frame
    	pop     ebp                 ; remove the stack frame
	ret			    ; return to calling c program

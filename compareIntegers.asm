

global  _main
extern  _printf
extern  _scanf
extern  _ExitProcess@4

section .bss
number1:     resd 1
number2:     resd 1

section .data
hello:      db 'Hello, this program will accept two integers and print them from least to greatest or state that they are equal.', 0ah, 0ah, 0
prompt1:    db 'Enter integer number 1: ', 0
prompt2:    db 0ah, 'Enter integer number 2: ', 0      
frmt:       db '%d', 0
equal:      db 0ah, 'The integers are equal.', 0ah, 0ah, 0
endM:       db 0ah, 'The integers in order are %d and %d.', 0ah, 0ah, 0

section .text
_main:

    
    push    ebp                     ; establish a stack frame
    mov     ebp, esp                ; establish a stack frame
    
    push    hello                   ; Push the hello prompt onto the stack
    call    _printf                 ; call printf function
    add     esp, 4                  ; Reset the stack pointer

    push    prompt1                 ; push prompt1 onto the stack
    call    _printf                 ; call printf function
    add     esp, 4                  ; reset the stack pointer
                    
    push    number1                 ; push the number1 variable
    push    frmt                    ; push the format string for scanf
    call    _scanf                  ; call the scanf function
    add     esp, 8                  ; reset the stack pointer

    push    prompt2                 ; push prompt2 onto the stack
    call    _printf                 ; call printf function
    add     esp, 4                  ; reset the stack pointer

    push    number2                 ; push the number2 variable
    push    frmt                    ; push the format string for scanf
    call    _scanf                  ; call scanf function
    add     esp, 8                  ; reset the stack pointer
    
    mov     ebx, dword [number1]    ; move the value stored inside number1 variable into ebx
    cmp     ebx, dword [number2]    ; compare the number1 value stored inside ebx against the value inside the number2 variable
    jg      n1                      ; jump to the n1 method if n1 is greater
    je      eq                      ; jump to the eq method if equal

    push    dword [number2]         ; push the value inside variable number2 onto the stack
    push    dword [number1]         ; push the value inside variable number1 onto the stack
    push    endM                    ; push the end message 
    call    _printf                 ; call printf function
    add     esp, 12                 ; reset the stack pointer
    jmp     end                     ; jump to the end method
      
n1:

    push    dword [number1]         ; push the value inside variable number1 onto the stack
    push    dword [number2]         ; push the value inside variable number2 onto the stack
    push    endM                    ; push the end message
    call    _printf                 ; call printf function
    add     esp, 12                 ; reset the stack pointer
    jmp     end                     ; jump to end method

eq:

    push    equal                   ; push equal message
    call    _printf                 ; call printf function
    add     esp, 4                  ; reset the stack pointer
    
end:   

    mov     esp, ebp                ; remove the stack frame
    pop     ebp                     ; remove the stack frame
   
    push 0                          ; push 0 for the exit process
    call _ExitProcess@4             ; exit the program
    
   

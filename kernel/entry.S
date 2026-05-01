        # qemu -kernel loads the kernel at 0x80000000
        # and causes each hart (i.e. CPU) to jump there.
        # kernel.ld causes the following code to
        # be placed at 0x80000000.
.section .text
.global _entry
_entry:
        # set up a stack for C.
        # stack0 is declared in start.c,
        # with a 4096-byte stack per CPU.
        # sp = stack0 + ((hartid + 1) * 4096) # hart 0 -> hartid + 1 -> hart 0+i
        la sp, stack0
        li a0, 1024*4 # 4096 is stored in register a0
        csrr a1, mhartid # mhartid is stored in register a1
        addi a1, a1, 1 # hartid is increment by 1 and stored in same register a1, a1 stores id of hardware thread (hart)
        mul a0, a0, a1 # ((hartid + 1) * 4096) hart0 stores at 4096, hart1 stores at 8192.. until hart7 
        add sp, sp, a0 # adding hart address into stack0
        # jump to start() in start.c
        call start #jumps to start() in start.c
spin:
        j spin

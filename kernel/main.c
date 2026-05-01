#include "types.h"
#include "param.h"
#include "memlayout.h"
#include "riscv.h"
#include "defs.h"

volatile static int pgtbl_ready = 0;   // page table built
volatile static int started = 0;       // full init done

// start() jumps here in supervisor mode on all CPUs.
void
main()
{
  if(cpuid() == 0){
    uint64 t_boot_start = r_time();

    consoleinit();
    printfinit();


    // printf("\n");
    // printf("xv6 kernel is booting\n");
    // printf("\n");
    printf("\n[BOOT] start=%lu\n", t_boot_start);
    uint64 t0 = r_time();

    kinit();         // physical page allocator
    printf("[BOOT] kinit         %lu ticks\n", r_time() - t0);

    t0 = r_time();
    kvminit();       // create kernel page table
    kvminithart();   // turn on paging
    __sync_synchronize();
    pgtbl_ready = 1;    // <-- release secondary harts here
    printf("[BOOT] vm_init       %lu ticks\n", r_time() - t0);

    t0 = r_time();
    procinit();      // process table
    printf("[BOOT] procinit      %lu ticks\n", r_time() - t0);

    trapinit();      // trap vectors
    trapinithart();  // install kernel trap vector
    // plicinit();      // set up interrupt controller
    // plicinithart();  // ask PLIC for device interrupts

    // Experiment D: binit/iinit/fileinit/virtio_disk_init deferred to first file open
    // (lazy init triggered from filealloc() in file.c)

    t0 = r_time();
#ifndef NODISK
    userinit();      // first user process
#endif
    printf("[BOOT] userinit      %lu ticks\n", r_time() - t0);

    printf("[BOOT] total_kernel  %lu ticks\n", r_time() - t_boot_start);
    __sync_synchronize();
    started = 1;
  } else {
    while(pgtbl_ready == 0)
      ;
    __sync_synchronize();
    kvminithart();    // turn on paging
    trapinithart();   // install kernel trap vector
    // plicinithart();   // Experiment I.1: PLIC disabled
  }

  // Experiment G2: arm timer now — boot is done, scheduler is about to run.
  w_stimecmp(r_time() + 1000000);
  scheduler();        
}

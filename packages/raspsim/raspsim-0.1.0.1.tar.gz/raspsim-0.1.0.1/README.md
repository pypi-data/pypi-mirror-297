# RASPsim

`RASPsim` is a cycle-accurate x86-64 simulator, forked from PTLsim. This simulator allows you to configure the virtual address space and initial register values, start simulation, and retrieve the latest register state, requested memory dumps, and the number of cycles and instructions simulated.

## Python Binding

`raspsim` includes a Python binding, allowing you to interface directly with the simulator. Below is an example of how to use the module directly:

```bash
python -m raspsim << EOF
.global _start
.intel_syntax noprefix
.text
_start:
mov rax, 1
int 0x80
EOF
```

## Usage
The raspsim Python module provides a range of features to interact with the simulator:

- Raspsim Class: This is the main class used to interact with the simulator. It provides methods to map memory pages, run the simulation, and access various registers. Only one instance of this class can be used at a time due to the havy use of global state of PTLsim.
- Address Class: This class allows reading and writing data at a specific address.
- Prot Enum: This enumeration provides memory protection flags, such as READ, WRITE, and EXEC.

The python module also provides several utility functions that ease the use of the simulator:
- `i[8|16|32|64]` classes that can be used to compare register values and store their values as an unsigned [8|16|32|64]-bit integer.
- The contextmanager `rscompile` that can be used to compile code with the appropiate flags for the simulator.
- The ELF dataclass that represents program sections of an elf file and `load_elf` function to parse a byte stream into an ELF object.
- The `populate_from_elf` function that can be used to load the program sections of an ELF object into the simulator.
- The `asm_preable` and `asm_stop_sim` functions that return some boilerplate asm code to setup a global label and raise the internal interrupt to stop the simulation respectively.
- `elf_add_trampoline` function that can be used to add a trampoline (a call to the original entry point follow by a stop-simulation interrupt) to an ELF object. This is useful to run the simulation until the end of the program and ensure that the original entry point returned gracefully.

Example:
```python
code = asm_preable() + "mov rax, -1\n" + asm_stop_sim()
with rscompile(code) as f:
    elf = load_elf(f)

sim = Raspsim()
populate_from_elf(sim, elf)
sim.run()
assert sim.rax == i64(-1) # Check if rax is -1, although registers return 64-bit unsigned values
```
        

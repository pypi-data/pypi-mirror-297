import sys
from .utils import rscompile, populate_from_elf, load_elf
from .core import Raspsim

if __name__ == "__main__":
    # check if arguments given
    if len(sys.argv) > 1:
        print("Usage: python -m pyraspsim < <file>\n\nRunning as module reads from stdin and does not take arguments.", file=sys.stderr)

    program = "\n".join(sys.stdin.readlines())

    with rscompile(program) as f:
        elf = load_elf(f)
        
    # Create a new Raspsim instance
    sim = Raspsim()

    populate_from_elf(sim, elf)

    # Run the simulation
    sim.run()

    # Print the simulation state
    print(sim)

    
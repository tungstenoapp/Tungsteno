from tsteno.kernel.kernel import Kernel
from tsteno.kernel.kexts.log import LogLevel

kernel = Kernel()

eval = kernel.get_kext('eval')

while True:
    code = input('> ')
    print(eval.evaluate_code(code))

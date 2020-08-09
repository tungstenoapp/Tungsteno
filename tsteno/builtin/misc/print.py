from tsteno.atoms.module import Module, ModuleArg, ARG_FLAG_ALL_NEXT


class Print(Module):

    def run(self, *arguments):
        output = self.get_kernel().get_kext('output')
        output.write(*arguments)

    def get_arguments(self):
        return [
            ModuleArg(ARG_FLAG_ALL_NEXT)
        ]

    def run_test(self, test):
        pass

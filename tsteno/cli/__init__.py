import click
from sys import platform

if platform == "linux" or platform == "linux2":
    import readline
from sympy import mathematica_code as mcode
from tsteno import VERSION, CODENAME, COPYRIGHT
from tsteno.kernel.kernel import Kernel
from tsteno.kernel.kexts.log import LogLevel
from tsteno.gui import init_gui
from tsteno.notebook import Notebook


@click.command()
@click.option('--debug', '-d', is_flag=True, help='Initialize tsteno kernel in debug mode')
@click.option('--gui', '-g', is_flag=True, help='GUI mode (BETA)')
@click.option('--input', '-i', 'input_', help="*.nb file for input")
def main(debug, gui, input_):
    kernel_opts = {}
    if debug:
        kernel_opts = {
            'kext_extensions': {
                'log': {
                    'log_level': LogLevel.DEBUG
                }
            }
        }

    kernel = Kernel(options=kernel_opts)
    evaluation = kernel.get_kext('eval')

    if gui:
        init_gui(kernel, input_)
    elif input is not None:
        nb_file = open(input_, 'r')
        eval_result = evaluation.evaluate_code(nb_file.read())

        output = kernel.get_kext('output')

        output.register_output_handler(cli_printer)

        if isinstance(eval_result, Notebook):
            eval_result.cli(evaluation)

        nb_file.close()
    else:
        cli(kernel)


k = 0


def cli_printer(obj):
    if obj is None or isinstance(obj, Notebook):
        return

    to_print = obj

    if not isinstance(to_print, str):
        to_print = mcode(to_print)

    click.echo("Out[{}]= {}".format(k, to_print))
    # click.echo()


def cli(kernel):
    global k
    # Print header
    click.echo("Tungsteno Language {} ({})".format(VERSION, CODENAME))
    click.echo(COPYRIGHT)

    evaluation = kernel.get_kext('eval')
    output = kernel.get_kext('output')

    output.register_output_handler(cli_printer)

    if platform == "linux" or platform == "linux2":
        readline.parse_and_bind("tab: complete")
        readline.set_completer(evaluation.get_autocompletion)

    click.echo()

    while True:
        to_execute = input("In[{}]:= ".format(k))
        try:
            evaluation.evaluate_code(to_execute)
        except Exception as err:
            click.echo(err)
        k = k + 1

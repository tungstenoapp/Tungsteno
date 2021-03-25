import click
from sys import platform

if platform == "linux" or platform == "linux2":
    import readline
from sympy import mathematica_code as mcode
from tsteno import VERSION, CODENAME, COPYRIGHT
from tsteno.kernel.kernel import Kernel
from tsteno.kernel.kexts.log import LogLevel
from tsteno.gui import init_gui


@click.command()
@click.option('--debug', '-d', is_flag=True,
              help='Initialize tsteno kernel in debug mode')
@click.option('--cli', '-c', is_flag=True, help='CLI mode')
@click.option('--input', '-i', 'input_', help="*.nb file for input")
def main(debug, cli, input_):
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

    if cli:
        run_cli(kernel)
    elif input_ is not None:
        nb_file = open(input_, 'r')
        eval_result = evaluation.evaluate_code(nb_file.read())

        output = kernel.get_kext('output')

        output.register_output_handler(cli_printer)

        nb_file.close()
    else:
        init_gui(kernel, input_)


k = 0


def cli_printer(obj):
    if obj is None:
        return

    to_print = obj

    if not isinstance(to_print, str):
        to_print = mcode(to_print)

    click.echo("Out[{}]= {}".format(k, to_print))
    # click.echo()


def run_cli(kernel):
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

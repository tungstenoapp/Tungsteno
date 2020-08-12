import click
from sys import platform

if platform == "linux" or platform == "linux2":
    import readline
from sympy import mathematica_code as mcode
from tsteno import VERSION, CODENAME, COPYRIGHT
from tsteno.kernel.kernel import Kernel
from tsteno.kernel.kexts.log import LogLevel


@click.command()
@click.option('--debug', '-d', is_flag=True, help='Initialize tsteno kernel in debug mode')
@click.option('--gui', '-g', is_flag=True, help='GUI mode (BETA)')
@click.option('--input', '-i', help="*.nb file for input")
def main(debug, gui, input):
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
        pass
    elif input is not None:
        nb_file = open(input, 'r')

        print(evaluation.evaluate_code(nb_file.read()))
    else:
        cli(kernel)


k = 0


def cli_printer(obj):
    if obj is None:
        return
    click.echo("Out[{}]= {}".format(k, mcode(obj)))
    click.echo()


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
    click.echo()

    while True:
        to_execute = input("In[{}]:= ".format(k))
        click.echo()
        try:
            evaluation.evaluate_code(to_execute)
        except Exception as err:
            click.echo(err)
        k = k + 1

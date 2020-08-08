import click
import readline
from sympy import mathematica_code as mcode
from tsteno import VERSION, CODENAME, COPYRIGHT
from tsteno.kernel.kernel import Kernel
from tsteno.kernel.kexts.log import LogLevel


@click.command()
@click.option('--debug', '-d', is_flag=True, help='Initialize tsteno kernel in debug mode')
@click.option('--gui', '-g', is_flag=True, help='GUI mode (BETA)')
def main(debug, gui):
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

    if gui:
        pass
    else:
        cli(kernel)


def cli(kernel):
    # Print header
    click.echo("Tungsteno Language {} ({})".format(VERSION, CODENAME))
    click.echo(COPYRIGHT)

    evaluation = kernel.get_kext('eval')

    readline.parse_and_bind("tab: complete")
    readline.set_completer(evaluation.get_autocompletion)

    click.echo()
    click.echo()

    k = 0
    while True:
        to_execute = input("In[{}]:= ".format(k))
        click.echo()
        try:
            result = evaluation.evaluate_code(to_execute)
            if result is not None:
                click.echo("Out[{}]= {}".format(k, mcode(result)))
                click.echo()
        except Exception as err:
            click.echo(err)
        k = k + 1

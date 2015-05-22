from importlib import import_module
import sys

import click

from .render import render_graphviz


@click.group()
def cli():
    pass


@cli.command(name='print')
@click.argument('import_name')
@click.option('--output', '-o', type=click.Path(writable=True))
@click.option(
    '--layout', '-l', default='dot',
    type=click.Choice(['neato', 'dot', 'twopi', 'circo', 'fdp', 'nop'])
)
def print_(import_name, output, layout):
    output = output or 'sm-' + import_name + '.pdf'

    mod_name, obj_name = import_name.rsplit('.', 1)

    sys.path.append('.')  # allow import of modules in current path
    mod = import_module(mod_name)
    sm = getattr(mod, obj_name)

    gvz = render_graphviz(sm)
    gvz.layout(layout)
    gvz.draw(output)

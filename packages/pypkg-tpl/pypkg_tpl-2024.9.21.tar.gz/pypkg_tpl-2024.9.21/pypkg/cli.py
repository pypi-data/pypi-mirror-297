import click

@click.command()
def cli():
    from pypkg.main import PKG
    from youqu3.init import print_tree
    pkg = PKG()
    pkg.dirs()
    pkg.file()
    print_tree()
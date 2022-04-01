import click


@click.group()
def cli():
    ...


@cli.command()
def build():
    """Build website"""
    ...


if __name__ == "__main__":
    cli()

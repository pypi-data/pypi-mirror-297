import click
from portableenv.env_manager import create_env_with_embedded_python

@click.command()
@click.argument('env_name')
def main(env_name):
    """Create a virtual environment with the given name using embedded Python."""
    create_env_with_embedded_python(env_name)

if __name__ == "__main__":
    main()
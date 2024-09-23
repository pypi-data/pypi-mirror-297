import click
import git
import shutil
import os

REPO_URL = "https://github.com/John-sys/django_vue_scaffold.git"

@click.group()
def cli():
    pass

@cli.command()
@click.argument('target_dir')
@click.option('--force', is_flag=True, help='Force clone into non-empty directory')
def install(target_dir, force):
    """Clone the predefined project template to a specified directory."""
    if os.path.exists(target_dir) and os.listdir(target_dir):
        if force:
            click.echo(f"Removing existing contents of {target_dir}")
            shutil.rmtree(target_dir)
        else:
            click.echo(f"Error: {target_dir} is not empty. Use --force to overwrite.")
            return

    try:
        git.Repo.clone_from(REPO_URL, target_dir)
        click.echo(f"Successfully cloned template to {target_dir}")
    except git.GitCommandError as e:
        click.echo(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    cli()

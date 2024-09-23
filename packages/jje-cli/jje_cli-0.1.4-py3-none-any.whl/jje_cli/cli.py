import click
import git
import shutil
import os

REPO_URL = "https://github.com/John-sys/django_vue_scaffold.git"

@click.group()
def cli():
    pass

def remove_contents(directory):
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.unlink(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

@cli.command()
@click.argument('target_dir')
@click.option('--force', is_flag=True, help='Force clone into non-empty directory')
def install(target_dir, force):
    if os.path.exists(target_dir) and os.listdir(target_dir):
        if force:
            click.echo(f"Removing existing contents of {target_dir}")
            remove_contents(target_dir)
        else:
            click.echo(f"Error: {target_dir} is not empty. Use --force to overwrite.")
            return

    try:
        git.Repo.clone_from(REPO_URL, target_dir, depth=1)
        click.echo(f"Successfully cloned template to {target_dir}")
    except git.GitCommandError as e:
        click.echo(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    cli()

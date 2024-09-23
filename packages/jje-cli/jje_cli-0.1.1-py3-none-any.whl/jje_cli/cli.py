import click
import git


REPO_URL = 'https://github.com/John-sys/django_vue_scaffold.git'

@click.group()
def cli():
    pass

# for cloning the django vuejs project scaffold repo from github
@cli.command()
@click.argument('target_dir')
def install(target_dir):
    try:
        git.Repo.clone_from(REPO_URL, target_dir)
        click.echo(f'Successfully created a Django-Vuejs project scaffold in {target_dir}')
    except git.GitCommandError as e:
        click.echo(f'Error: {e}')



if __name__ == '__main__':
    cli()

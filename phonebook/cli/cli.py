import click

from phonebook.data_operations.local_files.local_files import LocalFiles


@click.group()
def cli():
    pass


@cli.command('save')
@click.argument('phone')
@click.argument('name')
@click.option('-p', '--path')
def save(phone, name, path):
    lf = LocalFiles() if path is None else LocalFiles(path)
    lf.save_phone(phone, name)


@cli.command('delete')
@click.argument('name')
@click.option('-p', '--path')
def delete(name, path):
    lf = LocalFiles() if path is None else LocalFiles(path)
    lf.delete_phone_by_name(name)


@cli.command('search')
@click.argument('name')
@click.option('-p', '--path')
def search(name, path):
    lf = LocalFiles() if path is None else LocalFiles(path)
    click.echo('Запись найдена!') if lf.search_by_name(name)\
        else click.echo('Такой записи еще нет(')


if __name__ == '__main__':
    cli()

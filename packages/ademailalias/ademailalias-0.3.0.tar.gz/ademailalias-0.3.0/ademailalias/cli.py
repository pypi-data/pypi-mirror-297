import sys
import click
from ademailalias.aliaser import Aliaser, check_config


@click.group()
@click.argument("account", type=str)
@click.pass_context
def account(ctx, account):
    ctx.ensure_object(dict)
    try:
        aliaser = Aliaser(account)
    except KeyError:
        tokens, aliases = check_config()
        available = sorted(tokens.keys())
        click.secho(f"{account=} must be one of {available}", fg="red")
        sys.exit(1)
    ctx.obj["aliaser"] = aliaser


@account.command()
@click.argument("alias", type=str)
@click.option("-a", "--annotation", type=str, default=None)
@click.pass_context
def create(ctx, alias, annotation):
    aliaser = ctx.obj["aliaser"]
    aliaser.create(alias, annotation=annotation)


@account.command()
@click.pass_context
def list(ctx):
    aliaser = ctx.obj["aliaser"]
    aliases = sorted(aliaser.aliases.items())
    if not aliases:
        click.secho(f"no alias defined for '{aliaser.name}'", fg="blue")
        sys.exit(0)
    click.secho(f"alias defined for account '{aliaser.name}':", fg="blue")
    for alias, data in aliases:
        email = click.style(f"{alias}@{aliaser.domain}", bg="blue", fg="black")
        click.echo(
            f" * {alias}: {email} \"{data['annotation'].replace('EmailAlias - ', '')}\""
        )


@account.command()
@click.argument("alias", type=str)
@click.pass_context
def delete(ctx, alias):
    aliaser = ctx.obj["aliaser"]
    try:
        aliaser.delete(alias)
    except KeyError:
        msg = f"{alias=} does not exis. Existing = {sorted(aliaser.aliases.keys())}"
        click.secho(msg, fg="red")
        sys.exit(1)

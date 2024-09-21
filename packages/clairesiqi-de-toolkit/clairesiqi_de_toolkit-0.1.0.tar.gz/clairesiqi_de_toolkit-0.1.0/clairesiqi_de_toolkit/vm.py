# vm.py

import click
import subprocess

@click.command()
def start():
    """Start your VM"""
    try:
        # Replace 'vagrant up' with the command you use to start your VM
        subprocess.run(['vagrant', 'up'], check=True)
        click.echo("VM has been started.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to start the VM: {e}")

@click.command()
def stop():
    """Stop your VM"""
    try:
        # Replace 'vagrant halt' with the appropriate command for stopping your VM
        subprocess.run(['vagrant', 'halt'], check=True)
        click.echo("VM has been stopped.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to stop the VM: {e}")

@click.command()
def connect():
    """Connect to your VM in VSCode inside your ~/code/clairesiqi/folder"""
    try:
        # Replace the URI with your SSH or remote setup
        subprocess.run(['code', '--folder-uri', 'vscode-remote://ssh-remote+vm/~/code/clairesiqi'], check=True)
        click.echo("Connected to your VM in VSCode.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to connect to the VM in VSCode: {e}")

@click.group()
def cli():
    """CLI tool to manage VM (start, stop, connect)"""
    pass

# Add commands to the CLI group
cli.add_command(start)
cli.add_command(stop)
cli.add_command(connect)

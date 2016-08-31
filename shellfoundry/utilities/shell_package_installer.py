import os
import click
from cloudshell.rest.exceptions import ShellNotFoundException

from shellfoundry.utilities.config_reader import CloudShellConfigReader
from shellfoundry.utilities.shell_package_helper import ShellPackageHelper
from cloudshell.rest.api import CloudShellRestApiClient


class ShellPackageInstaller(object):
    def __init__(self):
        self.cloudshell_config_reader = CloudShellConfigReader()

    def install(self, path):
        shell_filename = ShellPackageHelper.get_shell_name(path) + '.zip'
        package_full_path = os.path.join(path, 'dist', shell_filename)

        cloudshell_config = self.cloudshell_config_reader.read()

        click.echo('Connecting to CloudShell {0}'.format(cloudshell_config.host))

        client = CloudShellRestApiClient(ip=cloudshell_config.host,
                                         username=cloudshell_config.username,
                                         port=cloudshell_config.port,
                                         domain=cloudshell_config.domain,
                                         password=cloudshell_config.password)

        try:
            click.echo('Updating shell {0}'.format(package_full_path))
            client.update_shell(package_full_path)
        except ShellNotFoundException:
            click.echo('Shell not found, adding shell {0}'.format(package_full_path))
            client.add_shell(package_full_path)
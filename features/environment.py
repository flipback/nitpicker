import os
import shutil
from click.testing import CliRunner
import nitpicker.nitpicker
from nitpicker.vcs.vcs_factory import VCSFactory
from unittest.mock import Mock


class MockFactory(VCSFactory):
    def __init__(self, mock_adapter):
        self.__mock_adapter = mock_adapter

    def create_cvs_adapter(self, vcs='git'):
        return self.__mock_adapter


def before_scenario(context, _):
    context.mock_adapter = Mock()
    context.mock_adapter.get_user_email.return_value = "mrhankey@gmail.com"
    context.mock_adapter.get_user_name.return_value = "Mr. Hankey"
    nitpicker.nitpicker.__vcs_factory__ = MockFactory(context.mock_adapter)

    context.test_dir = 'test_qa'
    context.runner = CliRunner()
    context.command = ['-d', context.test_dir, '--no-editor',
                       '--report-dir', context.test_dir,
                       '--vcs', 'mock_cvs',
                       ]


def after_scenario(context, _):
    if os.path.exists(context.test_dir):
        shutil.rmtree(context.test_dir)

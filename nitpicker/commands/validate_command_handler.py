import yaml
import os
import click
import datetime
from schema import Schema, And, Or, Use, Optional, SchemaError

class ValidateCommandHandler:
    """
    Implements 'validate' command
    """

    def __init__(self, qa_dir):
        """
        :param qa_dir: The QA dir where it searches runs
        """
        self.__qa_dir = qa_dir
        self.__schema = Schema(
            {
                'created': And(datetime.datetime),
                'author': And(str),
                'email': And(str),
                'description': Or(None, str),
                Optional('tags'): Or(None, And(Use(str), lambda s: len(s) >= 0)),
                'setup': And(list),
                'steps': And(Use(list), lambda steps: all('=>' in s for s in steps), error='Steps should be array of string '
                                                                                      'and contain "=>" to separate'
                                                                                      'actions and expectations'),
                'teardown': And(list)
            }
        )

    def validate(self):
        """
        Validate format of all the test cases in QA directory
        """

        for qa_dir, dirs, files in os.walk(self.__qa_dir):
            test_cases = (f for f in files if '.yml' in f)
            for test_case in test_cases:
                try:
                    self.__validate_case(os.path.join(qa_dir, test_case))
                except SchemaError as e:
                    click.secho('Test case {} is not valid: {}'.format(test_case, e), fg='red')
                    return False

        return True

    def __validate_case(self, filepath):
        with open(filepath) as f:
            data = yaml.load(f)
            self.__schema.validate(data)


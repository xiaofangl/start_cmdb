#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import os
from collections import namedtuple

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.playbook.play import Play
import ansible.constants as C
from ansible.utils.display import Display

from .callback import AdHocResultCallback, PlaybookResultCallBack, \
    CommandResultCallback
# from common.utils import get_logger
from .exceptions import AnsibleError
from my_ops.lib.utils import get_logger

C.HOST_KEY_CHECKING = False
logger = get_logger(__name__)


class CustomDisplay(Display):
    def display(self, msg, color=None, stderr=False, screen_only=False, log_only=False):
        pass


display = CustomDisplay()

Options = namedtuple('Options', [
    'listtags', 'listtasks', 'listhosts', 'syntax', 'connection',
    'module_path', 'forks', 'remote_user', 'private_key_file', 'timeout',
    'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
    'scp_extra_args', 'become', 'become_method', 'become_user',
    'verbosity', 'check', 'extra_vars', 'playbook_path', 'passwords',
    'diff', 'gathering', 'remote_tmp',
])


def get_default_options():
    options = Options(
        listtags=False,
        listtasks=False,
        listhosts=False,
        syntax=False,
        timeout=60,
        connection='ssh',
        module_path='',
        forks=10,
        remote_user='root',
        private_key_file=None,
        ssh_common_args="",
        ssh_extra_args="",
        sftp_extra_args="",
        scp_extra_args="",
        become=None,
        become_method=None,
        become_user=None,
        verbosity=None,
        extra_vars=[],
        check=False,
        playbook_path='/etc/ansible/',
        passwords=None,
        diff=False,
        gathering='implicit',
        remote_tmp='/tmp/.ansible'
    )
    return options


class PlayBookRunner(object):
    """
    用于执行AnsiblePlaybook的接口.简化Playbook对象的使用.
    """

    # Default results callback
    results_callback_class = PlaybookResultCallBack
    loader_class = DataLoader
    variable_manager_class = VariableManager
    options = get_default_options()

    def __init__(self, inventory=None, options=None):
        """
        :param options: Ansible options like ansible.cfg
        :param inventory: Ansible inventory
        """
        if options:
            self.options = options
        C.RETRY_FILES_ENABLED = False
        self.inventory = inventory
        self.loader = self.loader_class()
        self.results_callback = self.results_callback_class()
        self.playbook_path = options.playbook_path
        self.variable_manager = self.variable_manager_class(
            loader=self.loader, inventory=self.inventory
        )
        self.passwords = options.passwords
        self.__check()

    def __check(self):
        if self.options.playbook_path is None or \
                not os.path.exists(self.options.playbook_path):
            raise AnsibleError(
                "Not Found the playbook file: {}.".format(self.options.playbook_path)
            )
        if not self.inventory.list_hosts('all'):
            raise AnsibleError('Inventory is empty')

    def run(self):
        executor = PlaybookExecutor(
            playbooks=[self.playbook_path],
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            passwords=self.passwords
        )

        if executor._tqm:
            executor._tqm._stdout_callback = self.results_callback
        executor.run()
        executor._tqm.cleanup()
        return self.results_callback.output


class AdHocRunner(object):
    """
    ADHoc Runner接口
    """
    results_callback_class = AdHocResultCallback()
    loader_class = DataLoader
    variable_manager_class = VariableManager
    default_options = get_default_options()

    def __init__(self, inventory, options=None, gather_facts='no'):
        self.options = self.update_options(options)
        self.inventory = inventory
        self.loader = DataLoader()
        self.gather_facts = gather_facts
        self.results_callback = AdHocRunner.results_callback_class
        # self.results_callback = AdHocResultCallback
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory
        )
        self.tasks = []
        self.play_source = None
        self.play = None
        self.runner = None

    def get_result_callback(self):
        return self.__class__.results_callback_class()

    @staticmethod
    def check_module_args(module_name, module_args=''):
        if module_name in C.MODULE_REQUIRE_ARGS and not module_args:
            err = "No argument passed to '%s' module." % module_name
            raise AnsibleError(err)

    def check_pattern(self, pattern):
        if not pattern:
            raise AnsibleError("Pattern `{}` is not valid!".format(pattern))
        if not self.inventory.list_hosts("all"):
            raise AnsibleError("Inventory is empty.")
        if not self.inventory.list_hosts(pattern):
            raise AnsibleError(
                "pattern: %s  dose not match any hosts." % pattern
            )

    def clean_tasks(self, tasks):
        cleaned_tasks = []
        for task in tasks:
            self.check_module_args(task['action']['module'], task['action'].get('args'))
            cleaned_tasks.append(task)
        return cleaned_tasks

    def update_options(self, options):
        if options and isinstance(options, dict):
            options = self.__class__.default_options._replace(**options)
        else:
            options = self.__class__.default_options
        return options

    def run(self, task_tuple, pattern, play_name='Ansible Ad-hoc', gather_facts='no', file_obj=None):
        """
        :param tasks: [{'action': {'module': 'shell', 'args': 'ls'}, ...}, ]
        :param task_tuple:  (('shell', 'ls'), ('ping', ''))
        :param pattern: all, *, or others
        :param play_name: The play name
        :param gather_facts:
        :param file_obj: logging to file_obj
        :return:
        """
        # print task_tuple

        for module, args in task_tuple:
            # print module, args
            # if not self.check_module_args(module, args):
            #     print 'not?'
            #     return
            # print 'this'
            self.tasks.append(
                dict(action=dict(
                    module=module,
                    args=args,
                ))
            )
        print 20 * '0'
        # print 'tasks', tasks
        self.check_pattern(pattern)
        # cleaned_tasks = self.tasks

        self.play_source = dict(
            name=play_name,
            hosts=pattern,
            gather_facts='no',
            tasks=self.tasks
        )
        # print self.tasks
        self.play = Play().load(
            self.play_source,
            variable_manager=self.variable_manager,
            loader=self.loader,
        )

        self.runner = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.options,
            stdout_callback=self.results_callback,
            passwords=self.options.passwords,
        )
        print("Get matched hosts: {}".format(
            self.inventory.get_matched_hosts(pattern)
        ))

        try:
            self.runner.run(self.play)
            print 'this.runner.run...'
            # print self.results_callback.result_q
            return self.results_callback.result_q
            # AdHocResultCallback.gather_result()
        except Exception as e:
            raise AnsibleError(e)
        # else:
        #     return self.results_callback.result_q
        # finally:
        #     if self.runner:
        #         self.runner.cleanup()
        #     if self.loader:
        #         self.loader.cleanup_all_tmp_files()

    def clean_result(self):
        """
        :return: {
            "success": ['hostname',],
            "failed": [('hostname', 'msg'), {}],
        }
        """
        result = {'success': [], 'failed': []}
        for host in self.results_callback.result_q['contacted']:
            result['success'].append(host)

        for host, msgs in self.results_callback.result_q['dark'].items():
            msg = '\n'.join(['{} {}: {}'.format(
                msg.get('module_stdout', ''),
                msg.get('invocation', {}).get('module_name'),
                msg.get('msg', '')) for msg in msgs])
            result['failed'].append((host, msg))
        return result


class CommandRunner(AdHocRunner):
    results_callback_class = CommandResultCallback
    modules_choices = ('shell', 'raw', 'command', 'script')

    def execute(self, cmd, pattern, module=None):
        if module and module not in self.modules_choices:
            raise AnsibleError("Module should in {}".format(self.modules_choices))
        else:
            module = "shell"

        tasks = [
            {"action": {"module": module, "args": cmd}}
        ]
        hosts = self.inventory.get_hosts(pattern=pattern)
        print 20 * '7'
        print hosts
        name = "Run command {} on {}".format(cmd, ", ".join([host.name for host in hosts]))
        print 'this commandruner...'
        return self.run(tasks, pattern, play_name=name)

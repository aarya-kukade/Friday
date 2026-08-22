"""
FRIDAY AI Operating System

Shell Executor

Routes shell-related commands to the correct shell implementation.
"""

from __future__ import annotations

from apps.api.core.nlu.command import Command

from .base_executor import BaseExecutor

from .shell.python import python_shell
from .shell.git import git_shell
from .shell.npm import npm_shell
from .shell.cmd import cmd
from .shell.powershell import powershell


class ShellExecutor(BaseExecutor):

    def __init__(self):

        self.python = python_shell

        self.git = git_shell

        self.npm = npm_shell

        self.cmd = cmd

        self.powershell = powershell

    # ----------------------------------------------------------

    def execute(
        self,
        command: Command,
    ):

        intent = command.intent

        if intent.startswith("python_"):

            return self._python(command)

        if intent.startswith("git_"):

            return self._git(command)

        if intent.startswith("npm_"):

            return self._npm(command)

        if intent.startswith("cmd_"):

            return self._cmd(command)

        if intent.startswith("powershell_"):

            return self._powershell(command)

        return False

    # ==========================================================
    # Python
    # ==========================================================

    def _python(
        self,
        command: Command,
    ):

        match command.intent:

            case "python_run":

                return self.python.script(command.target)

            case "python_module":

                return self.python.module(command.target)

            case "python_install":

                return self.python.pip_install(command.target)

            case "python_uninstall":

                return self.python.pip_uninstall(command.target)

            case "python_upgrade":

                return self.python.pip_upgrade(command.target)

            case "python_venv":

                return self.python.create_venv(command.target)

            case "python_requirements":

                return self.python.install_requirements(command.target)

            case "python_uvicorn":

                return self.python.uvicorn(command.target)

        return False

    # ==========================================================
    # Git
    # ==========================================================

    def _git(
        self,
        command: Command,
    ):

        match command.intent:

            case "git_status":

                return self.git.status()

            case "git_pull":

                return self.git.pull()

            case "git_push":

                return self.git.push()

            case "git_fetch":

                return self.git.fetch()

            case "git_add":

                return self.git.add(command.target)

            case "git_commit":

                return self.git.commit(command.target)

            case "git_clone":

                return self.git.clone(command.target)

            case "git_checkout":

                return self.git.checkout(command.target)

            case "git_branch":

                return self.git.create_branch(command.target)

        return False

    # ==========================================================
    # NPM
    # ==========================================================

    def _npm(
        self,
        command: Command,
    ):

        match command.intent:

            case "npm_install":

                return self.npm.install(command.target)

            case "npm_uninstall":

                return self.npm.uninstall(command.target)

            case "npm_update":

                return self.npm.update(command.target)

            case "npm_start":

                return self.npm.start()

            case "npm_dev":

                return self.npm.dev()

            case "npm_build":

                return self.npm.build()

            case "npm_test":

                return self.npm.test()

        return False

    # ==========================================================
    # CMD
    # ==========================================================

    def _cmd(
        self,
        command: Command,
    ):

        match command.intent:

            case "cmd_dir":

                return self.cmd.dir()

            case "cmd_tree":

                return self.cmd.tree()

            case "cmd_pwd":

                return self.cmd.pwd()

            case "cmd_mkdir":

                return self.cmd.mkdir(command.target)

            case "cmd_delete":

                return self.cmd.delete(command.target)

            case "cmd_copy":

                return self.cmd.copy(

                    command.arguments["source"],

                    command.arguments["destination"],

                )

            case "cmd_move":

                return self.cmd.move(

                    command.arguments["source"],

                    command.arguments["destination"],

                )

        return False

    # ==========================================================
    # PowerShell
    # ==========================================================

    def _powershell(
        self,
        command: Command,
    ):

        match command.intent:

            case "powershell_run":

                return self.powershell.run(command.target)

            case "powershell_script":

                return self.powershell.script(command.target)

            case "powershell_processes":

                return self.powershell.get_processes()

            case "powershell_services":

                return self.powershell.get_services()

        return False


shell_executor = ShellExecutor()
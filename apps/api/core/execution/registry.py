"""
Executor Registry

Stores every executor used by FRIDAY.
"""
from apps.api.core.execution.app_executor import app_executor
from apps.api.core.execution.browser_executor import browser_executor
from apps.api.core.execution.file_executor import file_executor
from apps.api.core.execution.shell_executor import shell_executor
from apps.api.core.execution.system_executor import system_executor
from __future__ import annotations

from typing import Dict, Optional


class ExecutorRegistry:

    def __init__(self):

        self._executors: Dict[str, object] = {}

    def register(
        self,
        intent: str,
        executor: object,
    ) -> None:

        self._executors[intent] = executor

    def get(
        self,
        intent: str,
    ) -> Optional[object]:

        return self._executors.get(intent)

    def unregister(
        self,
        intent: str,
    ):

        self._executors.pop(intent, None)

    def intents(self):

        return tuple(self._executors.keys())


registry = ExecutorRegistry()
# =====================================================
# Application Executor
# =====================================================

registry.register(
    "open",
    app_executor,
)

registry.register(
    "close",
    app_executor,
)

# =====================================================
# Browser Executor
# =====================================================

registry.register(
    "search",
    browser_executor,
)

registry.register(
    "open_url",
    browser_executor,
)

# =====================================================
# File Executor
# =====================================================

registry.register(
    "create",
    file_executor,
)

registry.register(
    "write",
    file_executor,
)

registry.register(
    "read",
    file_executor,
)

registry.register(
    "delete",
    file_executor,
)

registry.register(
    "rename",
    file_executor,
)

registry.register(
    "move",
    file_executor,
)

registry.register(
    "copy",
    file_executor,
)

registry.register(
    "open_folder",
    file_executor,
)

# =====================================================
# Shell Executor
# =====================================================

registry.register("python_run", shell_executor)
registry.register("python_module", shell_executor)
registry.register("python_install", shell_executor)
registry.register("python_uninstall", shell_executor)
registry.register("python_upgrade", shell_executor)
registry.register("python_venv", shell_executor)
registry.register("python_requirements", shell_executor)
registry.register("python_uvicorn", shell_executor)

registry.register("git_status", shell_executor)
registry.register("git_pull", shell_executor)
registry.register("git_push", shell_executor)
registry.register("git_fetch", shell_executor)
registry.register("git_add", shell_executor)
registry.register("git_commit", shell_executor)
registry.register("git_clone", shell_executor)
registry.register("git_checkout", shell_executor)
registry.register("git_branch", shell_executor)

registry.register("npm_install", shell_executor)
registry.register("npm_uninstall", shell_executor)
registry.register("npm_update", shell_executor)
registry.register("npm_start", shell_executor)
registry.register("npm_dev", shell_executor)
registry.register("npm_build", shell_executor)
registry.register("npm_test", shell_executor)

registry.register("cmd_dir", shell_executor)
registry.register("cmd_tree", shell_executor)
registry.register("cmd_pwd", shell_executor)
registry.register("cmd_mkdir", shell_executor)
registry.register("cmd_delete", shell_executor)
registry.register("cmd_copy", shell_executor)
registry.register("cmd_move", shell_executor)

registry.register("powershell_run", shell_executor)
registry.register("powershell_script", shell_executor)
registry.register("powershell_processes", shell_executor)
registry.register("powershell_services", shell_executor)

registry.register(
    "system_lock",
    system_executor,
)

registry.register(
    "system_sleep",
    system_executor,
)

registry.register(
    "system_restart",
    system_executor,
)

registry.register(
    "system_shutdown",
    system_executor,
)

registry.register(
    "system_logoff",
    system_executor,
)

registry.register(
    "system_settings",
    system_executor,
)

registry.register(
    "system_task_manager",
    system_executor,
)

registry.register(
    "system_control_panel",
    system_executor,
)

registry.register(
    "system_explorer",
    system_executor,
)

registry.register(
    "system_recycle_bin",
    system_executor,
)
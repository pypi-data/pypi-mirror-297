import os
from enum import Enum
from typing import Optional, Tuple

from InquirerPy import inquirer, get_style
from InquirerPy.base.control import Choice
from InquirerPy.enum import INQUIRERPY_POINTER_SEQUENCE as POINTER_CODE

from .connection import Connection
from .stored import proceed_stored, append_to_stored, remove_from_stored
from .tmux import run_in_tmux


def one_time_selection() -> Optional[Connection]:
    """Start an interactive selection

    :return: Selected connection instance
    """
    class _MenuAction(Enum):
        """Enum representation os selected action in menu
        """
        Select = 0
        New = 1
        Delete = 2

    store = proceed_stored()
    menu = inquirer.select(
        message="Select SSH user:",
        qmark="",
        amark=POINTER_CODE,
        cycle=True,
        vi_mode=True,
        mandatory=False,
        show_cursor=False,
        raise_keyboard_interrupt=False,
        long_instruction="new: n, delete: d\nexit: C-c, q",
        keybindings={"skip": [{"key": "q"}, {"key": "c-c"}]},
        choices=[Choice(value=(_MenuAction.Select, i), name=str(_)) for i, _ in enumerate(store)],
        style=get_style({"answermark": "#61afef"}, style_override=False)
    )

    @menu.register_kb("d")
    def _delete_entry(ctx):
        """Process "d" button as Delete action
        """
        ctx.app.exit(result=(_MenuAction.Delete, menu.result_value[1]))

    @menu.register_kb('n')
    def _new_entry(ctx):
        """Process "n" button as New action
        """
        ctx.app.exit(result=(_MenuAction.New,))

    selected: Optional[Tuple[_MenuAction, int]] = menu.execute()
    if not selected:
        raise SystemExit()  # Exit on 'skip' action
    match selected[0]:
        case _MenuAction.New:
            append_to_stored(new_stored_entry())
            return None
        case _MenuAction.Delete:
            if inquirer.confirm(message=f"Delete {store[selected[1]]}?").execute():
                remove_from_stored(selected[1])
                if selected[1] == 0:
                    raise SystemExit(f"{store[selected[1]]} was last entry")
            return None
        case _MenuAction.Select:
            return store[selected[1]]


def new_stored_entry() -> Connection:
    """Step-by-step creating new stored info

    :return: Recently created connection instance
    """

    def _inquirer_wrapper_input(message: str, **kwargs):
        """Pre-configured :inquirer.text with provided placeholder
        Additional arguments would be passed as kwargs

        :return: Answer to text input
        """
        return inquirer.text(
            message=message,
            mandatory=True,
            amark=POINTER_CODE,
            validate=lambda self: len(self) > 0,
            long_instruction="exit: C-c",
            **kwargs
        ).execute()

    return Connection(
        hostname=_inquirer_wrapper_input("Hostname", instruction="(eg. google.com):"),
        remote_user=_inquirer_wrapper_input("Remote user:"),
        named_passwd=_inquirer_wrapper_input("Environment variable suffix", instruction="(eg. server in server_user):"),
    )


def open_ssh() -> None:
    """Start an SSH connection
    Checks whenever runs inside TMUX session, then proceeds further handling in `run_in_tmux`

    :return: No.
    """
    connection = one_time_selection()
    if not connection:
        return open_ssh()
    if os.environ.get(connection.env_passwd()):
        if os.environ.get("TMUX"):
            run_in_tmux(connection)
        else:
            os.system(connection.sshpass())
    else:
        print(f"${connection.env_passwd()} is empty!")

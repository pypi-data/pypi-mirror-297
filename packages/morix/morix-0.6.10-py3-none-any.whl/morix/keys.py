from prompt_toolkit.key_binding import KeyBindings
from .settings import config

bindings = KeyBindings()

@bindings.add('c-c')
def _(event):
    exit()

@bindings.add('c-w')
def _(event):
    # print('\r', end='', flush=True)
    config.is_wait_for_enter = not config.is_wait_for_enter
    # print(f'Value "wait for enter" switched to: {config.wait_for_enter}')


@bindings.add('c-d')
def _(event):
    exit()

@bindings.add('enter')
def _(event):
    buffer = event.current_buffer
    if buffer.validate():
        buffer.validate_and_handle()
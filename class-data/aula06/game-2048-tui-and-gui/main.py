import tui_mode
import gui_mode


if __name__ == '__main__':
    mode = ''
    while mode not in ('tui', 'gui'):
        mode = input('TUI or GUI mode? ').lower()

    if mode == 'tui':
        tui_mode.run()
    else:
        gui_mode.run()

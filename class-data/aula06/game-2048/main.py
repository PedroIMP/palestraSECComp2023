import tui_mode
import gui_mode


if __name__ == '__main__':
    try:
        mode = ''
        while mode not in ('tui', 'gui'):
            mode = input('Do you prefer the TUI or GUI? ').lower()
    except KeyboardInterrupt:
        print('Neither then... Ok. Bye!')
        exit(0)

    if mode == 'tui':
        tui_mode.run()
    else:
        gui_mode.run()

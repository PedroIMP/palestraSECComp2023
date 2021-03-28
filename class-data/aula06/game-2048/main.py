import curses_mode
import pgz_mode


if __name__ == '__main__':
    try:
        mode = ''
        while mode not in ('tui', 'gui'):
            mode = input('Do you prefer the TUI or GUI? ').lower()
    except KeyboardInterrupt:
        print('Neither then... Ok. Bye!')
        exit(0)

    if mode == 'tui':
        curses_mode.run()
    else:
        pgz_mode.run()

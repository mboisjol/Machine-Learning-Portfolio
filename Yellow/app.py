from pyfiglet import Figlet

from cli_reader import cmd_reader


def main():
    f = Figlet(font='slant')
    print(f.renderText('QE Snatch'))
    print("Type \'help\' to get a list of commands and what they do")
    try:
        cmd_reader.start()
    except KeyboardInterrupt:
        print("Exiting...")



if __name__ == '__main__':
    main()

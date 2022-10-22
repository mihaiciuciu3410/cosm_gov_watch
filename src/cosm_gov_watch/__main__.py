import logging

from cli_app.cli import process_command_line

def main():
    logging = process_command_line()
    if logging=='debug':
        logging.basicConfig(level=logging.DEBUG)
    elif logging=='info':
        logging.basicConfig(level=logging.INFO)
    elif logging=='warning':
        logging.basicConfig(level=logging.WARNING)
    elif logging=='error':
        logging.basicConfig(level=logging.ERROR)
    elif logging=='critical':
        logging.basicConfig(level=logging.CRITICAL)


if __name__ == '__main__':
    main()
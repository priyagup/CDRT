import socket
import json, time
import os, sys

socket = socket.socket()
port = int(sys.argv[1])


def update_stats(command, success):
    """Update the STATS dict with info about if executing
    *command* was a *success*."""
    if success:
        STATS[command]['success'] += 1
    else:
        STATS[command]['error'] += 1


def handle_put(key, value):
    """Return a tuple containing True and the message
    to send back to the client."""
    DATA[key] = value
    return True, 'Key [{}] set to [{}]'.format(key, value)


def handle_get(key):
    """Return a tuple containing True if the key exists and the message
    to send back to the client."""
    if key not in DATA:
        return False, 'ERROR: Key [{}] not found'.format(key)
    else:
        return True, DATA[key]


STATS = {
    'PUT': {'success': 0, 'error': 0},
    'GET': {'success': 0, 'error': 0},
}
COMMAND_HANDLERS = {
    'PUT': handle_put,
    'GET': handle_get,
}
DATA = {}


def main():
    socket.bind(('', port))
    print("Socket is created with port %s" % port)
    socket.listen(5)
    print("Listening")
    while True:
        connection, address = socket.accept()
        print("Got Connected with ", address)
        start_time = time.time()
        child_pid = os.fork()
        if child_pid == 0:
            print("Process", address)
            socket.close()
            while True:
                data = connection.recv(2049).decode()
                command, key, value = parse_message(data)
                if command in (
                        'GET',
                        'GETLIST',
                        'INCREMENT',
                        'DELETE'
                ):
                    response = COMMAND_HANDLERS[command](key)
                elif command in (
                        'PUT',
                        'PUTLIST',
                        'APPEND',
                ):
                    response = COMMAND_HANDLERS[command](key, value)
                else:
                    response = (False, 'Unknown command type [{}]'.format(command))
                update_stats(command, response[0])
                connection.sendall('{};{}'.format(response[0], response[1]))
                if not data:
                    break
            os._exit(0)

        print("child pid is %d" % child_pid)
    c.close()


if __name__ == '__main__':
    main()


def parse_message(data):
    """Return a tuple containing the command, the key, and (optionally) the
    value cast to the appropriate type."""
    command, key, value, value_type = data.strip().split(';')
    if value_type:
        if value_type == 'LIST':
            value = value.split(',')
        elif value_type == 'INT':
            value = int(value)
        else:
            value = str(value)
    else:
        value = None
    return command, key, value



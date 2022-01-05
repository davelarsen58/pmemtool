#!/usr/bin/python3

VERBOSE = 15

from inspect import currentframe, getframeinfo

# Verbosity Constants
V0 = 0  # Verbose Depth 0 AKA Quiet
V1 = 1  # Verbose Depth 1
V2 = 2  # Verbose Depth 2
V3 = 3  # Verbose Depth 3
V4 = 4  # Verbose Depth 4
V5 = 5  # Verbose Depth 5

# Debug Constants
D0 = 10  # Debug Depth 0
D1 = 11  # Debug Depth 1
D2 = 12  # Debug Depth 2
D3 = 13  # Debug Depth 3
D4 = 14  # Debug Depth 4
D5 = 15  # Debug Depth 5

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def unit_test_result(name, status):
    print("%-30s %-10s" % (name, status))

def message(message, level=0, message_type=''):
    """
    emits messages when VERBOSE => 0, when level => VERBOSE
       level controls the indentation as well as gates messages
       on verbosity level
          VERBOSE == False or Verbose == 0, yields not output
          example: if VERBOSE == 3 and level == 3, then message
          levels 0, 1, 2, and 3 are printed
    message_type prefixes message with string provided, with 'INFO'
    as default message type.  Note the trailing ':'
    """
    global VERBOSE
    n_spaces = 0

    '''if message_type is blank, fill in defaults based upon verbosity constants'''
    if not message_type:
        # '''Verbose Range'''
        if level > V0 and level <= V5:
            message_type = 'V' + str(VERBOSE) + ':' + str(level) + ': '
            n_spaces = level
        # '''Debug Range'''
        elif level > D0 and level <= D5:
            message_type = 'D' + str(VERBOSE - 10) + ':' + str(level) + ': '
            n_spaces = level - 10
    else:
        message_type = message_type + '_' + str(VERBOSE) + ':' + str(level) + ': '
        n_spaces = VERBOSE

    if level <= VERBOSE:
        spaces = ''

        for i in range(n_spaces):
            spaces = spaces + '  '
        print("%s%s%s" % (spaces, message_type, message))

def unit_tests():
    status = False

    global VERBOSE
    VERBOSE = V0

    # walk through each value for V0 ... D5
    for v in range(D5):
        print('v = ', v)
        msg = "%s%s" % (get_linenumber(), ": testing get_linenumber()")
        message(msg)

        # i = 0
        for i in range(VERBOSE):
            msg = "%s%s" % (get_linenumber(), ": testing message level")
            message(msg, i)

        # i = 0
        for i in range(VERBOSE):
            msg = "%s%s" % (get_linenumber(), ": testing message level with DEBUG message type")
            message(msg, i, "Hello:")

        # line_number = get_linenumber()
        # i = 0
        for i in range(VERBOSE):
            msg = "%s%s" % (get_linenumber(), ": testing message level with empty message type")
            message(msg, i, "")

        VERBOSE = VERBOSE + 1



def main():
    unit_tests()


if __name__ == "__main__":
    main()


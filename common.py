#!/usr/bin/python3

global VERBOSE
VERBOSE = 0

from inspect import currentframe, getframeinfo

# Verbosity Constants
V0 = 0  # Verbose Depth 0 AKA Quiet
V1 = 1  # Verbose Depth 1
V2 = 2  # Verbose Depth 2
V3 = 3  # Verbose Depth 3
V4 = 4  # Verbose Depth 4
V5 = 5  # Verbose Depth 5

# Debug Constants
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

def message(message, indent=0, message_type='INFO:'):
    """
    emits messages when VERBOSE => 0, when indent => VERBOSE
       indent controls the indentation as well as gates messages
       on verbosity level

          VERBOSE == False or Verbose == 0, yields not output

          example: if VERBOSE == 3 and indent == 3, then message
          levels 0, 1, 2, and 3 are printed

    message_type prefixes message with string provided, with 'INFO'
    as default message type.  Note the trailing ':'
    """
    global VERBOSE

    if indent <= VERBOSE:
        spaces = ''
        for i in range(indent):
            spaces = spaces + '  '
        print("%s%s%s" % (spaces, message_type, message))

def unit_tests():
    status = False

    line_number = get_linenumber()
    msg = "%s%s" % (line_number, ": testing get_linenumber()")
    message(msg)

    line_number = get_linenumber()
    msg = "%s%s" % (line_number, ": testing message indent")
    for i in range(5):
         message(msg, i)

    line_number = get_linenumber()
    msg = "%s%s" % (line_number, ": testing message indent with DEBUG message type")
    for i in range(5):
        message(msg, i, "DEBUG:")

    line_number = get_linenumber()
    msg = "%s%s" % (line_number, ": testing message indent with empty message type")
    for i in range(5):
         message(msg, i, "")



def main():
    unit_tests()


if __name__ == "__main__":
    main()


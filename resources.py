import numpy as np

# CONFIG

# Used size of the ascii table
asciiTableSize = 256


def asciiArray(message):
    # Turns a string into the respective ascii array
    # "ord" turns a char into it's ascii code
    return np.array(list(map(ord, list(message))))


def codeToString(code):
    # Turns an ascii array into the respective string
    # "chr" turns ascii code back into it's character
    return ''.join(list(map(chr, code)))


def content(file):
    # Returns file content as string
    return ''.join(file.readlines())


def displayUsageAndExit(message):
    print(message)
    exit()

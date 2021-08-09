import numpy as np

# CONFIG

# Used size of the ascii table
asciiTableSize = 256
keyAsciiTableSize = 128
minimumKeyAsciiValue = 32
# When looking at the top values for each possible value for a key's character
maxValuesToKeep = 5

# DECRYPTION


def decrypt(cipher, key):
    # Turn cipher into array of ascii codes
    codeCipher = asciiArray(cipher)
#
    # Turn key into array of ascii codes
    # Resize key to match cipher's size
    resizedKey = np.resize(asciiArray(key), len(codeCipher))
#
    # Remove the key, apply mod and convert from ascii back to text
    return codeToString(np.mod(codeCipher - resizedKey, asciiTableSize))


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

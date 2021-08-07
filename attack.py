import numpy as np
import sys

# Import local resources
from resources import *
from main import decrypt

# ATTACK


def getKeySize(cipher):
    return


def getKey(cipher, keySize):
    return


def attack(cipher):
    # 1. Get key size
    keySize = getKeySize(cipher)

    # 2. Use key size to guess the key
    key = getKey(cipher, keySize)

    # 3. Use key to get message
    return decrypt(cipher, key)


# MAIN


# Check that there are enough arguments
# Check that operation type argument is correct
if len(sys.argv) != 2:
    displayUsageAndExit(
        "Por favor, forneca o nome (com extensao) do arquivo a ser atacado.")

outputFileName = "resultado.txt"
cipherFileName = sys.argv[1]


try:
    with open(cipherFileName) as cipherFile:
        with open(outputFileName, "w") as outputFile:
            outputFile.write(
                attack(content(cipherFile))
            )

except IOError:
    print("Erro: verifique que o arquivo fornecido existe")

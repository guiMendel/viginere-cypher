import numpy as np
import sys

# Import local resources
from resources import *

# ENCRYPTION


def encrypt(message, key):
    # Turn message into array of ascii codes
    codeMessage = asciiArray(message)
#
    # Turn key into array of ascii codes
    # Resize key to match message's size
    resizedKey = np.resize(asciiArray(key), len(codeMessage))
#
    # Sum the key, apply mod and convert from ascii back to text
    return codeToString(np.mod(codeMessage + resizedKey, asciiTableSize))

# DECRYPTION


def decrypt(cypher, key):
    # Turn cypher into array of ascii codes
    codeCypher = asciiArray(cypher)
#
    # Turn key into array of ascii codes
    # Resize key to match cypher's size
    resizedKey = np.resize(asciiArray(key), len(codeCypher))
#
    # Remove the key, apply mod and convert from ascii back to text
    return codeToString(np.mod(codeCypher - resizedKey, asciiTableSize))

# MAIN


# Check that there are enough arguments
# Check that operation type argument is correct
if len(sys.argv) != 4 or sys.argv[1] != "-enc" and sys.argv[1] != "-dec":
    displayUsageAndExit("Por favor, forneca o modo de operacao (-enc para cifrar, -dec para decifrar), seguido pelo nome do arquivo (com extensao) com o texto a ser cifrado/decifrado, seguido pelo nome do arquivo (com extensao) contendo a chave.")

operation = encrypt if sys.argv[1] == "-enc" else decrypt
outputFileName = "cifra.txt" if sys.argv[1] == "-enc" else "mensagem.txt"
textFileName = sys.argv[2]
keyFileName = sys.argv[3]


try:
    with open(textFileName) as textFile:
        with open(keyFileName) as keyFile:
            with open(outputFileName, "w") as outputFile:
                outputFile.write(
                    operation(content(textFile), content(keyFile))
                )

except IOError:
    print("Erro: verifique que ambos os arquivos fornecidos existem")

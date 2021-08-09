from unidecode import unidecode as removeAccents
from functools import reduce
import sys
from pprint import pprint

# Import local resources
from resources import *
from letterDistribution import *

# TEM QUE FAZER PRA INGLES TAMBEM
# ATTACK


def countOccurrences(startIndex, limitIndex, step, container):
    # Returns a dictionary with each character of the container mapped to its' occurrence count
    counter = {}

    # Count every (step)th character
    for i in range(startIndex, limitIndex, step):
        # Get corresponding character
        character = container[i]
        # Count it
        try:
            counter[character] += 1
        except KeyError:
            counter[character] = 1

    return counter


def getKeySize(cipher):
    # Get ascii codes from text
    codeCipher = asciiArray(cipher)

    # Cipher size
    cipherSize = len(codeCipher)

    # Will hold the maximum sum of frequencies so far
    maxSum = 0

    # Try all possible sizes of k
    for keySize in range(1, cipherSize//10):
        # Count every (keySize)th character
        counter = countOccurrences(0, cipherSize, keySize, cipher)

        # Compute the sum of the squares, and divide by the square of elements count
        frequenciesSum = sum(
            count * count for count in counter.values()) / ((cipherSize / keySize) ** 2)

        # print(f'Size {keySize}: {frequenciesSum}')

        # If this is much higher than usual, it's the correct size
        if maxSum > 0 and frequenciesSum >= 2.5 * maxSum:
            return keySize

        # If not, store it if it's higher
        elif frequenciesSum > maxSum:
            maxSum = frequenciesSum

    # If none of the sizes fit, the algorithm failed
    return None


def getCharacterStreams(cipher, keySize):
    # For each character i of the key with size n, get it's i-stream: a string composed of every nth character of the cipher, starting with the ith character
    iStreams = []

    # Size of cipher
    cipherSize = len(cipher)

    for i in range(keySize):
        # Get every nth character of the cipher, starting at i
        iStreamArray = [cipher[index]
                        for index in range(i, cipherSize, keySize)]

        # Turn into a string
        iStream = ''.join(iStreamArray)

        # Append it
        iStreams.append(iStream)

    # Return the array of tuples
    return iStreams


def keepLeastDistant(characterDistances, newItem, maxValues):
    # Adds the new item but trims the characterDistances array to only have the maxValues closest items

    # If the new item is farther than the last item in the array, disregard it
    if len(characterDistances) == maxValues and newItem[1] >= characterDistances[-1][1]:
        return characterDistances

    # Add it and sort the array based on distance
    characterDistances.append(newItem)

    characterDistances.sort(
        key=lambda character: character[1])

    # Disregard the last item if list big enough
    if len(characterDistances) > maxValues:
        characterDistances.pop()

    return characterDistances


def getFrequency(letter):
    # Returns the letter frequency. If it's not in the dict, returns 0
    try:
        return distributionEN[letter]
    except KeyError:
        if letter == ' ':
            return 0.08
        return 0


def getKey(cipher, keySize, letterDistribution):

    # Get the sum of each letter's frequency squared (for a later comparison)
    lettersFrequencySum = sum(
        frequency ** 2 for frequency in letterDistribution.values())

    print(f'Base frequency sum : {lettersFrequencySum}')

    # Get the character stream for each character of the key
    characterStreams = getCharacterStreams(cipher, keySize)

    # Will construct the key
    key = ''

    # For each character of the key
    for keyIndex in range(keySize):

        # Get the stream and frequency array
        iStream = characterStreams[keyIndex]

        # Used to tell the fittest ascii code
        characterDistances = []

        # Try every key character possibility
        for characterCode in list(range(minimumKeyAsciiValue, keyAsciiTableSize)) + [32]:
            # Exclude non letter characters
            if 91 <= characterCode <= 96:
                continue

            # Decipher stream and normalize (lower the case and remove accents)
            decipheredStream = removeAccents(
                decrypt(iStream, chr(characterCode)).lower())
            decipheredStreamSize = len(decipheredStream)

            # Count the occurrences of each character in the stream
            counter = countOccurrences(
                0, decipheredStreamSize, 1, decipheredStream)

            # Get the distribution of the stream
            streamDistribution = {
                character: count / decipheredStreamSize for (character, count) in counter.items()}

            # Get the sum of each character's frequency times the character's frequency in the language
            frequencySum = sum(letterDistribution[char] * streamDistribution[char]
                               for char in letterDistribution.keys() if char in streamDistribution.keys())

            # See how far from the original frequency sum this is (the one we calculated earlier for comparison reasons)
            sumDistance = abs(frequencySum - lettersFrequencySum)

            # Store each char with it's distance and stream
            characterDistances = keepLeastDistant(
                characterDistances, (chr(characterCode), sumDistance, decipheredStream), maxValuesToKeep)

        def pickFittest(characterDistances):
            fittest = None

            # For each character in the list
            for charResult in characterDistances:
                # Sum up the frequency of each character in the stream
                sum = reduce(lambda sum, char: sum + getFrequency(char),
                             charResult[2], 0)

                # Save it if it's better
                if fittest == None or sum > fittest[1]:
                    fittest = (charResult, sum)

            return fittest[0][0]

        # Pick the character that results in more frequent characters
        bestCharacterCode = pickFittest(characterDistances)

        # Append the fittest ascii code found
        key += bestCharacterCode

    # Return the constructed key
    return key


def attack(cipher, letterDistribution):
    # 1. Get key size
    keySize = getKeySize(cipher)

    # Check that the algorithm succeeded
    if keySize == None:
        return "Falha em encontrar o tamanho da chave"

    print(f'Key size: {keySize}')

    # 2. Use key size to guess the key
    key = getKey(cipher, keySize, letterDistribution)

    print(f'Key value: {key}')

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
                attack(content(cipherFile), distributionEN)
            )

except IOError:
    print("Erro: verifique que o arquivo fornecido existe")

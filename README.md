# SmartSeed

SmartSeed is a text-based Python program that generates bip-39 seed phrases. The user can choose to generate seed phrases by using a randomiser or by using human-calculable number sequences. Using number sequences allows the user to come up with a formula to generate the seed phrase, making lost keys easily recoverable using the application in combination with the formula.

## Important Security Precautions

Since SmartSeed uses formulas to generate seed phrases, it is essential to use a passphrase when creating a wallet. This adds an aditional layer of security to the generated phrase. When generating private keys, it is recommended to use a machine not connected to the internet. Completely air-gapped devices are the best option for generating private keys.

## How It Works

1. The user selects a method to generate a string of digits.
2. The string of digits is converted to ones and zeros to create a binary string.
3. The binary string is then hashed using sha256 algorithm to find a valid checksum.
4. Both strings are divided into chunks of 11 and displayed on the screen, along with bip-39 word indices and each word represented by each index.
5. The seed phrase is displayed in an easily selectable format to be copied and pasted.

To run the program, open a terminal and navigate to the directory containing SmartSeed. Enter the following command: 

```python smartseed.py```

## License

SmartSeed is licensed under the MIT License. See LICENSE for more information.
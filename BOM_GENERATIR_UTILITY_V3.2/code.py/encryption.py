def encryptor(plain_text):
    encrypted_numbers = []
    shift = 5  # Custom shift value

    for char in plain_text:
        encrypted_char = (ord(char) + shift) ^ shift  # Shift and XOR
        encrypted_numbers.append(str(encrypted_char)) 

    return "-".join(encrypted_numbers)  # Convert numbers into a string


def decryptor(encrypted_data):
    decrypted_text = ""
    shift = 5  # Same shift value used in encryption

    for num in encrypted_data.split("-"):
        decrypted_char = chr((int(num) ^ shift) - shift)  # Reverse XOR and shift
        decrypted_text += decrypted_char 

    return decrypted_text


# Example Usage
plain_text = "HelloWorld123!"
encrypted_text = encryptor(plain_text)
print("Encrypted:", encrypted_text)

decrypted_text = decryptor(encrypted_text)
print("Decrypted:", decrypted_text)  # Should print "HelloWorld123!"

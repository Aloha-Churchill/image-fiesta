
# AES = Advanced Encryption Standard

# Encrypting
def encrypt_file(filename):
    # Read file contents
    with open(filename, 'r') as file_in:
        data = file_in.read()
    file_in.close()

    key = get_random_bytes(16)  # Generate a random key
    # write key to a file called key.txt
    with open('key.txt', 'wb') as file_key:
        file_key.write(key)

    file_key.close()

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))

    # write ciphertext to a file called encrypted.txt
    with open('encrypted.bin', 'wb') as file_out:
        [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
    file_out.close()


def decrypt_file(filename):
    # Read encrypted contents
    with open(filename, 'rb') as file_in:
        nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
    file_in.close()

    # Read key
    with open('key.txt', 'rb') as file_key:
        key = file_key.read()
    file_key.close()

    cipher = AES.new(key, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)

    # write decrypted contents to a file called decrypted.txt
    with open('decrypted.txt', 'wb') as file_out:
        file_out.write(data)
    file_out.close()
    

# put key.txt in same directory

def main():
    choice = input("Encrypt or decrypt? (e/d): ")
    if choice == 'e':
        # Here, you can either hardcode a key, generate one, or ask the user to provide one.
        encrypt_file('card.txt')
    elif choice == 'd':
        decrypt_file('encrypted.bin')

main()
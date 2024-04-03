import base64


def encode():
    with open("encoded_script.py.b64", "rb") as archivo:
        dato = archivo.read()
    archivo_bash = "".join(chr(i + 0x80) for i in range(len(dato))) + "VOID"
    with open("archivo.txt", "wb") as archivo:
        archivo.write(archivo_bash.encode())


if __name__ == "__main__":
    encode()

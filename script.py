import os
from time import sleep
from zipfile import ZipFile
from jsonargparse import ArgumentParser
from cryptutils import encrypt as en
from cryptutils import decrypt as de


def cmd(comando: str):
    return os.system(f"cmd /k {comando}")


def encrypt(file, password: str):
    # TODO aggiungere la possibilità di avere i files in una cartella separata
    try:
        os.mkdir("crypt")
    except:
        pass
    en(file, "crypt/" + file, password)
    return


def decrypt(file, password: str):
    if "/" in file:
        try:
            os.mkdir(file.split("/")[0] + "/decrypt")
        except:
            pass
    else:
        try:
            os.mkdir("decrypt")
        except:
            pass
    if password == None:
        password = ""
    if "/" in file:
        de(file, file.split("/")[0] + "/decrypt/" + os.path.basename(file), password)
    else:
        de(file, "decrypt/" + file, password)

    return


if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("-e")
    args.add_argument("-oe")
    args.add_argument("-d")
    args.add_argument("--files", type=list)
    args.add_argument("--password", type=str)
    args = args.parse_args()
    args = args.as_dict()
    print(args)
    modo = None
    if not args["e"] == None:
        contenitore = args["e"]
        modo = "e"
    elif not args["d"] == None:
        contenitore = args["d"]
        modo = "d"
    elif not args["oe"] == None:
        contenitore = args["oe"]
        modo = "oe"
    else:
        exit("Specificare 'e' o 'd'")

    if modo == "e":
        for f in args["files"]:
            encrypt(f, args["password"])

        with ZipFile("temp.zip", "w") as zipfile:
            for file in os.listdir("crypt/"):
                zipfile.write("crypt/" + file)

        try:
            os.mkdir("joined")
        except:
            pass
        cmd(f"copy /b {contenitore}+temp.zip joined\\{contenitore}")

    if modo == "oe":
        encrypt(args["oe"], args["password"])

    if modo == "d":
        decrypt(args["d"], args["password"])

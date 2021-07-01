import hashlib


# https://stackoverflow.com/a/3431838
def sha256(fname):
    ohash = hashlib.sha256()
    with open(fname, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            ohash.update(chunk)
    return ohash.hexdigest()

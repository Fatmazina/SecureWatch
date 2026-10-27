AUTHORIZED = ['alice_martin', 'bob_dupont']   # load from DB in production
KNOWN_UNAUTHORIZED = ['known_intruder']

def classify(name):
    if name == 'unknown':
        return 'UNKNOWN'         # alarm + capture + notification
    elif name in AUTHORIZED:
        return 'AUTHORIZED'      # log access, watermark image
    elif name in KNOWN_UNAUTHORIZED:
        return 'UNAUTHORIZED'    # alert + watermarked proof
    else:
        return 'UNKNOWN'

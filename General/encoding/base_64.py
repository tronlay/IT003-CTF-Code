import base64

msg = bytes.fromhex("72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf")
msg = base64.b64encode(msg)
print(msg)
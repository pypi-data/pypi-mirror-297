import base58
from .Constants import Constants

def lamport_to_sol(lamports):
    return round(lamports / Constants.LAMPORT_PER_SOL, 9)

def sol_to_lamport(sol):
    return int(sol * Constants.LAMPORT_PER_SOL)

def array_to_base58(address_array):
    if isinstance(address_array, str):
        # Dangerous!
        address_array = eval(address_array)
    x_bytes = bytes(address_array)
    base58_encoded = base58.b58encode(x_bytes)
    return base58_encoded.decode('utf-8')

def base58_to_array(base58_string):
    base58_encoded = base58_string.encode('utf-8')
    decoded = base58.b58decode(base58_encoded)
    return str(list(decoded)).replace(' ', '')


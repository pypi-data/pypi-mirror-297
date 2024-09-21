from spl.token.constants import TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID

class Constants:
    CONVERSION_FACTOR = 9
    LAMPORT_PER_SOL = 10**CONVERSION_FACTOR
    SOL_PER_LAMPORT = 1 / LAMPORT_PER_SOL
    VALID_COMMITMENTS = ["processed", "confirmed", "finalized", "recent", "single", "root", "max"]
    TOKEN_PROGRAM_ID = TOKEN_PROGRAM_ID
    TOKEN_2022_PROGRAM_ID = TOKEN_2022_PROGRAM_ID

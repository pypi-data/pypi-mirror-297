from .Constants import *

def lamport_to_sol(lamports):
    return round(lamports / Constants.LAMPORT_PER_SOL, 9)

def sol_to_lamport(sol):
    return int(sol * Constants.LAMPORT_PER_SOL)


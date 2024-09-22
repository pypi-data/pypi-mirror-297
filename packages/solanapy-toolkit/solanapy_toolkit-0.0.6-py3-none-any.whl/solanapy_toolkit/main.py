from .lib.ClientWrapper import SolanaClient
from .lib.Helpers import *

def cli():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--array', type=str, help="Convert private key array")
    parser.add_argument('--base58', type=str, help="Convert private base58 key")
    args = parser.parse_args()
    if not (args.array or args.base58):
        print("Use --help")
        exit()
    if args.array:
        result = array_to_base58(args.array)
        print(result)
    if args.base58:
        result = base58_to_array(args.base58)
        print(result)

if __name__ == "__main__":
    cli()

import solana
import traceback
import random

from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.signature import Signature
from retry import retry

class SolanaClient:
    def __init__(self, endpoints=[]):
        self.clients = []
        if not endpoints:
            raise ValueError("Endpoint is needed")
        if endpoints:
            for endpoint in endpoints:
                self.clients.append(Client(endpoint))

    @retry(ValueError, delay=2, backoff=2)
    def retryable_get_transaction(self, signature):
        solana_client = random.choice(self.clients)
        if isinstance(signature, str):
            try:
                signature = Signature.from_string(signature)
            except ValueError:
                raise TypeError("Malformed signature")
        try:
            tx = solana_client.get_transaction(signature, max_supported_transaction_version=0)
            return tx
        except solana.exceptions.SolanaRpcException:
            print("Retrying get transaction")
            raise ValueError
        except Exception as E:
            print(f"Failed to get transaction for {signature} ({traceback.format_exc().encode()})")
            raise ValueError

    @retry(ValueError, delay=4, backoff=2)
    def retryable_get_signatures_for_address(self, address, before=None, until=None, limit=1000):
        solana_client = random.choice(self.clients)
        if isinstance(address, str):
            try:
                address = Pubkey.from_string(address)
            except ValueError:
                raise TypeError("Malformed address")
        if isinstance(before, str) and before != None:
            before = Signature.from_string(before)
        if isinstance(until, str) and until != None:
            until = Signature.from_string(until)
        try:
            results = solana_client.get_signatures_for_address(address, before=before, until=until, limit=limit)
            return results
        except solana.exceptions.SolanaRpcException:
            print("Retrying get signatures for address")
            raise ValueError
        except Exception as E:
            print(f"Failed to get transaction for {address} ({traceback.format_exc().encode()})")
            raise ValueError

    @retry(ValueError, delay=4, backoff=2)
    def retryable_get_account_info(self, address, commitment=None):
        solana_client = random.choice(self.clients)
        if isinstance(address, str):
            try:
                address = Pubkey.from_string(address)
            except ValueError:
                raise TypeError("Malformed address")
        try:
            account_info = solana_client.get_account_info(address, commitment=commitment)
            return account_info
        except solana.exceptions.SolanaRpcException:
            print("Retrying get account info")
            raise ValueError
        except Exception as E:
            print(f"Failed to get account info for {address} ({traceback.format_exc().encode()})")
            raise ValueError

    @retry(ValueError, delay=4, backoff=2)
    def retryable_get_account_info_json_parsed(self, address, commitment=None):
        solana_client = random.choice(self.clients)
        if isinstance(address, str):
            try:
                address = Pubkey.from_string(address)
            except ValueError:
                raise TypeError("Malformed address")
        try:
            account_info = solana_client.get_account_info_json_parsed(address, commitment=commitment)
            return account_info
        except solana.exceptions.SolanaRpcException:
            print("Retrying get account info")
            raise ValueError
        except Exception as E:
            print(f"Failed to get account info for {address} ({traceback.format_exc().encode()})")
            raise ValueError



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


    @retry(ValueError, delay=4, backoff=2)
    def retryable_get_token_account_balance(self, address, commitment=None):
        solana_client = random.choice(self.clients)
        if isinstance(address, str):
            try:
                address = Pubkey.from_string(address)
            except ValueError:
                raise TypeError("Malformed address")
        try:
            account_balance = solana_client.get_token_account_balance(address, commitment=commitment)
            return account_balance
        except solana.exceptions.SolanaRpcException:
            print("Retrying get token account balance")
            raise ValueError
        except Exception as E:
            print(f"Failed to get token account balance for {address} ({traceback.format_exc().encode()})")
            raise ValueError

    @retry(ValueError, delay=4, backoff=2)
    def retryable_get_token_accounts_by_owner(self, address, token_account_opts=None, commitment=None):
        solana_client = random.choice(self.clients)
        if isinstance(address, str):
            try:
                address = Pubkey.from_string(address)
            except ValueError:
                raise TypeError("Malformed address")
        try:
            token_accounts = solana_client.get_token_accounts_by_owner(address, opts=token_account_opts, commitment=commitment)
            return token_accounts
        except solana.exceptions.SolanaRpcException:
            print("Retrying get token accounts")
            raise ValueError
        except Exception as E:
            print(f"Failed to get token account for {address} ({traceback.format_exc().encode()})")
            raise ValueError


    @retry(ValueError, delay=4, backoff=2)
    def retryable_get_token_accounts_by_owner_json_parsed(self, address, token_account_opts=None, commitment=None):
        solana_client = random.choice(self.clients)
        if isinstance(address, str):
            try:
                address = Pubkey.from_string(address)
            except ValueError:
                raise TypeError("Malformed address")
        try:
            token_accounts = solana_client.get_token_accounts_by_owner_json_parsed(address, opts=token_account_opts, commitment=commitment)
            return token_accounts
        except solana.exceptions.SolanaRpcException:
            print("Retrying get token accounts")
            raise ValueError
        except Exception as E:
            print(f"Failed to get token account for {address} ({traceback.format_exc().encode()})")
            raise ValueError



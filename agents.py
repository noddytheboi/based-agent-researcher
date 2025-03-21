import json
import os
from decimal import Decimal
from typing import Any, Dict, List, Union
from dotenv import load_dotenv
import requests
from openai import OpenAI
from swarm import Agent
from web3 import Web3
from web3 import eth

load_dotenv()
# Get configuration from environment variables

MORALIS_API_KEY = os.environ.get("MORALIS_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
BASESCAN_API_KEY = os.environ.get("BASESCAN_API_KEY")

# Initializing web3 connection

w3 = Web3(
    Web3.HTTPProvider(
        "https://site1.moralis-nodes.com/base/edfad7446e9e45ef8800fbf4a7ae8a57"
    )
)


def is_eoa(owner_address: str) -> str:
    # Checking if address eoa or contract

    try:
        checker = w3.eth.get_code(w3.to_checksum_address(owner_address))
        convert = w3.to_hex(checker)
        if convert == "0x" or None:
            return "True"
        else:
            return "False"
    except Exception as e:
        return f"Error: {str(e)}"


def wallet_pnl(owner_address: str, days: str = "all") -> str:
    # Checking wallet PnL and trade volume (default timeframe is 'all',you can specify it (7,30,60,90 days)
    # right after agent will do holders retrieve,just ask him to add this to breakdown)
    # More info https://docs.moralis.com/web3-data-api/evm/reference/wallet-api/get-wallet-profitability-summary

    url = f"https://deep-index.moralis.io/api/v2.2/wallets/{owner_address}/profitability/summary"
    headers = {"Accept": "application/json", "X-API-Key": MORALIS_API_KEY}
    params = {
        "chains": "base",
        "days": days,
        "address": owner_address,
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        owner_pnl = response.json()
        if owner_pnl:
            owner_pnl_data = "\n".join(
                [
                    f"Wallet PnL: {owner_pnl['total_realized_profit_usd']}\n"
                    f"Trade Volume: {owner_pnl['total_trade_volume']}\n"
                ]
            )
            return owner_pnl_data
        else:
            return "No wallet pnl"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def wallet_net(owner_address: str) -> str:
    # Checking token owners net_worth or any wallet you want to check
    # More info: https://docs.moralis.com/web3-data-api/evm/reference/wallet-api/get-wallet-net-worth

    url = f"https://deep-index.moralis.io/api/v2.2/wallets/{owner_address}/net-worth"
    headers = {"Accept": "application/json", "X-API-Key": MORALIS_API_KEY}
    params = {
        "chains": ["base"],
        "exclude_spam": True,
        "exclude_unverified_contracts": True,
        "address": owner_address,
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        owner_net_worth = response.json()

        if owner_net_worth:
            return owner_net_worth["total_networth_usd"]
        else:
            return "No holders found"

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def transfer_screener(owner_adress: str) -> str:
    # Checking "out" transactions of given address, its maybe helpful to find any connections between holders when
    # you do token_holders_analysis. Agent could go very deep,checking addresses of receivers of recievers
    # of....etc and compare them with initial holders list for instance.
    # Try your best, he could do much more than you assume.
    # More info: https://docs.basescan.org/api-endpoints/accounts

    url = f"https://api.basescan.org/api?module=account"
    headers = {
        "Accept": "application/json",
    }
    params = {
        "action": "txlist",
        "address": owner_adress,
        "startblock": 0,
        "endblock": 99999999,
        "page": 1,
        "offset": 100,
        "sort": "desc",
        "apikey": BASESCAN_API_KEY,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        status = response.raise_for_status()
        tx_history = response.json()["result"]
        if tx_history:
            tx_history_list = "\n".join(
                [
                    f"Receiver: {entry['to']}\n"
                    for entry in tx_history
                    if is_eoa(entry["to"]) == "True" and owner_adress != entry["to"]
                ]
            )
            return f"{owner_adress} tx_Receivers:\n{tx_history_list}"
        else:
            return "No receivers found."
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def first_buyers(token_address: str) -> str:
    # Checking first token buyers

    url = f"https://deep-index.moralis.io/api/v2.2/erc20/{token_address}/transfers"
    headers = {"Accept": "application/json", "X-API-Key": MORALIS_API_KEY}
    params = {
        "chain": "base",
        "to_block": 99999999,
        "limit": 15,
        "order": "ASC",
        "from_block": 20,
        "address": token_address,
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        tx_data = response.json()["result"]
        if tx_data:
            tx_data_list = "\n".join(
                [
                    f"Smart buyer address: {entry['to_address']}\n"
                    f"Token value: {entry['value_decimal']}\n"
                    for entry in tx_data
                    if is_eoa(entry["to_address"]) == "True"
                ]
            )
            return tx_data_list
        else:
            return "No byers found."
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


def get_token_holders_analysis(token_address: str) -> str:
    # Its a main function,retrieving top holders of token + resulting outputs for each addresses from all previous functions,
    # so you just need to ask agent "hey,pls show me full breakdown of this token *token address*"
    # More info: https://docs.moralis.com/web3-data-api/evm/reference/get-token-holders

    url = f"https://deep-index.moralis.io/api/v2.2/erc20/{token_address}/owners"
    headers = {"Accept": "application/json", "X-API-Key": MORALIS_API_KEY}
    params = {
        "chain": "base",
        "limit": "15",
        "order": "DESC",
        "token_address": token_address,
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        owners_stat = response.json()["result"]

        if owners_stat:
            owners_data_list = "\n".join(
                [
                    f"Address: {entry['owner_address']}\n"
                    f"Address Wallet net: {wallet_net(entry['owner_address'])}\n"
                    f"Token Balance: {entry['balance_formatted']}\n"
                    f"Supply weight: {entry['percentage_relative_to_total_supply']}\n"
                    f"Usd value: {entry['usd_value']}\n"
                    f"Wallet PNL and Trade Volume: {wallet_pnl(entry['owner_address'])}\n"
                    for entry in owners_stat
                    if is_eoa(entry["owner_address"]) == "True"
                ]
            )

            return owners_data_list
        else:
            return "No token holders found."
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"


# Create the Based Agent with all available functions
based_agent = Agent(
    name="Based Agent",
    model="google/gemini-2.0-pro-exp-02-05:free",
    instructions=(
        "You are a helpful agent that can find comprehensive info about tokens on Base \
    blockchain using token adress"
        "By doing analysis you provide structured breakdown of token market data,token holders,\
    its portfolio,wallet PnL and trade volume"
        "You can use transfer screener to look-up token holders transfer history to find out \
    connections with other token holders,so you could flag them as clusters"
        "You can compare two or more tokens,and find connections between their holders."
        "You can check first buyers of token and its value by given address"
        "If any of you can't do,you can ask to add such functionality"
    ),
    functions=[
        get_token_holders_analysis,
        wallet_net,
        transfer_screener,
        wallet_pnl,
        first_buyers,
    ],
)

# To add a new function:
# 1. Define your function above (follow the existing pattern)
# 2. Add appropriate error handling
# 3. Add the function to the based_agent's functions list
# 4. If your function requires new imports or global variables, add them at the top of the file
# 5. Test your new function thoroughly before deploying

# Example of adding a new function:
# def my_new_function(param1, param2):
#     """
#     Description of what this function does.
#
#     Args:
#         param1 (type): Description of param1
#         param2 (type): Description of param2
#
#     Returns:
#         type: Description of what is returned
#     """
#     try:
#         # Your function logic here
#         result = do_something(param1, param2)
#         return f"Operation successful: {result}"
#     except Exception as e:
#         return f"Error in my_new_function: {str(e)}"

# Then add to based_agent.functions:
# based_agent = Agent(
#     ...
#     functions=[
#         ...
#         my_new_function,
#     ],
# )

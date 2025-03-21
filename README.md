# 🔵 lame-researcher 0.1(trimmed-Based Agent)

An experimental playground for autonomous onchain interactions, and the starting point of the autonomous onchain agent revolution. 

## Introduction

Hi,this is lame-researcher 0.1 based on Based Agent. It was intended as a basic analytical tool or data scraper on Base,so i removed all CDP stuff (sorry) like a wallet interactions etc. Now its trimmed to the level of bare Swarm (i guess).Its utilizing 2 blockchain API (Moralis and Basescan) + 1 for LLM. This was wrote with barely zero knowledge of programming on python. So its a 100% you will find stpid typos or missings. But it works,and exceed any of my expectations.

Ok,what it can do:

### Key Features

- retrieving full breakdown of token top holders(e.g token holders data(supply,%,usd value),
    its net-worth,wallet PnL and trade volume)
- compare two or more tokens (sequentally e.g you ask check token A,then B,and then asking to compare A & B)   
- screening transfers to look-up token holders transfer history to find out any
    connections with other token holders
- checking first buyers of any token  
- standalone wallet check
- combine all above,actually you will figure out when try,its up on your imagination,agent could go much deeper....

### Prerequisites
- Python 3.7+
- Poetry

### API Configuration

Set yours keys and llm base_url as environment variables: 

- `MORALIS_API_KEY`: Your Moralis API key name.
- `BASESCAN_API_KEY`: Your Basescan Api key.
- `OPENAI_API_KEY`: Your OpenAI (or any) API key.
- `OPENAI_BASE_URL`: Your LLM base_url.

If you are not using OpenAi, you also have to set up model name of proprietary llm (e.g model = "google/gemini-2.0-pro-exp-02-05:free") in Agent arguments
(check agents.py)

![image](https://github.com/user-attachments/assets/1e08c265-c0dd-4149-87ef-bc0ba8c1acff)

You can get the Moralis API key here: https://admin.moralis.com/register, Basescan API key here: https://docs.basescan.org/getting-started/viewing-api-usage-statistics. And the OpenAI key here: https://platform.openai.com/api-keys (note you will need to have a paid account)

### Running the Agent

After adding your API Keys to the .env file, you start the agent by terminal command **python run.py**

The agent is typically interacted with through a conversational interface.  You can ask it questions like:

*   "Analyze the holders of token 0x1234..."
*   "Show me the PnL of wallet 0xabcd... over the last 30 days."
*   "What's the net of wallet of 0x9876..."
*    "Who were the first buyers of 0xabdc12356"
*   "Give a transfer screener of 0x1937..."
*   "Could you compare tokens A and B?"

## 🔧 Available Functions

1.  **Token Holder Analysis:**
    *   Provides a comprehensive breakdown of a token's holders.
    *   Identifies key holders and their distribution.
    *   Analyzes the overall health of the token's ownership.
        *   **API Call:** `get_token_holders_analysis(token_address: str)`

2.  **Wallet Net Worth:**
    *   Calculates to get net of the wallet.
        *   **API Call:** `wallet_net(owner_address: str)`

3.  **Transfer Screener:**
    *   Examines the transfer history of a given wallet address.
    *   Helps identify connections between wallets through transfer patterns.
    *   Can be used to flag potential clusters of related wallets.
        *   **API Call:** `transfer_screener(owner_adress: str)`

4.  **Wallet Profit and Loss (PnL):**
    *   Calculates the PnL of a wallet over a specified period (or all time).
    *   Provides insights into a wallet's trading performance.
      *   **API Call:** `wallet_pnl(owner_address: str, days: str | None = None)`

5.  **First Buyers Identification:**
     *   Identifies wallets which were the first buyers of token.
        *   **API Call:** `first_buyers(token_address: str)`


### Agents.py
All of the functionality for the Based Agent resides within `agents.py`. This is the central hub where you can add new capabilities, allowing the agent to perform a wide range of tasks. 
 
### Run.py

Within `run.py`, you have the flexibility to engage the agent in various ways:
1. **Chat-Based Communication**:  Its a main mode.This mode enables you to have a natural language conversation with the agent, allowing it to execute tasks on your behalf through Natural Language Processing (NLP).
2. **One-Agent Autonomous Mode**: In this mode, provide the agent with a static prompt, and it will execute tasks based on its internal decision-making processes and predefined capabilities.
3. **Two-Agent Autonomous Mode**: Here, the setup involves another instance of communication, where a second agent provides dynamic prompting to the primary agent. This setup allows more complex interactions and task executions, providing an exciting opportunity to explore how agents can work together and autonomously.

Based Agent uses:

- **Moralis EVM API**
- **OpenAI Swarm**
- **Basescan API**
- **OpenRouter API**

My setup was completely free,i tried to use Deepseek,its not working.So i used Moralis EVM API free endpoints,Basescan Api free endpoints 
and Gemini 2.0 Pro-Exp free through Openrouter. Even though it works very well.Feel free to use Gpt,Claude,Grok whatever... 

## ❤️ Acknowledgements

Based Agent is made possible thanks to:

- **Coinbase Developer Platform SDK**: [Documentation](https://docs.cdp.coinbase.com/cdp-apis/docs/welcome)
- **OpenAI Swarm (experimental)**: [Documentation](https://github.com/openai/swarm)
- **Lincoln Murr:**: (https://github.com/murrlincoln/Based-Agent)
- **Community Contributors**

Unleash the power of AI on the blockchain with BasedAgent! 🚀

Happy Building! 👩‍💻👨‍💻

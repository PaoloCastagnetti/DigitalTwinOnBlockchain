from web3 import Web3

#Goerli testnet
#web3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/21f69683b6ad401592d9fb2f4ed5e299'))

#Local testnet
#web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
web3 = Web3(Web3.HTTPProvider("192.168.4.11:7545"))
#web3 = Web3(Web3.HTTPProvider("http://023c-80-88-173-170.eu.ngrok.io"))
if(web3.isConnected()):
    print("Connected")

#MetamaskAccount
#account_from = {
#    'private_key': '',
#    'address': '',
#}

#GanacheAccount
account_from={
    'address': '0xf8F0D34C4E8d99e7FC244CF9C661fD9cfC04d129',
    'private_key': '8dd1ae2e6dc1d2a8196a84424413b5ccc640b109153c11a8c47f44f06c396547',
}

contract_address_DT = '0x2b983CD15762E6c169b3F65D6e590DF1a219dCBb'
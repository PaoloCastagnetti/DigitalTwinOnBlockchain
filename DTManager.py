from web3 import Web3
from i_details import account_from, web3
from i_details import contract_address_DT
from DTClass import DTClass as DT
import json

# ----------UTILITY----------
def getBalance(address):
    balance=web3.eth.getBalance(address)
    print(balance)

def deploy(abi, bytecode):
    print(f'Attempting to deploy from account: { account_from["address"] }')
    Contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    
    construct_txn = Contract.constructor().buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    tx_create = web3.eth.account.sign_transaction(construct_txn, account_from['private_key'])

    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    #timestamp = web3.eth.getBlock(tx_receipt.blockNumber, True).timestamp
    #print(timestamp)

    print(f'Contract deployed at address: { tx_receipt.contractAddress }')
    return tx_receipt.contractAddress, tx_receipt.gasUsed

def readAbi(pos):
    # Read the abi from the document written after the compiling
    document = open("Compiled/CompiledAbi.txt", "r").readlines()
    # Get the line in the document without spaces
    tmp_abi = document[(pos*4)-1].strip()
    _abi=json.loads(tmp_abi)
    return _abi

def readBytecode(pos):
    # Read the Bytecode from the document written after the compiling
    document = open("Compiled/CompiledBytecode.txt", "r").readlines()
    # Get the line in the document without spaces
    tmp_bytecode = document[(pos*4)-1].strip()
    return tmp_bytecode

def getLastTransactions(numberOfBlocks, span, abi):
    # Get the number of the last block in the blockchain
    ending_blocknumber = web3.eth.block_number
    # Set the starting block for the research
    starting_blocknumber = ending_blocknumber - span
    if(starting_blocknumber < 1):
        starting_blocknumber = 1
    hashStrList = []
    objFunctList = []
    paramsList = []
    print(f"Started filtering through block number {starting_blocknumber} to {ending_blocknumber} for transactions involving the address - {contract_address_DT}...")
    # Creating the instance of the contract
    contract = web3.eth.contract(address=contract_address_DT, abi=abi)

    # Condition if it's reached the necessary number of blocks
    condition = False

    # If we reached the number of transaction or we don't have any block left the cicle end
    while(len(hashStrList) < numberOfBlocks and starting_blocknumber != 1):
        for x in range(ending_blocknumber, starting_blocknumber, -1):
            block = web3.eth.getBlock(x, True)
            for transaction in block.transactions:
                if transaction['to'] == contract_address_DT or transaction['from'] == contract_address_DT:
                    hashStr = transaction['hash'].hex()
                    # Decoding the input given in the transactions
                    func_obj, func_params = contract.decode_function_input(transaction['input'])
                    hashStrList.append(hashStr)
                    objFunctList.append(str(func_obj))
                    paramsList.append(func_params)
                    if(len(hashStrList) == numberOfBlocks):
                        condition = True
                        break
            # Exit from block loop
            if(condition):
                break

        if(len(hashStrList) < numberOfBlocks):
            ending_blocknumber = starting_blocknumber 
            starting_blocknumber -= span 
            if(starting_blocknumber < 1):
                starting_blocknumber = 1

    print(f"Finished searching blocks {starting_blocknumber} through {ending_blocknumber} and found {len(hashStrList)} transactions")
    # Returning 3 list 
    return hashStrList, objFunctList, paramsList

def getState(abi):
    dt = DT()
    
    # Calling every get method in the contract that let us storage the state of the DT

    # ----------PROPERTIES----------
    properties = getProperties(abi)
    propertiesValue = []
    for i in properties:
        propertiesValue.append(getPropertyValue(i, abi))
    for i in range(len(properties)):
        dt.addProperty(properties[i], propertiesValue[i])
    
    # ----------ACTIONS----------
    actions = getActions(abi)
    actionsName = []
    for i in actions:
        actionsName.append(getActionName(i, abi))
    for i in range(len(actions)):
        dt.addAction(actions[i], actionsName[i])

    # ----------EVENTS----------
    events = getEvents(abi)
    eventsValue = []
    for i in events:
        eventsValue.append(getEventValue(i, abi))
    for i in range(len(events)):
        dt.addEvent(events[i], eventsValue[i])

    # ----------ASSOCIATED PHISICAL OBJECT----------
    associatedPhisicalObjects = getAssociatedPhisicalObjects(abi)
    for i in associatedPhisicalObjects:
        dt.addAssociatedPhisicalObject(i)
    
    # ----------RELATIONS----------
    relations = getRelations(abi)
    for i in relations:
        dt.addRelation(i)

    # Returning a clone of the DT
    return dt

def getOldState(numberOfBlocks, span, abi):
    # Getting the actual state of the DT
    dtState = getState(abi)
    # Getting the 2 list about transaction name and param list
    _, objFunctList, paramsList = getLastTransactions(numberOfBlocks, span, abi)
    k=0
    # If there is an adding action we have to remove it 
    # If there is a setting action we re-set the value to the old value
    for i in objFunctList:
        tmp = i.split(' ')
        #print("tmp: ", tmp)
        if(tmp[1] == "addProperty(string,string)>"):
            dtState.removeProperty(paramsList[k]['_property'])
            #print(paramsList[k]['_property'])
        elif(tmp[1] == "setPropertyValue(string,string,string)>"):
            dtState.setPropertyValue(paramsList[k]['_property'], paramsList[k]['_oldValue'])
            #print(paramsList[k]['_property'], paramsList[k]['_value'])
        elif(tmp[1] == "addAction(string,string)>"):
            dtState.removeAction(paramsList[k]['_action'])
            #print(paramsList[k]['_action'])
        elif(tmp[1] == "setActionName(string,string,string)>"):
            dtState.setActionName(paramsList[k]['_action'], paramsList[k]['_oldName'])
            #print(paramsList[k]['_action'], paramsList[k]['_name'])
        elif(tmp[1] == "addEvent(string,bool)>"):
            dtState.removeEvent(paramsList[k]['_event'])
            #print(paramsList[k]['_event'])
        elif(tmp[1] == "setEventValue(string,bool,bool)>"):
            dtState.setEventValue(paramsList[k]['_event'], paramsList[k]['_oldValue'])
            #print(paramsList[k]['_event'], paramsList[k]['_value'])
        elif(tmp[1] == "addAssociatedPhisicalObject(string)>"):
            dtState.removeAssociatedPhisicalObjects(paramsList[k]['_object'])
            #print(paramsList[k]['_object'])
        elif(tmp[1] == "addRelation(address)>"):
            dtState.removeRelation(paramsList[k]['_address'])
            #print(paramsList[k]['_address'])
        else:
            print("Error, string not accepted")
        k+=1
    # Still return an instance of the old state of the DT
    return dtState

def eventCheck(Contract, receipt):
    # Instantiate the Event
    intruderEvent = Contract.events.intruder()
    # Getting the log of the transaction
    log = intruderEvent.processReceipt(receipt)
    if not log:
        print("Nessun intruso rilevato")
    else:
        print("Trovato un intruso con address: ",log[0]['args']['intruder'])
        print("Tentava di modificare l'oggetto: ", log[0]['args']['object'])

# ----------PROPERTIES----------
def addProperty(_property, _value, abi):
    print(f'Calling the addProperty function with property {_property} with value {_value} at address: { contract_address_DT }')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Build addProperty tx
    addProperty_tx = Contract.functions.addProperty(_property, _value).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(addProperty_tx, account_from['private_key'])
    #print(tx_create.rawTransaction)
    # Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    #print(tx_receipt)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex(), tx_receipt.gasUsed

def setPropertyValue(_property, _value, _oldValue, abi):
    print(f'Calling the setPropertyValue function on property {_property} with value {_value}  at address: { contract_address_DT }')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Build setPropertyValue tx
    setPropertyValue_tx = Contract.functions.setPropertyValue(_property, _value, _oldValue).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(setPropertyValue_tx, account_from['private_key'])
    # Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    eventCheck(Contract, tx_receipt)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex(), tx_receipt.gasUsed

def getPropertyValue(_property, abi):
    print(f'Making a call to contract at address: { contract_address_DT } for info about {_property} property')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Call Contract
    propertyValue = Contract.functions.getPropertyValue(_property).call(transaction={'to':contract_address_DT})
    # The return value is an Integer
    return propertyValue

def getProperties(abi):
    print(f'Making a call to contract at address: { contract_address_DT } for getting properties')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Call Contract
    properties = Contract.functions.getProperties().call(transaction={'to':contract_address_DT})
    # The return value is a List
    return properties

# ----------ACTIONS----------
def addAction(_action, _name, abi):
    print(f'Calling the addAction function with action {_action} with name {_name} at address: { contract_address_DT }')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Build addAction tx
    addAction_tx = Contract.functions.addAction(_action, _name).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(addAction_tx, account_from['private_key'])
    # Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex(), tx_receipt.gasUsed

def setActionName(_action, _name, _oldName, abi):
    print(f'Calling the setActionName function on action {_action} with name {_name}  at address: { contract_address_DT }')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Build setActionName tx
    setActionName_tx = Contract.functions.setActionName(_action, _name, _oldName).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(setActionName_tx, account_from['private_key'])
    # Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    eventCheck(Contract, tx_receipt)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex(), tx_receipt.gasUsed

def getActionName(_action, abi):
    print(f'Making a call to contract at address: { contract_address_DT } for info about {_action} action')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Call Contract
    actionName = Contract.functions.getActionName(_action).call(transaction={'to':contract_address_DT})
    # The return value is a String
    return actionName

def getActions(abi):
    print(f'Making a call to contract at address: { contract_address_DT } for getting actions')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Call Contract
    actions = Contract.functions.getActions().call(transaction={'to':contract_address_DT})
    # The return value is a List
    return actions

# ----------EVENTS----------
def addEvent(_event, _value, abi):
    print(f'Calling the addEvent function with event {_event} with value {_value} at address: { contract_address_DT }')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Build addEvent tx
    addEvent_tx = Contract.functions.addEvent(_event, _value).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(addEvent_tx, account_from['private_key'])
    # Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex(), tx_receipt.gasUsed

def setEventValue(_event, _value, _oldValue, abi):
    print(f'Calling the setEventValue function on event {_event} with value {_value}  at address: { contract_address_DT }')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Build setEventValue tx
    setEventValue_tx = Contract.functions.setEventValue(_event, _value, _oldValue).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(setEventValue_tx, account_from['private_key'])
    # Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    eventCheck(Contract, tx_receipt)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex(), tx_receipt.gasUsed

def getEventValue(_event, abi):
    print(f'Making a call to contract at address: { contract_address_DT } for info about {_event} event')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Call Contract
    eventValue = Contract.functions.getEventValue(_event).call(transaction={'to':contract_address_DT})
    # The return value is an Boolean
    return eventValue

def getEvents(abi):
    print(f'Making a call to contract at address: { contract_address_DT } for getting events')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Call Contract
    events = Contract.functions.getEvents().call(transaction={'to':contract_address_DT})
    # The return value is a List
    return events

# ----------ASSOCIATED PHISICAL OBJECT----------
def addAssociatedPhisicalObject(_object, abi):
    print(f'Calling the addAssociatedPhisicalObject function in contract at address: { contract_address_DT } with {_object} object')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Build addAssociatedPhisicalObject tx
    addAssociatedPhisicalObject_tx = Contract.functions.addAssociatedPhisicalObject(_object).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(addAssociatedPhisicalObject_tx, account_from['private_key'])
    # Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex(), tx_receipt.gasUsed

def getAssociatedPhisicalObjects(abi):
    print(f'Making a call to contract at address: { contract_address_DT } for getting AssociatedPhisicalObjects')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Call Contract
    objects = Contract.functions.getAssociatedPhisicalObjects().call(transaction={'to':contract_address_DT})
    # The return value is a List
    return objects

# ----------RELATIONS----------
def addRelation(_address, abi):
    print(f'Calling the addRelation function in contract at address: { contract_address_DT } with {_address} address')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Build addRelation tx
    addRelation_tx = Contract.functions.addRelation(_address).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(addRelation_tx, account_from['private_key'])
    # Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex(), tx_receipt.gasUsed

def getRelations(abi):
    print(f'Making a call to contract at address: { contract_address_DT } for getting Relations')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Call Contract
    relations = Contract.functions.getRelations().call(transaction={'to':contract_address_DT})
    # The return value is a List
    return relations

def removeRalation(_address, abi):
    print(f'Calling the removeRalation function in contract at address: { contract_address_DT } with {_address} address')
    # Create contract instance
    Contract = web3.eth.contract(address=Web3.toChecksumAddress(contract_address_DT), abi=abi)
    # Build removeRalation tx
    removeRalation_tx = Contract.functions.removeRelation(_address).buildTransaction(
        {
            "gasPrice": web3.eth.gas_price,
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )
    # Sign tx with PK
    tx_create = web3.eth.account.sign_transaction(removeRalation_tx, account_from['private_key'])
    # Send tx and wait for receipt
    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex()
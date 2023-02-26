import DTManager as dt
import json
from DTClass import DTClass as _class
from i_details import account_from, web3

abi = dt.readAbi(2)
bytecode = dt.readBytecode(2)
#dt.getBalance(account_from['address'])
dt.deploy(abi,bytecode)

#hashStrList, objFunctList, paramsList = dt.getLastTransactions(10, 3, abi)
#print(hashStrList)
#print(objFunctList)
#print(paramsList)

#DT = _class()
#DT = dt.getState(abi=abi)
#DT = dt.getOldState(numberOfBlocks=10, span=3, abi=abi)
#jsonStr = json.dumps(DT.__dict__)
#print(jsonStr)


#dt.addProperty("Temperatura", "value: 1", abi)
#tmp = dt.getPropertyValue("1", abi)
#print("actual: ", tmp)

#dt.setPropertyValue("1", "ciaooo", "ciao", abi)

#tmp = dt.getPropertyValue("1", abi)
#print("actual: ", tmp)

#prp = dt.getProperties(abi)
#print("prp: ", prp)

"""

dt.addAction("7", "cal", abi)
#tmp = dt.getActionName("AccendiSpegniLuci", abi)
#print("tmp: ", tmp)
#dt.setActionName("5", "core.a", "switch",abi)
#tmp = dt.getActionName("AccendiSpegniLuci", abi)
#print("tmp: ", tmp)
act = dt.getActions(abi)
print("act: ", act)



dt.addEvent("8", True, abi)
#stl = dt.getEventValue("Stallo", abi)
#print("stl: ", stl)
#dt.setEventValue("7", True, False, abi)
#stl = dt.getEventValue("Stallo", abi)
#print("stl: ", stl)
evn = dt.getEvents(abi)
print("evn: ", evn)



dt.addAssociatedPhisicalObject("9", abi)
psc = dt.getAssociatedPhisicalObjects(abi)
print("psc: ", psc)


# L'indirizzo passato deve esistere sulla net in cui si esegue il contratto
# altrimenti risulta errore dalla variabile assegnata
dt.addRelation("0x8274c471BAa42960f6DE7dDF91E87B80e2F19534", abi)
rlt = dt.getRelations(abi)
print("rlt: ", rlt)
"""
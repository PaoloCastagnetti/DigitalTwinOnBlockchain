import DTManager as dt
import json
from DTClass import DTClass as _class
import time
import numpy as np

abi = dt.readAbi(2)
bytecode = dt.readBytecode(2)
#dt.deploy(abi, bytecode)

print("Selezionare l'operazione di cui valutare le performance:")
print("1. Aggiunta dati")
print("2. Modifica dati")
print("3. Recupero valore")
print("4. Recupero stato DT")
print("5. Deploy contract")
print("6. TestIniziale")
print("7. RecuperoStatoTestIniziale")
print(" ")

op = input("Inserire scelta (1/2/3/4/5/6/7): ")
print(" ")

if op == '1':
    iteration = int(input("Inserire numero di iterazioni da effettuare: "))
    dev=[]
    gas=[]
    for i in range(0, iteration):
        prop = str(i)

        try:
            start_time = time.time()
            _, tmp_gas = dt.addProperty(prop,"value", abi)
            end_time = time.time()
        except Exception as e:
            print("----------!!!----------")
            print(e)
            print("----------!!!----------")
            continue

        elapsed_time = end_time - start_time
        dev.append(elapsed_time)
        gas.append(tmp_gas)
        time.sleep(3)

    mean=np.mean(dev)
    stdev = np.std(dev)
    gasMean=np.mean(gas)

    print(" ")
    print("Operazione: Aggiunta di un valore")
    print("La media del tempo delle operazioni è: ", int(mean*1000), "ms")
    print("La deviazione standard è: ", stdev)
    print("La media del prezzo è di: ", gasMean, " wei")

if op == '2':
    iteration = int(input("Inserire numero di iterazioni da effettuare: "))
    dev=[]
    gas=[]
    for i in range(0, iteration):
        prop = str(i)

        try:
            start_time = time.time()
            _, tmp_gas = dt.setPropertyValue(prop,"value2","value", abi)
            end_time = time.time()
        except Exception as e:
            print("----------!!!----------")
            print(e)
            print("----------!!!----------")
            continue

        elapsed_time = end_time - start_time
        dev.append(elapsed_time)
        gas.append(tmp_gas)
        time.sleep(3)
    
    mean=np.mean(dev)
    stdev = np.std(dev)
    gasMean=np.mean(gas)

    print(" ")
    print("Operazione: Modifica di un valore")
    print("La media del tempo delle operazioni è: ", int(mean*1000), "ms")
    print("La deviazione standard è: ", stdev)
    print("La media del prezzo è di: ", gasMean, " wei")

if op == '3':
    iteration = int(input("Inserire numero di iterazioni da effettuare: "))
    dev=[]
    for i in range(0, iteration):
        prop = str(i)

        try:
            start_time = time.time()
            dt.getPropertyValue(prop,abi)
            end_time = time.time()
        except Exception as e:
            print("----------!!!----------")
            print(e)
            print("----------!!!----------")
            continue

        elapsed_time = end_time - start_time
        dev.append(elapsed_time)

        time.sleep(3)
    
    mean=np.mean(dev)
    stdev = np.std(dev)

    print(" ")
    print("Operazione: Recupero di un valore")
    print("La media del tempo delle operazioni è: ", int(mean*1000), "ms")
    print("La deviazione standard è: ", stdev)
        

if op == '4':
    iteration = int(input("Inserire numero di iterazioni da effettuare: "))
    dev=[]
    for i in range(0, iteration):

        try:
            start_time = time.time()
            dt.getState(abi)
            end_time = time.time()
        except Exception as e:
            print("----------!!!----------")
            print(e)
            print("----------!!!----------")
            continue

        elapsed_time = end_time - start_time
        dev.append(elapsed_time)

        time.sleep(3)
    
    mean=np.mean(dev)
    stdev = np.std(dev)

    print(" ")
    print("Operazione: Recupero di uno stato")
    print("La media del tempo delle operazioni è: ", int(mean*1000), "ms")
    print("La deviazione standard è: ", stdev)
        

if op == '5':
    dev=[]
    gas=[]
    iteration = int(input("Inserire numero di iterazioni da effettuare: "))
    for i in range(0, iteration):
        
        try:
            start_time = time.time()
            _, tmp_gas = dt.deploy(abi, bytecode)
            end_time = time.time()
        except Exception as e:
            print("----------!!!----------")
            print(e)
            print("----------!!!----------")
            continue

         
        elapsed_time = end_time - start_time
        dev.append(elapsed_time)
        gas.append(tmp_gas)
        time.sleep(3)
    
    mean=np.mean(dev)
    stdev = np.std(dev)
    gasMean=np.mean(gas)

    print(" ")
    print("Operazione: Deploy di un contratto")
    print("La media del tempo delle operazioni è: ", int(mean*1000), "ms")
    print("La deviazione standard è: ", stdev)
    print("La media del prezzo è di: ", gasMean, " wei")

if op == '6':
    dev=[]
    gas=[]

    for i in range(1, 11):
        prop = str(i)
        val = str(i)
        try:
            start_time = time.time()
            _, tmp_gas = dt.addProperty(prop,val, abi)
            end_time = time.time()
        except Exception as e:
            print("----------!!!----------")
            print(e)
            print("----------!!!----------")
            continue

         
        elapsed_time = end_time - start_time
        dev.append(elapsed_time)
        gas.append(tmp_gas)
        time.sleep(5)

    time.sleep(300)

    for i in range(0,11):
        for j in range(1,11):
            prop=str(j)
            val = str(j)
            oldVal = str(j)
            try:
                start_time = time.time()
                _, tmp_gas = dt.setPropertyValue(prop, val, oldVal, abi)
                end_time = time.time()
            except Exception as e:
                print("----------!!!----------")
                print(e)
                print("----------!!!----------")
                continue

            elapsed_time = end_time - start_time
            dev.append(elapsed_time)
            gas.append(tmp_gas)
            time.sleep(5)

        time.sleep(300)
    
    mean=np.mean(dev)
    stdev = np.std(dev)
    gasMean=np.mean(gas)

    print(" ")
    print("Operazione: Deploy di un contratto")
    print("La media del tempo delle operazioni è: ", int(mean*1000), "ms")
    print("La deviazione standard è: ", stdev)
    print("La media del prezzo è di: ", gasMean, " wei")

if op == '7':
    try:
        start_time = time.time()
        dt.getState(abi)
        end_time = time.time()
    except Exception as e:
        print("----------!!!----------")
        print(e)
        print("----------!!!----------")
            
    dev=[]
    for i in range(0, iteration):

        try:
            start_time = time.time()
            dt.getState(abi)
            end_time = time.time()
        except Exception as e:
            print("----------!!!----------")
            print(e)
            print("----------!!!----------")
            continue

        elapsed_time = end_time - start_time
        dev.append(elapsed_time)

        time.sleep(3)
    
    mean=np.mean(dev)
    stdev = np.std(dev)

    print(" ")
    print("Operazione: Recupero di uno stato")
    print("La media del tempo delle operazioni è: ", int(mean*1000), "ms")
    print("La deviazione standard è: ", stdev)
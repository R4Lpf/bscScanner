import scanner
import pandas as pd
from pprint import pprint
import time
import time
import asyncio

####################################################
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
#from matplotlib import style
#####################################################
#
#style.use("fivethirtyeight")
#fig, (ax1, ax2) = plt.subplots(2) #,figsize=(16,10), dpi= 80
#####################################################
t0 = time.time()
url= "https://bscscan.com/tokentxns"




async def main():
    t = 1000
    it_compiute = 0
    it_saltate = 0

    for i in range(t):
        time.sleep(1)
        try:
            d = await asyncio.wait_for(scanner.fillDictionary({}), timeout=5.0) #await
            print("---------------------------------------------")
            print(i)
            print("_____________________________________________")
            print(d)
            it_compiute += 1
        except:
            d = 0
            it_saltate+=1
            print(i,"iterazioni salatate: {}".format(it_saltate))
        if d == 0 or d == None or type(d) == type(None):
            pass
        #print(i,d)   qui la funzione fillDictionary ritornava solo se rows(url) era un NoneType o no
        #print(d)
        else:
            if type(d) != type(None):
                try:
                    dfUpdate = pd.read_csv("shitcoins.csv")
                    top_8_transactions = dfUpdate.nlargest(8,"n-transactions")
                    top_8_amount = dfUpdate.nlargest(8,"amount_usd")
                    print(top_8_transactions[["Unnamed: 0", "coincode","n-transactions"]])
                    print(top_8_amount[["Unnamed: 0", "coincode","amount_usd"]])
                    print(len(dfUpdate))
                    #######################################################################################

                    #def animate():
                    #    global top_8_transactions
                    #    global top_8_amount
                    #    top_8_transactions = top_8_transactions.set_index("coincode")
                    #    top_8_transactions.reset_index(inplace=True)
#
                    #    top_8_amount = top_8_amount.set_index("coincode")
                    #    top_8_amount.reset_index(inplace=True)
#
                    #    x = it_compiute
                    #    y0 = top_8_transactions[0]["n-transactions"]
                    #    y1 = top_8_transactions[1]["n-transactions"]
                    #    y2 = top_8_transactions[2]["n-transactions"]
                    #    y3 = top_8_transactions[3]["n-transactions"]
                    #    y4 = top_8_transactions[4]["n-transactions"]
                    #    y5 = top_8_transactions[5]["n-transactions"]
                    #    y6 = top_8_transactions[6]["n-transactions"]
                    #    y7 = top_8_transactions[7]["n-transactions"]
#
                    #    plt.cla()
#
                    #    plt.plot(x, y0, label='Channel 0')
                    #    plt.plot(x, y1, label='Channel 1')
                    #    plt.plot(x, y2, label='Channel 2')
                    #    plt.plot(x, y3, label='Channel 3')
                    #    plt.plot(x, y4, label='Channel 4')
                    #    plt.plot(x, y5, label='Channel 5')
                    #    plt.plot(x, y6, label='Channel 6')
                    #    plt.plot(x, y7, label='Channel 7')
#
                    #    plt.legend(loc='upper left')
                    #    plt.tight_layout()
#
#
                    #ani = animation.FuncAnimation(fig,animate, interval = 5000)
                    #plt.tight_layout()
                    #plt.show()
                except:
                   dfUpdate = pd.DataFrame(data=d).T
                   dfUpdate.to_csv("shitcoins.csv")  
                   
                dfUpdate = pd.read_csv("shitcoins.csv")
                try:
                    dfUpdate = dfUpdate.set_index("Unnamed: 0")
                except:
                    continue
                for i in d:
                    if i in dfUpdate.index:
                        #print("{}: sono li dentro".format(i))
                        dfUpdate.loc[i, "transactionInstant"] = d[i]["transactionInstant"]
                        dfUpdate.loc[i, "transactionHash"] = d[i]["transactionHash"]
                        dfUpdate.loc[i, "amount"] = dfUpdate.loc[i, "amount"] + d[i]["amount"]#*g["price_usd"]
                        dfUpdate.loc[i, "amount_usd"] = dfUpdate.loc[i, "amount_usd"] + d[i]["amount_usd"]
                        dfUpdate.loc[i, "price"] = d[i]["price"]
                        dfUpdate.loc[i, "n-transactions"] += 1
                    else:
                        #print("{}: non sono li dentro".format(i))
                        da_aggiungere = {i:d[i]}
                        dfDA = pd.DataFrame(data = da_aggiungere).T
                        dfUpdate = dfUpdate.append(dfDA)
                    
                    dfUpdate.to_csv("shitcoins.csv")
    t1 = time.time()
    return t1-t0, "iterazioni salatate: {}".format(it_saltate)

try:
    loop = asyncio.get_running_loop()
except RuntimeError:  # 'RuntimeError: There is no current event loop...'
    loop = None

if loop and loop.is_running():
    print('Async event loop already running. Adding coroutine to the event loop.')
    tsk = loop.create_task(main())
    # ^-- https://docs.python.org/3/library/asyncio-task.html#task-object
    # Optionally, a callback function can be executed when the coroutine completes
    tsk.add_done_callback(
        lambda t: print(f'Task done with result={t.result()}  << return val of main()'))
else:
    print('Starting new event loop')
    asyncio.run(main())


#pprint(count)
columns = ("amount","coincode","n-transactions","transactionHash","transactionInstant")


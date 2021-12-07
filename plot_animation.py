import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use("fivethirtyeight")
fig, (ax1, ax2) = plt.subplots(2) #,figsize=(16,10), dpi= 80

def animate(i):
    df = pd.read_csv("coins.csv")
    top_8_transactions = df.nlargest(8, "n-transactions")
    top_8_amount = df.nlargest(8, "amount_usd")
    print(top_8_transactions)
    print(top_8_amount)

    top_8_transactions = top_8_transactions.set_index("coincode")
    top_8_transactions.reset_index(inplace=True)

    # Draw plot
    
    ax1.hlines(y=top_8_transactions.index, xmin=0, xmax=max(top_8_transactions["n-transactions"]), color='gray', alpha=0.7, linewidth=1, linestyles='dashdot')
    ax1.scatter(y=top_8_transactions.index, x=top_8_transactions["n-transactions"], s=75, color='firebrick', alpha=0.7)

    # Title, Label, Ticks and Ylim
    ax1.set_title('Dot Plot for Most Popular coins', fontdict={'size':22})
    ax1.set_xlabel('N-Transactions')
    ax1.set_yticks(top_8_transactions.index)
    ax1.set_yticklabels(top_8_transactions["coincode"].str.title(), fontdict={'horizontalalignment': 'right'})
    ax1.set_xlim(10, max(top_8_transactions["n-transactions"])+10)

    ###############################################################################################################
    # SECOND GRAPH

    # Prepare Data



    # Draw plot
    
    ax2.hlines(y=top_8_amount.index, xmin=0, xmax=max(top_8_amount["amount_usd"]), color='gray', alpha=0.7, linewidth=1, linestyles='dashdot')
    ax2.scatter(y=top_8_amount.index, x=top_8_amount["amount_usd"], s=75, color='firebrick', alpha=0.7)

    # Title, Label, Ticks and Ylim
    ax2.set_title('Dot Plot for Most Payed coins', fontdict={'size':22})
    ax2.set_xlabel('USD')
    ax2.set_yticks(top_8_amount.index)
    ax2.set_yticklabels(top_8_amount["coincode"].str.title(), fontdict={'horizontalalignment': 'right'})
    ax2.set_xlim(10, max(top_8_amount["amount_usd"]))




ani = animation.FuncAnimation(fig, animate, interval = 1000)
plt.tight_layout()
plt.show()



#df = pd.read_csv("coins.csv")
#    top_8_transactions = df.nlargest(8, "n-transactions")
#    top_8_amount = df.nlargest(8, "amount_usd")
#    print(top_8_transactions)
#    print(top_8_amount)
#
#    top_8_transactions = top_8_transactions.set_index("coincode")
#    top_8_transactions.reset_index(inplace=True)
#
#    x = 8
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
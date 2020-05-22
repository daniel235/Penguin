import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib_venn import venn2


def box_plot(pseudoCount, controlCount):
    x = np.arange(2)
    counts = [pseudoCount, controlCount]

    fig, ax = plt.subplots()
    plt.bar(x, counts)
    plt.xticks(x, ('Pseudouridine', 'control'))

    #save box plot
    plt.savefig("TotalCount.png")
    plt.close()



def ven_diagram(pseudoCount, controlCount, totalUmers):
    v = venn2((pseudoCount, controlCount, totalUmers), alpha=1)

    plt.gca().set_axis_bgcolor('skyblue')
    plt.gca().set_axis_on()

    #save graph
    plt.savefig("CountVennDiagram.png")
    plt.close()
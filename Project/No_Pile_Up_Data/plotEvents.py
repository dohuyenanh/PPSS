import matplotlib.pyplot as plt 

with open('Events.csv') as f:
    data = f.readlines()
    
N = len(data)
for i in range(N):
    if i>0:
        line = data[i]
        temp = line.split(',')
        pileUp = int(temp[0])
        defNoPile = int(temp[1])
        manNoPile = int(temp[2])
        stdCut = int(temp[3])
        extCut = int(temp[4])
        cV0A = int(temp[5])
        cZNA = int(temp[6])
        
plt.bar(["With Pile Up","Default No Pile Up","MV & SPD No Pile Up","Standard VertexZ Cut","Extended VertexZ Cut","V0A Centrality Selection","ZNA Centrality Selection"],[pileUp, defNoPile, manNoPile, stdCut, extCut, cV0A, cZNA])
plt.ylabel('Frequency')
plt.title('Histogram of Events')
plt.show()
        
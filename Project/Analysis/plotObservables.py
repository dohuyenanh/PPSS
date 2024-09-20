import matplotlib.pyplot as plt 
import math
import numpy as np
from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages # for saving multiple plots to a single pdf

dataFile = "Big"
cEstimator = "V0A"
VertexZ = False
BonusPileUpRemoved = False


if VertexZ:
    vTitle = "VertexZ"
    vName = "VertexZ"
else:
    vTitle = "NoCut"
    vName = "NoCut"
if dataFile == "Pile":
    pileTitle = "default pile up cuts"
else:
    pileTitle = ""

if BonusPileUpRemoved:
    pileTitle = "extra pile up cuts"
    pileName = "PileUp"
else:
    pileName = "NoPile"

fileName = dataFile+"_"+cEstimator+"_"+vName+"_"+pileName
dirName = "individual_plots/"+fileName+"_plots"
cMax = 9
mean = np.zeros((16,cMax),dtype=float) # Initializes a 2D array for storing mean values, with shape (16,9) and float data type.
var = np.zeros((16,cMax),dtype=float)
nParticles = np.zeros((16,cMax),dtype=float) # 
cov = np.zeros((16,16,cMax),dtype=float) # index1, index2, centrality
Sigma = np.zeros((16,16,cMax),dtype=float)
Delta = np.zeros((16,16,cMax),dtype=float)
Bcorr = np.zeros((16,16,cMax),dtype=float)
Path(dirName).mkdir(parents=True, exist_ok=True)

titleTail = "centrality: "+cEstimator+", "+pileTitle

alfa=0.8
colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:brown","tab:pink","tab:grey","tab:olive","tab:cyan"]
##colors = [(57/255,0/255,7/255,alfa),(75/255,28/255,47/255,alfa),(93/255,55/255,86/255,alfa),(114/255,88/255,133/255,alfa),(132/255,115/255,171/255,alfa),(159/255,158/255,232/255,alfa),(169/255,173/255,254/255,alfa),(205/255,207/255,1,alfa)]
with open(fileName+".csv") as f: # Opens the CSV file in read mode.
    data = f.readlines() # Reads all lines from the file and stores them in the variable 'data'.

N = len(data) # Stores the number of lines read from the file in 'N'.
for i in range(N): # Iterates over each line in 'data'.
    if i>0: # Skips the first line (headers in CSV files).
        line = data[i] # Stores the current line in 'line'.
        temp = line.split(',') # Splits the line by commas and stores the result in 'temp'.
        etaIndex1 = int(temp[0]) # Converts the first element of 'temp' to an integer and stores it in 'etaIndex1'.
        etaIndex2 = int(temp[1])
        cIndex = int(temp[2])
        delta = int(temp[3])
        if(delta == 4):
            nParticles[etaIndex1][cIndex] = float(temp[4])
            mean[etaIndex1][cIndex] = float(temp[5])
            cov[etaIndex1][etaIndex2][cIndex] = float(temp[7])
            Sigma[etaIndex1][etaIndex2][cIndex] = float(temp[8])
            if(etaIndex1 != etaIndex2):
                Delta[etaIndex1][etaIndex2][cIndex] = float(temp[9])
            else:
                var[etaIndex1][cIndex] = float(temp[7])
            Bcorr[etaIndex1][etaIndex2][cIndex] = float(temp[10])
        
plotAll = True
stdDev = True
pdfName = fileName+".pdf"

# Create a PDF file to save all plots


with PdfPages(pdfName) as pdf:
    for centrality in range(1,cMax):
        X = []
        Y = []
        for eta in range(16):
            X.append(eta)
            Y.append(nParticles[eta][centrality]/10**6)
        XPlot = []
        YPlot = []
        XPlot.append(X[0])
        YPlot.append(0)
        for i in range(len(X)-1):
            XPlot.append(X[i])
            YPlot.append(Y[i])
            XPlot.append(X[i+1])
            YPlot.append(Y[i])
        XPlot.append(X[len(X)-1])
        YPlot.append(0)
        plt.plot(XPlot,YPlot,color=colors[centrality-1],label=str(10*(centrality-1))+"-"+str(10*centrality)+"%")
    plt.plot([-2,17],[0,0],color='black')
    plt.xlim([-1,16])
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.xlabel(r"$\eta$ index")
    plt.ylabel("# of particles [millions]")
    plt.title(r"# of particles by $\eta$ range, "+titleTail)
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.subplots_adjust(right=0.8)
    plt.savefig(dirName+"/"+fileName+"_histograms.pdf")
    plt.savefig(dirName+"/"+fileName+"_histograms.png")
    pdf.savefig()
    plt.close()
    # Sigma as a function of centrality. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    for eta in range(7):
        if plotAll:
            etaSym = 16-2-eta
            X = []
            Y = []
            for cIndex in range(1,cMax):
                X.append(cIndex*80/(cMax-1)-5)
                Y.append(Sigma[eta][etaSym][cIndex])
            plt.plot(X,Y,marker="o",label = str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                etaSym = 16-2-eta
                X = []
                Y = []
                for cIndex in range(1,cMax):
                    X.append(cIndex*80/(cMax-1))
                    Y.append(Sigma[eta][etaSym][cIndex])
                plt.plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])


    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title=r"$\Delta \eta$")
    plt.subplots_adjust(right=0.8)
    plt.xlabel("Centrality [%]")
    plt.ylabel(r"$\Sigma$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\Sigma$ vs Centrality, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    pdf.savefig()
    plt.savefig(dirName+"/sigma_vs_centrality.pdf")
    plt.savefig(dirName+"/sigma_vs_centrality.png")
    plt.close()


    # Sigma as a function of ΔEta. Condition: symmetric F & B intervals around \eta=0, for different cetrality classes.
    for centrality in range(1,cMax):
        # etaSym = 16-2-eta
        X = []
        Y = []
        for eta in range(7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Sigma[eta][etaSym][centrality])
        if plotAll:
            plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
        else:
            if centrality == 1 or centrality == 6:
                plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"$\Sigma$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\Sigma$ vs $\Delta\eta$ (symmetric), "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.savefig(dirName+"/sigma_vs_eta_symmetric.pdf")
    plt.savefig(dirName+"/sigma_vs_eta_symmetric.png")
    pdf.savefig()
    plt.close()

     # Sigma as a function of ΔEta. Condition: asymmetric F,B intervals, for different cetrality classes; keep B interval [-0.8, -0.6] fixed and "move" only F interval.
    for centrality in range(1,cMax):
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Sigma[0][eta][centrality])
        plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"$\Sigma$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\Sigma$ vs $\Delta \eta$, (-0.8,-0.6) fixed, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.subplots_adjust(right=0.8) # Adjust the right margin to make room for the legend
    plt.savefig(dirName+"/sigma_vs_eta_asymmetric.pdf")
    plt.savefig(dirName+"/sigma_vs_eta_asymmetric.png")
    pdf.savefig()
    plt.close()
    
# DELTA WITH UNCUT CENTRALITY############################################################################    
    
    # Delta as a function of cenrality. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Delta[eta][etaSym][cIndex])
        if plotAll:
            plt.plot(X,Y,marker="o",label = str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                plt.plot(X,Y,marker="o",label = r"$\Delta \eta$ = "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
            
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title=r"$\Delta\eta$:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel("Centrality [%]")
    plt.ylabel(r"$\Delta$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.title(r"$\Delta$ vs Centrality, "+titleTail)
    pdf.savefig()
    plt.savefig(dirName+"/delta_vs_centrality.pdf")
    plt.savefig(dirName+"/delta_vs_centrality.png")
    plt.close()
### 1 - mean ratio vs centrality
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(1-mean[eta][cIndex]/mean[etaSym][cIndex])
        if plotAll:
            plt.plot(X,Y,marker="o",label = str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                plt.plot(X,Y,marker="o",label = r"$\Delta \eta$ = "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
            
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title=r"$\Delta \eta$")
    plt.subplots_adjust(right=0.8)
    plt.xlabel("Centrality [%]")
    plt.ylabel(r"$1-\frac{\langle n_F \rangle}{\langle n_B \rangle}$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$1-\frac{\langle n_F \rangle}{\langle n_B \rangle}$ vs Centrality, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    pdf.savefig()
    plt.savefig(dirName+"/means_ratio_centrality.pdf")
    plt.savefig(dirName+"/means_ratio_centrality.png")
    plt.close()
### 1 - mean ratio vs delta eta
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(1-mean[eta][centrality]/mean[etaSym][centrality])
        if plotAll:
            plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
            
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title=r"$\Delta \eta$")
    plt.subplots_adjust(right=0.8)
    plt.xlabel(r"$\Delta\eta$")
    plt.ylabel(r"$1-\frac{\langle n_F \rangle}{\langle n_B \rangle}$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$1-\frac{\langle n_F \rangle}{\langle n_B \rangle}$ vs $\Delta\eta$ (symmetric), "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    pdf.savefig()
    plt.savefig(dirName+"/means_ratio_eta.pdf")
    plt.savefig(dirName+"/means_ratio_eta.png")
    plt.close()

# variance vs centrality
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(var[eta][cIndex])
        if plotAll:
            plt.plot(X,Y,marker="o",label = r"$\Delta \eta$ = "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                plt.plot(X,Y,marker="o",label = str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
    dummy1, = plt.plot([],[],color = "black", label = "Backward")
    dummy2, = plt.plot([],[],color = "black", linestyle = "dashed", label = "Forward")        
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title=r"$\Delta \eta$")
    plt.subplots_adjust(right=0.8)

    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(var[etaSym][cIndex])
        if plotAll:
            plt.plot(X,Y,marker="o",label = str(round(2*abs(-0.6+eta*0.1),2)),color = colors[eta], linestyle = "dashed")
        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                plt.plot(X,Y,marker="o",label = str(round(2*abs(-0.6+eta*0.1),2)),color = colors[eta], linestyle = "dashed")
    plt.xlabel("Centrality [%]")
    plt.ylabel(r"$\text{Var}(n)$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    
    plt.title(r"$\text{Var}(n)$ vs Centrality, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    pdf.savefig()
    plt.savefig(dirName+"/var_centrality.pdf")
    plt.savefig(dirName+"/var_centrality.png")
    plt.close()
## variance vs delta Eta
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(var[eta][centrality])
        if plotAll:
            plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
        else:
            if centrality == 1 or centrality == 6:
                plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    dummy1, = plt.plot([],[],color = "black", label = "Backward")
    dummy2, = plt.plot([],[],color = "black", linestyle = "dashed", label = "Forward")  
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.subplots_adjust(right=0.8)
    for centrality in range(1,cMax):    
        X = []
        Y = []
        for eta in range(7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(var[etaSym][centrality])
        if plotAll:
            plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color = colors[centrality-1], linestyle = "dashed")
        else:
            if centrality == 1 or centrality == 6:
                plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color = colors[centrality-1], linestyle = "dashed")
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"$\text{Var}(n)$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\text{Var}(n)$ vs $\Delta\eta$ (symmetric), "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.savefig(dirName+"/var_eta_symmetric.pdf")
    plt.savefig(dirName+"/var_eta_symmetric.png")
    pdf.savefig()
    plt.close() 
#     # Delta as a function of ΔEta. Condition: symmetric F & B intervals around \eta=0, for different cetrality classes.

    for centrality in range(1,cMax):
        X = []
        Y = []
        for eta in range(7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Delta[eta][etaSym][centrality])
        if plotAll:
            plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
        else:
            if centrality == 1 or centrality == 6:
                plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"$\Delta$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\Delta$ vs $\Delta\eta$ (symmetric), "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.savefig(dirName+"/delta_vs_eta_symmetric.pdf")
    plt.savefig(dirName+"/delta_vs_eta_symmetric.png")
    
    pdf.savefig()
    plt.close()

#     # Delta as a function of ΔEta. Condition: asymmetric F,B intervals, for different cetrality classes; keep B interval [-0.8, -0.6] fixed and "move" only F interval.
#     for centrality in range(1,cMax):
    for centrality in range(1,cMax):
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Delta[0][eta][centrality])
        plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"$\Delta$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\Delta$ vs $\Delta \eta$, (-0.8,-0.6) fixed, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.subplots_adjust(right=0.8) # Adjust the right margin to make room for the legend
    plt.savefig(dirName+"/delta_vs_eta_asymmetric.pdf")
    plt.savefig(dirName+"/delta_vs_eta_asymmetric.png")
    pdf.savefig()
    plt.close()
# DELTA WITH CUT CENTRALITY############################################################################    
    
    # Delta as a function of centrality. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,6):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Delta[eta][etaSym][cIndex])
        if plotAll:
            plt.plot(X,Y,marker="o",label = str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                plt.plot(X,Y,marker="o",label = r"$\Delta \eta$ = "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
            
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title=r"$\Delta\eta$:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel("Centrality [%]")
    plt.ylabel(r"$\Delta$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.title(r"$\Delta$ vs Centrality, "+titleTail)
    pdf.savefig()
    plt.savefig(dirName+"/delta_vs_centrality_cut.pdf")
    plt.savefig(dirName+"/delta_vs_centrality_cut.png")
    
    plt.close()

    

#     # Delta as a function of ΔEta. Condition: symmetric F & B intervals around \eta=0, for different cetrality classes.

    for centrality in range(1,6):
        # etaSym = 16-2-eta
        X = []
        Y = []
        for eta in range(7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Delta[eta][etaSym][centrality])
        if plotAll:
            plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
        else:
            if centrality == 1 or centrality == 6:
                plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"$\Delta$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\Delta$ vs $\Delta\eta$ (symmetric), "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.savefig(dirName+"/delta_vs_eta_symmetric_cut.pdf")
    plt.savefig(dirName+"/delta_vs_eta_symmetric_cut.png")
    pdf.savefig()
    plt.close()

#     # Delta as a function of ΔEta. Condition: asymmetric F,B intervals, for different cetrality classes; keep B interval [-0.8, -0.6] fixed and "move" only F interval.
#     for centrality in range(1,cMax):
    for centrality in range(1,6):
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Delta[0][eta][centrality])
        plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"$\Delta$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\Delta$ vs $\Delta \eta$, (-0.8,-0.6) fixed, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.subplots_adjust(right=0.8) # Adjust the right margin to make room for the legend
    plt.savefig(dirName+"/delta_vs_eta_asymmetric_cut.pdf")
    plt.savefig(dirName+"/delta_vs_eta_asymmetric_cut.png")
    pdf.savefig()
    plt.close()
# ############################################################################
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Bcorr[eta][etaSym][cIndex])
        
        if plotAll:
            plt.plot(X,Y,marker="o",label = str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                plt.plot(X,Y,marker="o",label = r"$\Delta \eta$ = "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
            
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title=r"$\Delta \eta$")
    plt.subplots_adjust(right=0.8)
    plt.xlabel("Centrality [%]")
    plt.ylabel(r"$b_\text{corr}$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$b_\text{corr}$ vs Centrality, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    pdf.savefig()
    plt.savefig(dirName+"/bcorr_vs_centrality.pdf")
    plt.savefig(dirName+"/bcorr_vs_centrality.png")
    plt.close()
    

#     # Bcorr as a function of ΔEta. Condition: symmetric F & B intervals around \eta=0, for different cetrality classes.

    for centrality in range(1,cMax):
        # etaSym = 16-2-eta
        X = []
        Y = []
        for eta in range(7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Bcorr[eta][etaSym][centrality])
        if plotAll:
            plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
        else:
            if centrality == 1 or centrality == 6:
                plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"$b_\text{corr}$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$b_\text{corr}$ vs $\Delta\eta$ (symmetric), "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.savefig(dirName+"/bcorr_vs_eta_symmetric.pdf")
    plt.savefig(dirName+"/bcorr_vs_eta_symmetric.png")
    pdf.savefig()
    plt.close()

#     # Bcorr as a function of ΔEta. Condition: asymmetric F,B intervals, for different cetrality classes; keep B interval [-0.8, -0.6] fixed and "move" only F interval.
#     for centrality in range(1,cMax):
    for centrality in range(1,cMax):
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Bcorr[0][eta][centrality])
        plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"$b_\text{corr}$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$b_\text{corr}$ vs $\Delta \eta$, (-0.8,-0.6) fixed, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.subplots_adjust(right=0.8) # Adjust the right margin to make room for the legend
    plt.savefig(dirName+"/bcorr_vs_eta_asymmetric.pdf")
    plt.savefig(dirName+"/bcorr_vs_eta_asymmetric.png")
    pdf.savefig()
    plt.close()

# ############################################################################    
    
    # covariance as a function of centrality. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(cov[eta][etaSym][cIndex])
        if plotAll:
            plt.plot(X,Y,marker="o",label = str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                plt.plot(X,Y,marker="o",label = r"$\Delta \eta$ = "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
            
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title=r"$\Delta \eta$")
    plt.subplots_adjust(right=0.8)
    plt.xlabel("Centrality [%]")
    plt.ylabel(r"Covariance")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"Covariance vs Centrality, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    pdf.savefig()
    plt.savefig(dirName+"/covariance_vs_centrality.pdf")
    plt.savefig(dirName+"/covariance_vs_centrality.png")
    plt.close()

#     # Delta as a function of ΔEta. Condition: symmetric F & B intervals around \eta=0, for different cetrality classes.

    for centrality in range(1,cMax):
        # etaSym = 16-2-eta
        X = []
        Y = []
        for eta in range(7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(cov[eta][etaSym][centrality])
        if plotAll:
            plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
        else:
            if centrality == 1 or centrality == 6:
                plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"Covariance")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"Covariance vs $\Delta\eta$ (symmetric), "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.savefig(dirName+"/covariance_vs_eta_symmetric.pdf")
    plt.savefig(dirName+"/covariance_vs_eta_symmetric.png")
    pdf.savefig()
    plt.close()

#     # Delta as a function of ΔEta. Condition: asymmetric F,B intervals, for different cetrality classes; keep B interval [-0.8, -0.6] fixed and "move" only F interval.
#     for centrality in range(1,cMax):
    for centrality in range(1,cMax):
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(cov[0][eta][centrality])
        plt.plot(X,Y,marker="o",label=str(10*(centrality-1))+"-"+str(10*centrality)+"%",color=colors[centrality-1])
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Centrality range:")
    plt.subplots_adjust(right=0.8) # Adjust the right margin to make room for the legend
    plt.xlabel(r"$\Delta \eta$")
    plt.ylabel(r"Covariance")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"Covariance vs $\Delta \eta$, (-0.8,-0.6) fixed, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.savefig(dirName+"/covariance_vs_eta_asymmetric.pdf")
    plt.savefig(dirName+"/covariance_vs_eta_asymmetric.png")
    pdf.savefig()
    plt.close()


    bMax = 5
    mean = np.zeros((16,cMax,bMax),dtype=float) # Initializes a 2D array for storing mean values, with shape (16,9) and float data type.
    cov = np.zeros((16,16,cMax,bMax),dtype=float) # index1, index2, centrality
    nParticles = np.zeros((16,cMax,bMax),dtype=float) # 
    Sigma = np.zeros((16,16,cMax,bMax),dtype=float)
    Delta = np.zeros((16,16,cMax,bMax),dtype=float)
    Bcorr = np.zeros((16,16,cMax,bMax),dtype=float)
    with open(fileName+".csv") as f: # Opens the CSV file in read mode.
        data = f.readlines() # Reads all lines from the file and stores them in the variable 'data'.
    N = len(data) # Stores the number of lines read from the file in 'N'.
    for i in range(N): # Iterates over each line in 'data'.
        if i>0: # Skips the first line (headers in CSV files).
            line = data[i] # Stores the current line in 'line'.
            temp = line.split(',') # Splits the line by commas and stores the result in 'temp'.
            etaIndex1 = int(temp[0]) # Converts the first element of 'temp' to an integer and stores it in 'etaIndex1'.
            etaIndex2 = int(temp[1])
            cIndex = int(temp[2])
            delta = int(temp[3])
        
            nParticles[etaIndex1][cIndex][delta] = float(temp[4])
            mean[etaIndex1][cIndex][delta] = float(temp[5]) 
            cov[etaIndex1][etaIndex2][cIndex][delta] = float(temp[7])
            Sigma[etaIndex1][etaIndex2][cIndex][delta] = float(temp[8])
            if(etaIndex1 != etaIndex2):
                Delta[etaIndex1][etaIndex2][cIndex][delta] = float(temp[9])
            Bcorr[etaIndex1][etaIndex2][cIndex][delta] = float(temp[10])
        
    # Sigma as a function of bin width for delta eta = 1.2
    eta = 0
    etaSym = 16-2-eta
    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Sigma[eta][etaSym][centrality][delta])
        plt.plot(X,Y,marker="o",label = str(binCenter)+"%",color=colors[centrality-1])
        print(binCenter, Y)
    
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Bin center:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel(r"$\Delta$Centrality [%]")
    plt.ylabel(r"$\Sigma$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\Sigma$ vs $\Delta$Centrality, $\Delta\eta=1.2$, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    plt.savefig(dirName+"/sigma_vs_bin_width.pdf")
    plt.savefig(dirName+"/sigma_vs_bin_width.png")
    pdf.savefig()
    plt.close()
    # Delta as a function of as a function of bin width for delta eta = 1.2
    eta = 0
    etaSym = 16-2-eta
    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Delta[eta][etaSym][centrality][delta])
        plt.plot(X,Y,marker="o",label = str(binCenter)+"%",color=colors[centrality-1])
        print(binCenter, Y)
    
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Bin center:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel(r"$\Delta$Centrality [%]")
    plt.ylabel(r"$\Delta$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$\Delta$ vs $\Delta$Centrality, $\Delta\eta=1.2$, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    #plt.show()
    #plt.savefig("Sigma_vs_Centrality.pdf")
    plt.savefig(dirName+"/delta_vs_bin_width.pdf")
    plt.savefig(dirName+"/delta_vs_bin_width.png")
    pdf.savefig()
    plt.close()
    
    # Bcorr as a function of bin width for delta eta = 1.2
    eta = 0
    etaSym = 16-2-eta
    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Bcorr[eta][etaSym][centrality][delta])
        plt.plot(X,Y,marker="o",label = str(binCenter)+"%",color=colors[centrality-1])
        print(binCenter, Y)
    
    plt.legend(bbox_to_anchor=(1, 0.5), loc='center left',title="Bin center:")
    plt.subplots_adjust(right=0.8)
    plt.xlabel(r"$\Delta$Centrality [%]")
    plt.ylabel(r"$b_\text{corr}$")
    plt.grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    plt.title(r"$b_\text{corr}$ vs $\Delta$Centrality, $\Delta\eta=1.2$, "+titleTail)
    if stdDev:
        plt.annotate("Std. dev. < 0.0005",(0.05,0.05),xycoords='axes fraction',bbox=dict(facecolor=(1,1,1,0.5), edgecolor='black', pad=5.0))
    #plt.show()
    plt.savefig(dirName+"/bcorr_vs_bin_width.pdf")
    plt.savefig(dirName+"/bcorr_vs_bin_width.png")
    pdf.savefig()
    plt.close()

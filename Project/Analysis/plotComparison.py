import matplotlib.pyplot as plt 
import math
import numpy as np
from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages # for saving multiple plots to a single pdf

FirstLabel = "V0A"
SecondLabel = "ZNA"
outputName = "V0A_vs_ZNA_extra_pileup"

dataFile1 = "Pile"
cEstimator1 = "V0A"
VertexZ1 = True
BonusPileUpRemoved1 = True
dataFile2 = "Pile"
cEstimator2 = "ZNA"
VertexZ2 = True
BonusPileUpRemoved2 = True

if VertexZ1:
    vName1 = "VertexZ"
else:
    vName1 = "NoCut"
if VertexZ2:
    vName2 = "VertexZ"
else:
    vName2 = "NoCut"
##if dataFile1 == "Pile":
##    pileTitle1 = "default pile up cuts"
##else:
##    pileTitle1 = ""
##if dataFile2 == "Pile":
##    pileTitle2 = "default pile up cuts"
##else:
##    pileTitle2 = ""

if BonusPileUpRemoved1:
    pileName1 = "PileUp"
else:
    pileName1 = "NoPile"
if BonusPileUpRemoved2:
    pileName2 = "PileUp"
else:
    pileName2 = "NoPile"

fileName1 = dataFile1+"_"+cEstimator1+"_"+vName1+"_"+pileName1
fileName2 = dataFile2+"_"+cEstimator2+"_"+vName2+"_"+pileName2



dirName = "individual_plots/"+outputName+"_plots"
cMax = 9
mean = np.zeros((16,cMax,2),dtype=float) # Initializes a 2D array for storing mean values, with shape (16,9) and float data type.
nParticles = np.zeros((16,cMax,2),dtype=float) # 
cov = np.zeros((16,16,cMax,2),dtype=float) # index1, index2, centrality
Sigma = np.zeros((16,16,cMax,2),dtype=float)
Delta = np.zeros((16,16,cMax,2),dtype=float)
Bcorr = np.zeros((16,16,cMax,2),dtype=float)
Path(dirName).mkdir(parents=True, exist_ok=True)
alfa=0.8
colors = ["tab:blue","tab:orange","tab:green","tab:red","tab:purple","tab:brown","tab:pink","tab:grey","tab:olive","tab:cyan"]
##colors = [(57/255,0/255,7/255,alfa),(75/255,28/255,47/255,alfa),(93/255,55/255,86/255,alfa),(114/255,88/255,133/255,alfa),(132/255,115/255,171/255,alfa),(159/255,158/255,232/255,alfa),(169/255,173/255,254/255,alfa),(205/255,207/255,1,alfa)]

with open(fileName1+".csv") as f: # Opens the CSV file in read mode.
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
            nParticles[etaIndex1][cIndex][0] = float(temp[4])
            mean[etaIndex1][cIndex][0] = float(temp[5]) 
            cov[etaIndex1][etaIndex2][cIndex][0] = float(temp[7])
            Sigma[etaIndex1][etaIndex2][cIndex][0] = float(temp[8])
            if(etaIndex1 != etaIndex2):
                Delta[etaIndex1][etaIndex2][cIndex][0] = float(temp[9])
            Bcorr[etaIndex1][etaIndex2][cIndex][0] = float(temp[10])
with open(fileName2+".csv") as f: # Opens the CSV file in read mode.
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
            nParticles[etaIndex1][cIndex][1] = float(temp[4])
            mean[etaIndex1][cIndex][1] = float(temp[5]) 
            cov[etaIndex1][etaIndex2][cIndex][1] = float(temp[7])
            Sigma[etaIndex1][etaIndex2][cIndex][1] = float(temp[8])
            if(etaIndex1 != etaIndex2):
                Delta[etaIndex1][etaIndex2][cIndex][1] = float(temp[9])
            Bcorr[etaIndex1][etaIndex2][cIndex][1] = float(temp[10])
        
plotAll = True
pdfName = outputName+".pdf"

# Create a PDF file to save all plots


with PdfPages(pdfName) as pdf:
    # Sigma as a function of centrality. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Sigma[eta][etaSym][cIndex][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

    handles, labels = axs[0].get_legend_handles_labels()
    for eta in range(7):
        
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Sigma[eta][etaSym][cIndex][1])
            
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)))

    for eta in range(7):
        
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Sigma[eta][etaSym][cIndex][0]/Sigma[eta][etaSym][cIndex][1])
            print(Sigma[eta][etaSym][cIndex][0]/Sigma[eta][etaSym][cIndex][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
    ##plt.legend()
    axs[0].set_xlabel("Centrality [%]")
    axs[0].set_ylabel(r"$\Sigma$")
    axs[1].set_ylabel(r"$\Sigma_1/\Sigma_2$")
    fig.suptitle(r"$\Sigma$ vs centrality")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel,marker="o",fillstyle="none")
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", marker="s",fillstyle="none",label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/sigma_vs_centrality.pdf")
    plt.close()

# Sigma as a function of delta eta. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Sigma[eta][etaSym][centrality][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    for centrality in range(1,cMax):  
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Sigma[eta][etaSym][centrality][1])
           
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Sigma[eta][etaSym][centrality][0]/Sigma[eta][etaSym][centrality][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    ##plt.legend()
    axs[0].set_xlabel(r"$\Delta \eta$")
    axs[0].set_ylabel(r"$\Sigma$")
    axs[1].set_ylabel(r"$\Sigma_1/\Sigma_2$")
    fig.suptitle(r"$\Sigma$ vs $\Delta\eta$")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/sigma_vs_eta_symmetric.pdf")
    plt.close()
# Sigma as a function of delta eta, asymmetric. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Sigma[0][eta][centrality][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    for centrality in range(1,cMax):  
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Sigma[0][eta][centrality][0])
           
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Sigma[0][eta][centrality][0]/Sigma[0][eta][centrality][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    ##plt.legend()
    axs[0].set_xlabel(r"$\Delta \eta$")
    axs[0].set_ylabel(r"$\Sigma$")
    axs[1].set_ylabel(r"$\Sigma_1/\Sigma_2$")
    fig.suptitle(r"$\Sigma$ vs $\Delta \eta$ for (-0.8,-0.6) bin fixed")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/sigma_vs_eta_asymmetric.pdf")
    plt.close()
######DELTA
    # Delta as a function of centrality. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Delta[eta][etaSym][cIndex][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

    for eta in range(7):
        
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Delta[eta][etaSym][cIndex][1])
            
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)))

    for eta in range(7):
        
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Delta[eta][etaSym][cIndex][0]/Delta[eta][etaSym][cIndex][1])
            print(Delta[eta][etaSym][cIndex][0]/Delta[eta][etaSym][cIndex][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
    ##plt.legend()
    axs[0].set_xlabel("Centrality [%]")
    axs[0].set_ylabel(r"$\Delta$")
    axs[1].set_ylabel(r"$\Delta_1/\Delta_2$")
    fig.suptitle(r"$\Delta$ vs centrality")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/delta_vs_centrality.pdf")
    plt.close()

# Delta as a function of delta eta. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Delta[eta][etaSym][centrality][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    for centrality in range(1,cMax):  
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Delta[eta][etaSym][centrality][1])
           
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Delta[eta][etaSym][centrality][0]/Delta[eta][etaSym][centrality][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    ##plt.legend()
    axs[0].set_xlabel(r"$\Delta \eta$")
    axs[0].set_ylabel(r"$\Delta$")
    axs[1].set_ylabel(r"$\Delta_1/\Delta_2$")
    fig.suptitle(r"$\Delta$ vs $\Delta\eta$")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/delta_vs_eta_symmetric.pdf")
    plt.close()
# Delta as a function of delta eta, asymmetric. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Delta[0][eta][centrality][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    for centrality in range(1,cMax):  
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Delta[0][eta][centrality][1])
           
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Delta[0][eta][centrality][0]/Delta[0][eta][centrality][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    ##plt.legend()
    axs[0].set_xlabel(r"$\Delta \eta$")
    axs[0].set_ylabel(r"$\Delta$")
    axs[1].set_ylabel(r"$\Delta_1/\Delta_2$")
    fig.suptitle(r"$\Delta$ vs $\Delta \eta$ for (-0.8,-0.6) bin fixed")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/delta_vs_eta_asymmetric.pdf")
    plt.close()

######DELTA (CUT TO CENTRALITY<=50%)
    # Delta as a function of centrality. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,6):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Delta[eta][etaSym][cIndex][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

    for eta in range(7):
        
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,6):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Delta[eta][etaSym][cIndex][1])
            
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)))

    for eta in range(7):
        
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,6):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Delta[eta][etaSym][cIndex][0]/Delta[eta][etaSym][cIndex][1])
            print(Delta[eta][etaSym][cIndex][0]/Delta[eta][etaSym][cIndex][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
    ##plt.legend()
    axs[0].set_xlabel("Centrality [%]")
    axs[0].set_ylabel(r"$\Delta$")
    axs[1].set_ylabel(r"$\Delta_1/\Delta_2$")
    fig.suptitle(r"$\Delta$ vs centrality")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/delta_vs_centrality.pdf")
    plt.close()

# Delta as a function of delta eta. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for centrality in range(1,6):
        
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Delta[eta][etaSym][centrality][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    for centrality in range(1,6):  
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Delta[eta][etaSym][centrality][1])
           
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")
    for centrality in range(1,6):
        
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Delta[eta][etaSym][centrality][0]/Delta[eta][etaSym][centrality][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    ##plt.legend()
    axs[0].set_xlabel(r"$\Delta \eta$")
    axs[0].set_ylabel(r"$\Delta$")
    axs[1].set_ylabel(r"$\Delta_1/\Delta_2$")
    fig.suptitle(r"$\Delta$ vs $\Delta\eta$")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/delta_vs_eta_symmetric.pdf")
    plt.close()
# Delta as a function of delta eta, asymmetric. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for centrality in range(1,6):
        
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Delta[0][eta][centrality][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    for centrality in range(1,6):  
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Delta[0][eta][centrality][1])
           
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")
    for centrality in range(1,6):
        
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Delta[0][eta][centrality][0]/Delta[0][eta][centrality][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    ##plt.legend()
    axs[0].set_xlabel(r"$\Delta \eta$")
    axs[0].set_ylabel(r"$\Delta$")
    axs[1].set_ylabel(r"$\Delta_1/\Delta_2$")
    fig.suptitle(r"$\Delta$ vs $\Delta \eta$ for (-0.8,-0.6) bin fixed")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/delta_vs_eta_asymmetric.pdf")
    plt.close()
# Bcorr as a function of centrality. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for eta in range(7):
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Bcorr[eta][etaSym][cIndex][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

    for eta in range(7):
        
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Bcorr[eta][etaSym][cIndex][1])
            
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)))

    for eta in range(7):
        
        etaSym = 16-2-eta
        X = []
        Y = []
        for cIndex in range(1,cMax):
            X.append(cIndex*80/(cMax-1)-5)
            Y.append(Bcorr[eta][etaSym][cIndex][0]/Bcorr[eta][etaSym][cIndex][1])
            print(Bcorr[eta][etaSym][cIndex][0]/Bcorr[eta][etaSym][cIndex][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[eta])
    ##plt.legend()
    axs[0].set_xlabel("Centrality [%]")
    axs[0].set_ylabel(r"$b_\text{corr}$")
    axs[1].set_ylabel(r"$b_{\text{corr}1}/b_{\text{corr}2}$")
    fig.suptitle(r"$b_{\text{corr}}$ vs centrality")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/bcorr_vs_centrality.pdf")
    plt.close()

# Bcorr as a function of delta eta. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Bcorr[eta][etaSym][centrality][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    for centrality in range(1,cMax):  
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Bcorr[eta][etaSym][centrality][1])
           
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(1,7):
            etaSym = 16-2-eta
            X.append(2*abs(-0.6+eta*0.1))
            Y.append(Bcorr[eta][etaSym][centrality][0]/Bcorr[eta][etaSym][centrality][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    ##plt.legend()
    axs[0].set_xlabel(r"$\Delta \eta$")
    axs[0].set_ylabel(r"$b_{\text{corr}}$")
    axs[1].set_ylabel(r"$b_{\text{corr}1}/b_{\text{corr}2}$")
    fig.suptitle(r"$b_{\text{corr}}$ vs $\Delta\eta$")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/bcorr_vs_eta_symmetric.pdf")
    plt.close()
# Bcorr as a function of delta eta, asymmetric. Condition: separation gap between F and B intervals ΔEta=1.2 and ΔEta=0.6 and F & B intervals are symmetric.
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Bcorr[0][eta][centrality][0])
        if plotAll:
            axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="o",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    for centrality in range(1,cMax):  
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Bcorr[0][eta][centrality][1])
           
        if plotAll:
            axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[0].plot(X,Y,marker="s",fillstyle='none',label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1],linestyle="dashed")
    for centrality in range(1,cMax):
        
        X = []
        Y = []
        for eta in range(2,15):
            X.append((eta-2)*0.1)
            Y.append(Bcorr[0][eta][centrality][0]/Bcorr[0][eta][centrality][1])
        if plotAll:
            axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

        else:
            if round(2*abs(-0.6+eta*0.1),2)==1.2 or round(2*abs(-0.6+eta*0.1),2) == 0.6:
                axs[1].plot(X,Y,marker="o",label = r"$\Delta \eta$ "+str(round(2*abs(-0.6+eta*0.1),2)),color=colors[centrality-1])

    
    
    axs[0].set_xlabel(r"$\Delta \eta$")
    axs[0].set_ylabel(r"$b_{\text{corr}}$")
    axs[1].set_ylabel(r"$b_{\text{corr}1}/b_{\text{corr}2}$")
    fig.suptitle(r"$b_{\text{corr}}$ vs $\Delta \eta$ for (-0.8,-0.6) bin fixed")
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend(handles = [dummy1,dummy2])
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    pdf.savefig()
    plt.savefig(dirName+"/bcorr_vs_eta_asymmetric.pdf")
    plt.close()

    ##bin width comparison
    bMax = 5
    mean = np.zeros((16,cMax,bMax,2),dtype=float) # Initializes a 2D array for storing mean values, with shape (16,9) and float data type.
    nParticles = np.zeros((16,cMax,bMax,2),dtype=float) # 
    cov = np.zeros((16,16,cMax,bMax,2),dtype=float) # index1, index2, centrality
    Sigma = np.zeros((16,16,cMax,bMax,2),dtype=float)
    Delta = np.zeros((16,16,cMax,bMax,2),dtype=float)
    Bcorr = np.zeros((16,16,cMax,bMax,2),dtype=float)
    with open(fileName1+".csv") as f: # Opens the CSV file in read mode.
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
            nParticles[etaIndex1][cIndex][delta][0] = float(temp[4])
            mean[etaIndex1][cIndex][delta][0] = float(temp[5]) 
            cov[etaIndex1][etaIndex2][cIndex][delta][0] = float(temp[7])
            Sigma[etaIndex1][etaIndex2][cIndex][delta][0] = float(temp[8])
            if(etaIndex1 != etaIndex2):
                Delta[etaIndex1][etaIndex2][cIndex][delta][0] = float(temp[9])
            Bcorr[etaIndex1][etaIndex2][cIndex][delta][0] = float(temp[10])
    with open(fileName2+".csv") as f: # Opens the CSV file in read mode.
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
            nParticles[etaIndex1][cIndex][delta][1] = float(temp[4])
            mean[etaIndex1][cIndex][delta][1] = float(temp[5]) 
            cov[etaIndex1][etaIndex2][cIndex][delta][1] = float(temp[7])
            Sigma[etaIndex1][etaIndex2][cIndex][delta][1] = float(temp[8])
            if(etaIndex1 != etaIndex2):
                Delta[etaIndex1][etaIndex2][cIndex][delta][1] = float(temp[9])
            Bcorr[etaIndex1][etaIndex2][cIndex][delta][1] = float(temp[10])
    # Sigma as a function of bin width for delta eta = 1.2
    eta = 0
    etaSym = 16-2-eta
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend()
    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Sigma[eta][etaSym][centrality][delta][0])
        axs[0].plot(X,Y,marker="o",fillstyle="none",label = str(binCenter)+"%",color=colors[centrality-1])
    
    

    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Sigma[eta][etaSym][centrality][delta][1])
        axs[0].plot(X,Y,marker="s",fillstyle="none",linestyle="dashed",color=colors[centrality-1])

    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Sigma[eta][etaSym][centrality][delta][0]/Sigma[eta][etaSym][centrality][delta][1])
        axs[1].plot(X,Y,marker="o",color=colors[centrality-1])
    
    
    axs[0].set_xlabel(r"$\Delta$Centrality [%]")
    axs[0].set_ylabel(r"$\Sigma$")
    axs[1].set_ylabel(r"$\Sigma_F$/$\Sigma_B$")
    fig.suptitle(r"$\Sigma$ vs $\Delta$Centrality for $\Delta\eta=1.2$")
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    plt.savefig(dirName+"/sigma_vs_bin_width.pdf")
    pdf.savefig()
    plt.close()
    # Delta as a function of bin width for delta eta = 1.2
    eta = 0
    etaSym = 16-2-eta
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend()
    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Delta[eta][etaSym][centrality][delta][0])
        axs[0].plot(X,Y,marker="o",fillstyle="none",label = str(binCenter)+"%",color=colors[centrality-1])
    
    

    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Delta[eta][etaSym][centrality][delta][1])
        axs[0].plot(X,Y,marker="s",fillstyle="none",linestyle="dashed",color=colors[centrality-1])

    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Delta[eta][etaSym][centrality][delta][0]/Delta[eta][etaSym][centrality][delta][1])
        axs[1].plot(X,Y,marker="o",color=colors[centrality-1])
    
    
    axs[0].set_xlabel(r"$\Delta$Centrality [%]")
    axs[0].set_ylabel(r"$\Delta$")
    axs[1].set_ylabel(r"$\Delta_F$/$\Delta_B$")
    fig.suptitle(r"$\Delta$ vs $\Delta$Centrality for $\Delta\eta=1.2$")
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    plt.savefig(dirName+"/delta_vs_bin_width.pdf")
    pdf.savefig()
    plt.close()

    # Bcorr as a function of bin width for delta eta = 1.2
    eta = 0
    etaSym = 16-2-eta
    fig, axs = plt.subplots(2,1,height_ratios=[4,1],constrained_layout=True)
    dummy1, = axs[0].plot([],[],color = "black", label = FirstLabel)
    dummy2, = axs[0].plot([],[],color = "black", linestyle = "dashed", label = SecondLabel)
    axs[0].legend()
    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Bcorr[eta][etaSym][centrality][delta][0])
        axs[0].plot(X,Y,marker="o",fillstyle="none",label = str(binCenter)+"%",color=colors[centrality-1])
    
    

    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Bcorr[eta][etaSym][centrality][delta][1])
        axs[0].plot(X,Y,marker="s",fillstyle="none",linestyle="dashed",color=colors[centrality-1])

    for centrality in range(1,cMax):
        binCenter = 5*(2*centrality-1)
        X = []
        Y = []
        for delta in range(0,bMax):
            X.append(2*(delta+1))
            Y.append(Bcorr[eta][etaSym][centrality][delta][0]/Bcorr[eta][etaSym][centrality][delta][1])
        axs[1].plot(X,Y,marker="o",color=colors[centrality-1])
    
    
    axs[0].set_xlabel(r"$\Delta$Centrality [%]")
    axs[0].set_ylabel(r"$b_\text{corr}$")
    axs[1].set_ylabel(r"$b_{\text{corr}F}$/$b_{\text{corr}B}$")
    fig.suptitle(r"$b_\text{corr}$ vs $\Delta$Centrality for $\Delta\eta=1.2$")
    axs[0].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    axs[1].grid(visible=None, which='major', axis='both', linestyle='--',color="grey",alpha=0.5)
    fig.set_size_inches(6, 7)
    plt.savefig(dirName+"/bcorr_vs_bin_width.pdf")
    pdf.savefig()
    plt.close()
    
    


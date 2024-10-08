#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TF1.h>
#include <THnSparse.h>
#include <vector>
#include <fstream>

void sparseReader(){
   
   
   //Accessing the data from the THnSparse histogram in .root file
   TFile *f = TFile::Open("tAnalysis.root");
   TDirectoryFile *directory = (TDirectoryFile*)f->Get("fb_768");
   TList *list1 = (TList*)directory->Get("OutputList");   
   THnSparse *sHist = (THnSparse*)list1->FindObject("fhistQASparseD");
   
   
   //canvas declaration
   TCanvas c;
  c.Divide(3,3);
   std::string s1, s2;
   //names of variables (to make the titling of plots automatic)
   std::string names[5] = {"Eta","DCAz","Centrality","Pt","Phi"};
   // loop over quantities. 0 is Eta, 1 is DCAz, etc.
   c.Print("histograms_sparse.pdf[");
   for(int quantity = 0; quantity < 5; quantity++){
   
   if(quantity!=1 && quantity!=2){ // excluding DCAz and Centrality
   //Projecting the 5D histogram to a 2D histogram with relevant quantities
   TH2D *histogram = (TH2D*)sHist->Projection(quantity,2);
   
   //Printing the 2D histogram
   
   s1 = names[quantity]+" vs Centrality ";
   histogram->SetTitle(s1.c_str());
   c.cd(1);
   histogram->Draw();
   //s2 = names[quantity]+".png";
   //c.SaveAs(s2.c_str());

  
   //Declaring a histogram for later export. the no of bins, min and max values are taken from the Y axis of the 2D histogram.
   TH1F * hExport = new TH1F("hExport", ";;",histogram->GetNbinsY(),histogram->GetYaxis()->GetXmin(),histogram->GetYaxis()->GetXmax());
   

  //a loop over all centrality ranges
   for(int cIndex = 0; cIndex < 80;cIndex+=10){
   c.cd(cIndex/10 +2);
   std::cout << cIndex << std::endl;
   //a loop over histogram bin to be filled
   for(int k=1; k <= histogram->GetNbinsY();k++){
   
   //declaring the bin content
   double binContent = 0;
   
   //loop over all centrality bins
   for(int i=1; i <= histogram->GetNbinsX();i++){
      
        //check if Centrality is within desired range
        if(i>= cIndex && i<cIndex+10){
        //if so, increment the bin content
         binContent+=histogram->GetBinContent(i,k);
        }
      }
      //set the bin content
      hExport->SetBinContent(k,binContent);
   }
   //just some titles and file names
    s1 = names[quantity]+", "+std::to_string(cIndex)+"% < Centrality_V0A < "+std::to_string(cIndex+10)+"%";
    //s2 = names[quantity]+"_histogram_"+std::to_string(cIndex)+".pdf"; //this is for saving individual histograms
    
    
    hExport->SetTitle(s1.c_str());
    hExport->Draw();
    //Saving the canvas
    //c.SaveAs(s2.c_str());
     
    //Creating a new, blank histogram
    hExport = new TH1F("hExport", ";;",histogram->GetNbinsY(),histogram->GetYaxis()->GetXmin(),histogram->GetYaxis()->GetXmax());
   }
   
   c.Print("histograms_sparse.pdf");
   }
   
   }
   
   c.Print("histograms_sparse.pdf]");
}

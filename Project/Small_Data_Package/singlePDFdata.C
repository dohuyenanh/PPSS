#define TreeLRC_cxx
#include "TreeLRC.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TF1.h"
#include <vector>
#include <fstream>

void TreeLRC::Loop()
{
   if (fChain == 0)
      return;

   // Creating the canvas and the histogram
   TH1F *h1 = new TH1F("h1", ";# particles; # events", 16, 0, 16);
   TCanvas c;

   // At the end of the loop, these vectors will be used to create a CSV file
   std::vector<float> means;
   std::vector<float> rms;
   std::vector<int> eta_indices;
   std::vector<int> c_indices;

   c.Print("histograms_V0A_data.pdf[");
   // A loop over Centrality index
   for (int c_index = 0; c_index <= 100; c_index += 10)
   {
      // A loop over Eta index
      for (int index = 0; index < 16; index++)
      {

         Long64_t nentries = fChain->GetEntriesFast();

         Long64_t nbytes = 0, nb = 0;

         // A loop over Events
         for (Long64_t jentry = 0; jentry < nentries; jentry++)
         {
            Long64_t ientry = LoadTree(jentry);
            if (ientry < 0)
               break;
            nb = fChain->GetEntry(jentry);
            nbytes += nb;

            // Filling the histogram

            this->GetEntry(jentry);
            if (c_index == 0)
            {
               h1->Fill(this->N[index]);
            }
            else
            {
               if ((this->Centrality_V0A) > c_index - 10 && (this->Centrality_V0A) < c_index)
               {
                  h1->Fill(this->N[index]);
               };
            }
         }

         // Safety-check index print-out to see if the code works
         std::cout << index << std::endl;
         std::cout << c_index << std::endl;

         // setting the title of the histogram and the name and file extension
         std::string s1, s2;
         if (c_index == 0)
         {
            s1 = "N[j=" + std::to_string(index) + "]";
            s2 = std::to_string(index) + "_histogram_all.png";
         }
         else
         {
            s1 = "N[j=" + std::to_string(index) + "], " + std::to_string(c_index - 10) + "% < Centrality_V0A < " + std::to_string(c_index) + "%";
            s2 = std::to_string(index) + "_histogram_" + std::to_string(c_index) + ".png";
         }

         // Drawing the histogram in the canvas
         h1->Draw();
         h1->SetTitle(s1.c_str());
         // Saving the canvas
         c.Print("histograms_V0A_data.pdf");

         // Updating the CSV vectors
         means.push_back(h1->GetMean());
         rms.push_back(h1->GetRMS());
         eta_indices.push_back(index);
         c_indices.push_back(c_index);

         // Creating the new, empty histogram to fill it up in the next iteration of the loop
         h1 = new TH1F("h1", ";# particles; # events", 16, 0, 16);
      }
   }
   c.Print("histograms_V0A_data.pdf]");

   // Writing the means and rms to .CSV

   std::ofstream outFile("data_V0A.csv");
   outFile << "eta index";
   outFile << ",";
   outFile << "centrality index";
   outFile << ",";
   outFile << "mean";
   outFile << ",";
   outFile << "rms";
   outFile << "\n";
   for (int i = 0; i < means.size(); i++)
   {
      outFile << eta_indices.at(i);
      outFile << ",";
      outFile << c_indices.at(i);
      outFile << ",";
      outFile << means.at(i);
      outFile << ",";
      outFile << rms.at(i);
      if (i < means.size() - 1)
      {
         outFile << "\n";
      }
   }
   outFile.close();
}

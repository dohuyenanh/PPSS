#define TreeLRC_cxx
#include "TreeLRC.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TF1.h"
#include <vector>
#include <fstream>
#include <cmath>

// this method draws the histograms as individual files
void TreeLRC::Loop()
{
  if (fChain == 0)
    return;

  // Creating the canvas and the histogram
  TH1F *h1 = new TH1F("h1", ";# particles; # events", 50, 0, 50);
  TCanvas c;

  // At the end of the loop, these vectors will be used to create a CSV file
  std::vector<float> means;
  std::vector<float> rms;
  std::vector<int> eta_indices;
  std::vector<int> c_indices;

  // A loop over Eta index
  for (int index = 0; index < 16; index++)
  {
    // A loop over Centrality index
    for (int c_index = 0; c_index <= 0; c_index += 10)
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
          h1->Fill(N[index]);
        }
        else
        {
          if ((Centrality_V0A) > c_index - 10 && (Centrality_V0A) < c_index)
          {
            h1->Fill(N[index]);
          };
        }
      }

      // Safety-check index print-out to see if the code works
      std::cout << index << std::endl;

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
      c.SaveAs(s2.c_str());

      // Updating the CSV vectors
      means.push_back(h1->GetMean());
      rms.push_back(h1->GetRMS());
      eta_indices.push_back(index);
      c_indices.push_back(c_index);

      // Creating the new, empty histogram to fill it up in the next iteration of the loop
      h1 = new TH1F("h1", ";# particles; # events", 50, 0, 50);
    }
  }

  // Writing the means and rms to .CSV

  std::ofstream outFile("data_V0A_Loop.csv");
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

void TreeLRC::Arrayed()
{

  if (fChain == 0)
    return;

  // Creating the canvas
  TCanvas c;
  c.Divide(4, 4);

  // At the end of the loop, these vectors will be used to create a CSV file
  int etaMax = 16;
  int cMax = 1;
  TH1F *allHistograms[etaMax][cMax];
  for (int c_index = 0; c_index < cMax; c_index ++)
  {
    // A loop over Eta index
    for (int index = 0; index < etaMax; index++)
    {
      std::string s1;
      if (c_index == 0)
      {
        s1 = "N[j=" + std::to_string(index) + "]";
      }
      else
      {
        s1 = "N[j=" + std::to_string(index) + "], " + std::to_string(c_index - 10) + "% < Centrality_V0M < " + std::to_string(c_index) + "%";
      }
      allHistograms[index][c_index] = new TH1F("h1", ";# particles; # events", 50, 0, 50);
      allHistograms[index][c_index]->SetTitle(s1.c_str());
    }}

  std::cout << "It works" << std::endl;

  ///up to here it works  
  
  
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
// A loop over Centrality index
  for (int c_index = 0; c_index < cMax; c_index ++)
  {
    // A loop over Eta index
    for (int index = 0; index < etaMax; index++)
    {
      
        // Filling the histogram

        this->GetEntry(jentry);
        if (c_index == 0)
        {
          allHistograms[index][0]->Fill(N[index]);
        }
        else
        {
          if ((Centrality_V0M) > c_index*10 - 10 && (Centrality_V0M) < c_index*10)
          {
            allHistograms[index][c_index]->Fill(N[index]);
          };
        }
      }}


      // setting the title of the histogram and the name and file extension
      /* std::string s1, s2;
      if (c_index == 0)
      {
        s1 = "N[j=" + std::to_string(index) + "]";
        s2 = std::to_string(index) + "_histogram_all.png";
      }
      else
      {
        s1 = "N[j=" + std::to_string(index) + "], " + std::to_string(c_index - 10) + "% < Centrality_V0M < " + std::to_string(c_index) + "%";
        s2 = std::to_string(index) + "_histogram_" + std::to_string(c_index) + ".png";
      } */

      
    

    
  }
  
  c.Print("histograms_V0M.pdf[");
  // A loop over Centrality index
  for (int c_index = 0; c_index < cMax; c_index ++)
  {
    // A loop over Eta index
    for (int index = 0; index < etaMax; index++)
    {
  // changing the placement in canvas
  TVirtualPad *p1 = c.cd(index + 1);
  p1->SetLogy();
  
  allHistograms[index][c_index]->Draw();
    }
    c.Print("histograms_V0M.pdf");
    }
  c.Print("histograms_V0M.pdf]");

  // Writing the means and rms to .CSV

}

// the efficient method: about 18 seconds to compile
void TreeLRC::Means()
{

  if (fChain == 0)
    return;

  //  # of eta bins
  int etaMax = 16;
  // # of centrality intervals. centrality = 0 is all centralities, 1 is 0%-10%, 2 is 10%-20%, etc.
  int cMax = 9;
  // the arrays for storing the # of events and # of particles

  //
  int covMax = 16;

  double nEvents[etaMax][cMax];
  double nParticles[etaMax][cMax];
  double nParticles2[etaMax][cMax];
  double vars[etaMax][cMax];
  double nCovs[covMax][cMax];
  for (int index = 0; index < covMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      nCovs[index][c_index] = 0;
    }
  }

  // setting the initial values in arrays to 0 - without it some of the means are calculated incorrectly due to memory issues
  for (int index = 0; index < etaMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      nParticles[index][c_index] = 0;
      nParticles2[index][c_index] = 0;
      nEvents[index][c_index] = 0;
      vars[index][c_index] = 0;
    }
  }

  Long64_t nentries = fChain->GetEntriesFast();

  Long64_t nbytes = 0, nb = 0;

  // A loop over Events for means
  for (Long64_t jentry = 0; jentry < nentries; jentry++)
  {

    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0)
      break;
    nb = fChain->GetEntry(jentry);
    nbytes += nb;

    this->GetEntry(jentry);

    for (int index = 0; index < etaMax; index++)
    {

      // incrementing the values of # of events and # of particles for centrality = 0 (all centralities)
      nEvents[index][0]++;
      nParticles[index][0] += (double)(N[index]);

      if (Centrality_V0A < 80)
      {

        // incrementing the values of # of events and # of particles for specific centralities
        //  the index is calculated like I showed you in the notebook:
        //  if the centrality of an event is 38.7 then it should go to index 4 (range 30%-40%)
        //  floor(38.7/10+1) = floor(4.87) = 4
        int c_index = (int)(Centrality_V0A / 10) + 1;
        nEvents[index][c_index]++;
        nParticles[index][c_index] += (double)(N[index]);
      }
    }

    // this is just to check if the code runs properly: it prints out a number once every 100000 events
    // if(jentry%100000 == 0){
    // std::cout << jentry/100000 << std::endl;
    //}
  }

  // calculating the mean

  double means[etaMax][cMax];
  for (int index = 0; index < etaMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      means[index][c_index] = nParticles[index][c_index] / nEvents[index][c_index];
      // optional print-out
      // std::cout << "i: "+std::to_string(index)+" c: "+std::to_string(c_index)+" m: "+std::to_string(means[index][c_index])+" p: "+std::to_string(nParticles[index][c_index])+" e: " +std::to_string(nEvents[index][c_index])<< std::endl;
    }
  }

  // A loop over Events for standard deviation and covariance
  for (Long64_t jentry = 0; jentry < nentries; jentry++)
  {

    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0)
      break;
    nb = fChain->GetEntry(jentry);
    nbytes += nb;

    this->GetEntry(jentry);

    for (int index = 0; index < etaMax; index++)
    {

      // incrementing the values of # of events and # of particles for centrality = 0 (all centralities)

      nParticles2[index][0] += ((double)(N[index]) - means[index][0]) * ((double)(N[index]) - means[index][0]);
      nCovs[index][0] += ((double)(N[index]) - means[index][0]) * ((double)(N[etaMax - 1 - index]) - means[etaMax - 1 - index][0]);
      if (Centrality_V0A < 80)
      {

        // incrementing the values of # of events and # of particles for specific centralities
        //  the index is calculated like I showed you in the notebook:
        //  if the centrality of an event is 38.7 then it should go to index 4 (range 30%-40%)
        //  floor(38.7/10+1) = floor(4.87) = 4
        int c_index = (int)floor(Centrality_V0A / 10 + 1);

        nParticles2[index][c_index] += ((double)(N[index]) - means[index][c_index]) * ((double)(N[index]) - means[index][c_index]);
        nCovs[index][c_index] += ((double)(N[index]) - means[index][c_index]) * ((double)(N[etaMax - 1 - index]) - means[etaMax - 1 - index][c_index]);
      }
    }
    // for(int index = 0; index < covMax; index++){
    // int c_index = (int)floor(Centrality_V0A/10+1);

    //}

    // this is just to check if the code runs properly: it prints out a number once every 100000 events
    // if(jentry%100000 == 0){
    // std::cout << jentry/100000 << std::endl;
    //}
  }

  // calculating the standard deviation

  for (int index = 0; index < etaMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      // this is actually the standard deviation, not the variance
      vars[index][c_index] = sqrt(nParticles2[index][c_index] / (nEvents[index][c_index]));
      // std::cout << "i: "+std::to_string(index)+" c: "+std::to_string(c_index)+" m: "+std::to_string(means[index][c_index])+" std: "+std::to_string(vars[index][c_index])+" p2: "+std::to_string(nParticles2[index][c_index])+" e: " +std::to_string(nEvents[index][c_index])<< std::endl;
    }
  }
  // calculating covariance
  double covs[covMax][cMax];
  for (int index = 0; index < covMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      covs[index][c_index] = nCovs[index][c_index] / (nEvents[index][c_index]);
      // optional print-out
      // std::cout << "i: "+std::to_string(index)+" c: "+std::to_string(c_index)+" cov: "+std::to_string(covs[index][c_index])+" nCovs: "+std::to_string(nCovs[index][c_index])+" e1: " +std::to_string(nEvents[index][c_index]) +" e2: " +std::to_string(nEvents[etaMax-1-index][c_index]) << std::endl;
    }
  }

  // Writing the means and rms to .CSV
  std::ofstream outFile("data_V0A_Means_Fast.csv");
  outFile << "eta index";
  outFile << ",";
  outFile << "centrality index";
  outFile << ",";
  outFile << "mean";
  outFile << ",";
  outFile << "rms";
  outFile << "\n";
  for (int index = 0; index < etaMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      outFile << index;
      outFile << ",";
      outFile << c_index;
      outFile << ",";
      outFile << means[index][c_index];
      outFile << ",";
      outFile << vars[index][c_index];
      if (index < etaMax - 1 || c_index < cMax - 1)
      {
        outFile << "\n";
      }
    }
  }

  outFile.close();

  // Writing the covs to .CSV
  std::ofstream outFile2("data_V0A_covs_Fast.csv");
  outFile2 << "eta index";
  outFile2 << ",";
  outFile2 << "centrality index";
  outFile2 << ",";
  outFile2 << "covariance";
  outFile2 << "\n";
  for (int index = 0; index < covMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      outFile2 << index;
      outFile2 << ",";
      outFile2 << c_index;
      outFile2 << ",";
      outFile2 << covs[index][c_index];
      if (index < covMax - 1 || c_index < cMax - 1)
      {
        outFile2 << "\n";
      }
    }
  }

  outFile2.close();
  // Below: covariances

  // 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15
}

// time ~15 sec
void TreeLRC::MeansMoments()
{

  if (fChain == 0)
    return;

  //  # of eta bins
  int etaMax = 16;
  // # of centrality intervals. centrality = 0 is all centralities, 1 is 0%-10%, 2 is 10%-20%, etc.
  int cMax = 9;
  // the arrays for storing the # of events and # of particles

  //
  int covMax = 16;

  double nEvents[etaMax][cMax];
  double nParticles[etaMax][cMax];
  double nParticles2[etaMax][cMax];
  double nParticlesXY[covMax][cMax];

  // setting the initial values in arrays to 0 - without it some of the means are calculated incorrectly due to memory issues
  for (int c_index = 0; c_index < cMax; c_index++)
  {
    for (int index = 0; index < etaMax; index++)
    {
      nParticlesXY[index][c_index] = 0;
      nParticles[index][c_index] = 0;
      nParticles2[index][c_index] = 0;
      nEvents[index][c_index] = 0;
    }
  }

  Long64_t nentries = fChain->GetEntriesFast();

  Long64_t nbytes = 0, nb = 0;

  // A loop over Events for means
  for (Long64_t jentry = 0; jentry < nentries; jentry++)
  {

    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0)
      break;
    nb = fChain->GetEntry(jentry);
    nbytes += nb;

    this->GetEntry(jentry);

    for (int index = 0; index < etaMax; index++)
    {

      // incrementing the values of # of events and # of particles for centrality = 0 (all centralities)
      nEvents[index][0]++;
      nParticles[index][0] += (double)(N[index]);
      nParticles2[index][0] += (double)(N[index]) * (double)(N[index]);
      nParticlesXY[index][0] += (double)(N[index]) * (double)(N[etaMax - 1 - index]);

      if (Centrality_V0A < 80)
      {

        // incrementing the values of # of events and # of particles for specific centralities
        //  the index is calculated like I showed you in the notebook:
        //  if the centrality of an event is 38.7 then it should go to index 4 (range 30%-40%)
        //  floor(38.7/10+1) = floor(4.87) = 4
        int c_index = (int)(Centrality_V0A / 10) + 1;
        nEvents[index][c_index]++;
        nParticles[index][c_index] += (double)(N[index]);
        // for (int index2 = 0; index2 < etaMax; index2++){

        //}
        nParticles2[index][c_index] += (double)(N[index]) * (double)(N[index]);
        nParticlesXY[index][c_index] += (double)(N[index]) * (double)(N[etaMax - 1 - index]);

        // index = 0
        // 16-1-0 = 15
        // index = 15
        // 16-1-15=0
      }

      // this is just to check if the code runs properly: it prints out a number once every 100000 events
      // if(jentry%100000 == 0){
      // std::cout << jentry/100000 << std::endl;
      //}
    }
  }

  // calculating the mean, vars and covariances

  double means[etaMax][cMax];
  double vars[etaMax][cMax];
  double covs[covMax][cMax];
  double sndmoment[etaMax][cMax];
  double xymoment[etaMax][cMax];
  for (int index = 0; index < etaMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      means[index][c_index] = nParticles[index][c_index] / nEvents[index][c_index];
      // E[x^2]-E[x]^2
      vars[index][c_index] = nParticles2[index][c_index] / (nEvents[index][c_index]) - means[index][c_index] * means[index][c_index];
      sndmoment[index][c_index] = nParticles2[index][c_index] / (nEvents[index][c_index]);
      xymoment[index][c_index] = nParticlesXY[index][c_index] / (nEvents[index][c_index]);
    }
  }

  for (int index = 0; index < etaMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      // if(index<covMax){
      covs[index][c_index] = nParticlesXY[index][c_index] / (nEvents[index][c_index]) - means[index][c_index] * means[etaMax - 1 - index][c_index];

      // optional print-out
      // std::cout << "i: "+std::to_string(index)+" c: "+std::to_string(c_index)+" cov: "+std::to_string(covs[index][c_index])+" XY: "+std::to_string(nParticlesXY[index][c_index])+" e1: " +std::to_string(nEvents[index][c_index]) +" e2: " +std::to_string(nEvents[etaMax-1-index][c_index]) +" m1: "+std::to_string(means[index][c_index])+" m2: "+std::to_string(means[etaMax-1-index][c_index]) << std::endl;
      // }
    }
  }

  // calculating the Sigma

  double Sigma[etaMax][cMax];
  double Delta[etaMax][cMax];
  double Bcorr[etaMax][cMax];
  float cov, mean, meanSym, var, varSym, omega, omegaSym;
  for (int index = 0; index < 16; index++)
  {
    for (int c_index = 0; c_index < 9; c_index++)
    {
      int indexSym = 16 - 1 - index;
      mean = means[index][c_index];
      meanSym = means[indexSym][c_index];
      var = vars[index][c_index];
      varSym = vars[indexSym][c_index];
      omega = var / mean;
      omegaSym = varSym / meanSym;
      cov = covs[index][c_index];

      Sigma[index][c_index] = (mean * omegaSym + meanSym * omega - 2 * cov) / (mean + meanSym);
      Delta[index][c_index] = (mean * omegaSym - meanSym * omega) / (mean - meanSym);
      Bcorr[index][c_index] = cov / sqrt(var * varSym);
    }
  }

  // Writing the means and rms to .CSV
  std::ofstream outFile("data_V0A_Means_Final.csv");
  outFile << "eta index";
  outFile << ",";
  outFile << "centrality index";
  outFile << ",";
  outFile << "mean";
  outFile << ",";
  outFile << "var";
  outFile << ",";
  outFile << "cov";
  outFile << ",";
  outFile << "Sigma";
  outFile << ",";
  outFile << "Delta";
  outFile << ",";
  outFile << "Bcorr";
  outFile << "\n";
  for (int index = 0; index < etaMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      outFile << index;
      outFile << ",";
      outFile << c_index;
      outFile << ",";
      outFile << means[index][c_index];
      outFile << ",";
      outFile << vars[index][c_index];
      outFile << ",";
      outFile << covs[index][c_index];
      outFile << ",";
      outFile << Sigma[index][c_index];
      outFile << ",";
      outFile << Delta[index][c_index];
      outFile << ",";
      outFile << Bcorr[index][c_index];
      if (index < etaMax - 1 || c_index < cMax - 1)
      {
        outFile << "\n";
      }
    }
  }

  outFile.close();
}

void TreeLRC::Asymmetric()
{

  if (fChain == 0)
    return;

  //  # of eta bins
  int etaMax = 16;
  // # of centrality intervals + 1 (0 is for all centralities)
  int cMax = 9;
  // the arrays for storing the # of events and # of particles
  //
  double nEvents[etaMax][cMax];
  double nParticles[etaMax][cMax];
  double nParticlesXY[etaMax][etaMax][cMax];

  // setting the initial values in arrays to 0 - without it some of the means are calculated incorrectly due to memory issues
  for (int c_index = 0; c_index < cMax; c_index++)
  {
    for (int index = 0; index < etaMax; index++)
    {
      for (int index2 = 0; index2 < etaMax; index2++)
      {
        nParticlesXY[index][index2][c_index] = 0;
      }
      nParticles[index][c_index] = 0;
      nEvents[index][c_index] = 0;
    }
  }

  Long64_t nentries = fChain->GetEntriesFast();

  Long64_t nbytes = 0, nb = 0;

  // A loop over Events for means
  for (Long64_t jentry = 0; jentry < nentries; jentry++)
  {

    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0)
      break;
    nb = fChain->GetEntry(jentry);
    nbytes += nb;

    this->GetEntry(jentry);

    for (int index = 0; index < etaMax; index++)
    {

      // incrementing the values of # of events and # of particles for centrality = 0 (all centralities)
      nEvents[index][0]++;
      nParticles[index][0] += (double)(N[index]);
      for (int index2 = 0; index2 < etaMax; index2++)
      {
        nParticlesXY[index][index2][0] += (double)(N[index]) * (double)(N[index2]);
      }

      if (Centrality_V0A < 80)
      {

        // incrementing the values of # of events and # of particles for specific centralities
        //  the index is calculated as: index = floor[centrality * cMax-1 (number of centrality bins) / 80 (full range of centrality) ] + 1
        int c_index = (int)(Centrality_V0A * (cMax - 1) / 80) + 1;
        nEvents[index][c_index]++;
        nParticles[index][c_index] += (double)(N[index]);

        for (int index2 = 0; index2 < etaMax; index2++)
        {
          nParticlesXY[index][index2][c_index] += (double)(N[index]) * (double)(N[index2]);
        }
      }

      // this is just to check if the code runs properly: it prints out a number once every 100000 events
      // if(jentry%100000 == 0){
      // std::cout << jentry/100000 << std::endl;
      //}
    }
  }

  // calculating the mean, vars and covariances

  double means[etaMax][cMax];
  double covs[etaMax][etaMax][cMax];
  for (int index = 0; index < etaMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      means[index][c_index] = nParticles[index][c_index] / nEvents[index][c_index];
    }
  }

  for (int index = 0; index < etaMax; index++)
  {
    for (int index2 = 0; index2 < etaMax; index2++)
    {
      for (int c_index = 0; c_index < cMax; c_index++)
      {
        // covariance = E[XY] - E[X]E[Y]
        covs[index][index2][c_index] = nParticlesXY[index][index2][c_index] / (nEvents[index][c_index]) - means[index][c_index] * means[index2][c_index];

        // optional print-out
        // std::cout << "i: "+std::to_string(index)+" c: "+std::to_string(c_index)+" cov: "+std::to_string(covs[index][c_index])+" XY: "+std::to_string(nParticlesXY[index][c_index])+" e1: " +std::to_string(nEvents[index][c_index]) +" e2: " +std::to_string(nEvents[etaMax-1-index][c_index]) +" m1: "+std::to_string(means[index][c_index])+" m2: "+std::to_string(means[etaMax-1-index][c_index]) << std::endl;
        // }
      }
    }
  }

  // calculating the Sigma, Delta, and Bcorr

  double Sigma[etaMax][etaMax][cMax];
  double Delta[etaMax][etaMax][cMax];
  double Bcorr[etaMax][etaMax][cMax];
  float cov, mean1, mean2, var1, var2, omega1, omega2;
  for (int index = 0; index < etaMax; index++)
  {
    for (int index2 = 0; index2 < etaMax; index2++)
    {
      for (int c_index = 0; c_index < cMax; c_index++)
      {
        mean1 = means[index][c_index];
        mean2 = means[index2][c_index];
        var1 = covs[index][index][c_index];
        var2 = covs[index2][index2][c_index];
        omega1 = var1 / mean1;
        omega2 = var2 / mean2;
        cov = covs[index][index2][c_index];

        Sigma[index][index2][c_index] = (mean1 * omega2 + mean2 * omega1 - 2 * cov) / (mean1 + mean2);
        Delta[index][index2][c_index] = (mean1 * omega2 - mean2 * omega1) / (mean1 - mean2);
        Bcorr[index][index2][c_index] = cov / sqrt(var1 * var2);
      }
    }
  }

  // Writing the means and rms to .CSV
  std::ofstream outFile("data_V0A_Asymmetric.csv");
  outFile << "eta index 1";
  outFile << ",";
  outFile << "eta index 2";
  outFile << ",";
  outFile << "centrality index";
  outFile << ",";
  outFile << "mean 1";
  outFile << ",";
  outFile << "mean 2";
  outFile << ",";
  outFile << "cov";
  outFile << ",";
  outFile << "Sigma";
  outFile << ",";
  outFile << "Delta";
  outFile << ",";
  outFile << "Bcorr";
  outFile << "\n";
  for (int index = 0; index < etaMax; index++)
  {
    for (int index2 = 0; index2 < etaMax; index2++)
    {
      for (int c_index = 0; c_index < cMax; c_index++)
      {
        outFile << index;
        outFile << ",";
        outFile << index2;
        outFile << ",";
        outFile << c_index;
        outFile << ",";
        outFile << means[index][c_index];
        outFile << ",";
        outFile << means[index2][c_index];
        outFile << ",";
        outFile << covs[index][index2][c_index];
        outFile << ",";
        outFile << Sigma[index][index2][c_index];
        outFile << ",";
        outFile << Delta[index][index2][c_index];
        outFile << ",";
        outFile << Bcorr[index][index2][c_index];
        if (index < etaMax - 1 || index2 < etaMax - 1 || c_index < cMax - 1)
        {
          outFile << "\n";
        }
      }
    }
  }
  outFile.close();
}

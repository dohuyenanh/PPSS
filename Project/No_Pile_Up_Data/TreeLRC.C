#define TreeLRC_cxx
#include "TreeLRC.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "TF1.h"
#include <vector>
#include <fstream>
#include <cmath>

bool isHalfInteger(double num)
{
  double twice_num = num * 2;
  return std::floor(twice_num) == twice_num;
}

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
          h1->Fill(this->N[index]);
        }
        else
        {
          if ((this->Centrality_ZNA) > c_index - 10 && (this->Centrality_ZNA) < c_index)
          {
            h1->Fill(this->N[index]);
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
        s1 = "N[j=" + std::to_string(index) + "], " + std::to_string(c_index - 10) + "% < Centrality_ZNA < " + std::to_string(c_index) + "%";
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

  std::ofstream outFile("data_ZNA_Loop.csv");
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
  int etaMax = 1;
  int cMax = 9;
  TH1F *allHistograms[etaMax][cMax];
  for (int c_index = 0; c_index < cMax; c_index++)
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
        s1 = "N[j=" + std::to_string(index) + "], " + std::to_string(c_index - 10) + "% < Centrality_ZNA < " + std::to_string(c_index) + "%";
      }
      allHistograms[index][c_index] = new TH1F("h1", ";# particles; # events", 50, 0, 50);
      allHistograms[index][c_index]->SetTitle(s1.c_str());
    }
  }

  std::cout << "It works" << std::endl;

  /// up to here it works

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
    for (int c_index = 0; c_index < cMax; c_index++)
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
          if ((Centrality_ZNA) > c_index * 10 - 10 && (Centrality_ZNA) < c_index * 10)
          {
            allHistograms[index][c_index]->Fill(N[index]);
          };
        }
      }
    }
    // this is just to check if the code runs properly: it prints out a number once every 1000000 events
    if (jentry % 100000 == 0)
    {
      std::cout << jentry / 100000 << std::endl;
    }
  }

  c.Print("histograms_ZNA.pdf[");
  // A loop over Centrality index
  for (int c_index = 0; c_index < cMax; c_index++)
  {
    // A loop over Eta index
    for (int index = 0; index < etaMax; index++)
    {
      // changing the placement in canvas
      TVirtualPad *p1 = c.cd(index + 1);
      p1->SetLogy();

      allHistograms[index][c_index]->Draw();
    }
    c.Print("histograms_ZNA.pdf");
  }
  c.Print("histograms_ZNA.pdf]");

  // Writing the means and rms to .CSV
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
  int bMax = 5; // bins width for centrality
  // delta = 0 is for bin width = 2
  // delta = 1 is for bin width = 4
  //...
  // delta = delta is for bin width 2*(delta+1)

  double nEvents[etaMax][cMax][bMax];
  double nParticles[etaMax][cMax][bMax];
  double nParticlesXY[etaMax][etaMax][cMax][bMax];

  // setting the initial values in arrays to 0 - without it some of the means are calculated incorrectly due to memory issues
  for (int c_index = 0; c_index < cMax; c_index++)
  {
    for (int delta = 0; delta < bMax; delta++)
    {

      for (int index = 0; index < etaMax; index++)
      {
        for (int index2 = 0; index2 < etaMax; index2++)
        {
          nParticlesXY[index][index2][c_index][delta] = 0;
        }
        nParticles[index][c_index][delta] = 0;
        nEvents[index][c_index][delta] = 0;
      }
    }
  }
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
    this->GetEntry(jentry);
    if (/* abs(VertexZ) < 7 && abs(VertexZ) > 0.15 && pileupmv == 0 && pileupspd == 0 */ true)
    {

      for (int index = 0; index < etaMax; index++)
      {

        // incrementing the values of # of events and # of particles for centrality = 0 (all centralities)
        nEvents[index][0][0]++;
        nParticles[index][0][0] += (double)(N[index]);
        for (int index2 = 0; index2 < etaMax; index2++)
        {
          nParticlesXY[index][index2][0][0] += (double)(N[index]) * (double)(N[index2]);
        }

        if (Centrality_ZNA < 80)
        {

          // incrementing the values of # of events and # of particles for specific centralities
          //  the index is calculated as: index = floor[centrality * cMax-1 (number of centrality bins) / 80 (full range of centrality) ] + 1
          int c_index = (int)(Centrality_ZNA * (cMax - 1) / 80) + 1;
          float binCenter = (2 * c_index - 1) * 80 / (2 * (cMax - 1));
          for (int delta = 0; delta < bMax; delta++)
          {

            if (abs(Centrality_ZNA - binCenter) <= delta + 1)
            {
              nEvents[index][c_index][delta]++;
              nParticles[index][c_index][delta] += (double)(N[index]);

              for (int index2 = 0; index2 < etaMax; index2++)
              {
                nParticlesXY[index][index2][c_index][delta] += (double)(N[index]) * (double)(N[index2]);
              }
            }
          }
        }
      }
    }
    // this is just to check if the code runs properly: it prints out a number once every 1000000 events
    if (jentry % 1000000 == 0)
    {
      std::cout << jentry / 1000000 << std::endl;
    }
  }

  for (int delta = 1; delta < bMax; delta++)
  {
    for (int index = 0; index < etaMax; index++)
    {
      nEvents[index][0][delta] = nEvents[index][0][0];
      nParticles[index][0][delta] = nParticles[index][0][0];
      for (int index2 = 0; index2 < etaMax; index2++)
      {
        nParticlesXY[index][index2][0][delta] = nParticlesXY[index][index2][0][0];
        ;
      }
    }
  }
  // calculating the mean, vars and covariances

  double means[etaMax][cMax][bMax];
  double covs[etaMax][etaMax][cMax][bMax];
  for (int index = 0; index < etaMax; index++)
  {
    for (int c_index = 0; c_index < cMax; c_index++)
    {
      for (int delta = 0; delta < bMax; delta++)
      {
        means[index][c_index][delta] = nParticles[index][c_index][delta] / nEvents[index][c_index][delta];
      }
    }
  }
  for (int index = 0; index < etaMax; index++)
  {
    for (int index2 = 0; index2 < etaMax; index2++)
    {
      for (int c_index = 0; c_index < cMax; c_index++)
      {
        for (int delta = 0; delta < bMax; delta++)
        {
          // covariance = E[XY] - E[X]E[Y]
          covs[index][index2][c_index][delta] = nParticlesXY[index][index2][c_index][delta] / (nEvents[index][c_index][delta]) - means[index][c_index][delta] * means[index2][c_index][delta];

          // optional print-out
          // std::cout << "i: "+std::to_string(index)+" c: "+std::to_string(c_index)+" cov: "+std::to_string(covs[index][c_index])+" XY: "+std::to_string(nParticlesXY[index][c_index])+" e1: " +std::to_string(nEvents[index][c_index]) +" e2: " +std::to_string(nEvents[etaMax-1-index][c_index]) +" m1: "+std::to_string(means[index][c_index])+" m2: "+std::to_string(means[etaMax-1-index][c_index]) << std::endl;
          // }
        }
      }
    }
  }

  // calculating the Sigma, Delta, and Bcorr

  double Sigma[etaMax][etaMax][cMax][bMax];
  double Delta[etaMax][etaMax][cMax][bMax];
  double Bcorr[etaMax][etaMax][cMax][bMax];
  float cov, mean1, mean2, var1, var2, omega1, omega2;
  for (int index = 0; index < etaMax; index++)
  {
    for (int delta = 0; delta < bMax; delta++)
    {
      for (int index2 = 0; index2 < etaMax; index2++)
      {
        for (int c_index = 0; c_index < cMax; c_index++)
        {
          mean1 = means[index][c_index][delta];
          mean2 = means[index2][c_index][delta];
          var1 = covs[index][index][c_index][delta];
          var2 = covs[index2][index2][c_index][delta];
          omega1 = var1 / mean1;
          omega2 = var2 / mean2;
          cov = covs[index][index2][c_index][delta];

          Sigma[index][index2][c_index][delta] = (mean1 * omega2 + mean2 * omega1 - 2 * cov) / (mean1 + mean2);
          Delta[index][index2][c_index][delta] = (mean1 * omega2 - mean2 * omega1) / (mean1 - mean2);
          Bcorr[index][index2][c_index][delta] = cov / sqrt(var1 * var2);
        }
      }
    }
  }

  // Writing the means and rms to .CSV
  std::ofstream outFile("Pile_ZNA_NoCut_NoPile.csv");
  outFile << "eta index 1";
  outFile << ",";
  outFile << "eta index 2";
  outFile << ",";
  outFile << "centrality index";
  outFile << ",";
  outFile << "bin width";
  outFile << ",";
  outFile << "# Particles";
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
        for (int delta = 0; delta < bMax; delta++)
        {
          outFile << index;
          outFile << ",";
          outFile << index2;
          outFile << ",";
          outFile << c_index;
          outFile << ",";
          outFile << delta;
          outFile << ",";
          outFile << nParticles[index][c_index][delta];
          outFile << ",";
          outFile << means[index][c_index][delta];
          outFile << ",";
          outFile << means[index2][c_index][delta];
          outFile << ",";
          outFile << covs[index][index2][c_index][delta];
          outFile << ",";
          outFile << Sigma[index][index2][c_index][delta];
          outFile << ",";
          outFile << Delta[index][index2][c_index][delta];
          outFile << ",";
          outFile << Bcorr[index][index2][c_index][delta];
          if (index < etaMax - 1 || index2 < etaMax - 1 || c_index < cMax - 1 || delta < bMax - 1)
          {
            outFile << "\n";
          }
        }
      }
    }
  }
  outFile.close();
}

void TreeLRC::Events()
{
  if (fChain == 0)
    return;

  int noPile1 = 0; // no pile-up by default
  int noPile2 = 0; // no pile-up using MV and SPD
  int stdCut = 0;  // standard cut: |VertexZ| < 10
  int extCut = 0;  // extended cut: |VertexZ| < 7 && |VertexZ| > 0.15
  int cV0A = 0;    // centrality selection on V0A
  int cZNA = 0;    // centrality selection on ZNA
  //std::vector<int> runNum;

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
    this->GetEntry(jentry);
    if (RunNumber != 265343)
    {

      noPile1++;
      if (pileupmv == 0 && pileupspd == 0)
      {
        noPile2++;
        if (abs(VertexZ) < 10)
        {
          stdCut++;
          if (abs(VertexZ) < 7 && abs(VertexZ) > 0.15)
          {
            extCut++;
            if (Centrality_V0A < 80)
            {
              cV0A++;
            }
            if (Centrality_ZNA < 80)
            {
              cZNA++;
            }
          }
        }
      }

      // this is just to check if the code runs properly: it prints out a number once every 1000000 events
      if (jentry % 1000000 == 0)
      {
        std::cout << jentry / 1000000 << std::endl;
      }
    }
  }
  std::ofstream outFile("Events.csv");
  outFile << "with pile-up";
  outFile << ",";
  outFile << "no pile-up by default";
  outFile << ",";
  outFile << "no pile-up using MV and SPD";
  outFile << ",";
  outFile << "standard cut";
  outFile << ",";
  outFile << "extended cut";
  outFile << ",";
  outFile << "Centrality_V0A < 80";
  outFile << ",";
  outFile << "Centrality_ZNA < 80";
  outFile << "\n";
  outFile << ",";
  outFile << noPile1;
  outFile << ",";
  outFile << noPile2;
  outFile << ",";
  outFile << stdCut;
  outFile << ",";
  outFile << extCut;
  outFile << ",";
  outFile << cV0A;
  outFile << ",";
  outFile << cZNA;

  outFile.close();

}

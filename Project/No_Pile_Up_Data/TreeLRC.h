//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Jul 25 12:17:27 2024 by ROOT version 6.32.02
// from TTree TreeLRC/
// found on file: AnalysisResults_noPileUp.root
//////////////////////////////////////////////////////////

#ifndef TreeLRC_h
#define TreeLRC_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class TreeLRC {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Int_t           RunNumber;
   Float_t         VertexZ;
   Float_t         Centrality_V0M;
   Float_t         Centrality_V0A;
   Float_t         Centrality_V0C;
   Float_t         Centrality_ZNA;
   Float_t         Centrality_ZNC;
   Float_t         Centrality_V0Mminus05;
   Float_t         Centrality_TRK;
   Float_t         Centrality_ZEMvsZDC;
   Float_t         Centrality_V0M_GetCentrality;
   Float_t         Centrality_b;
   Float_t         MagneticFiled;
   Short_t         N[16];
   Float_t         multV0A;
   Float_t         multV0C;
   Short_t         partZDC;
   Bool_t          pileupspd;
   //if TRUE, event is pile up
   Bool_t          pileupmv;

   // List of branches
   TBranch        *b_RunNumber;   //!
   TBranch        *b_VertexZ;   //!
   TBranch        *b_Centrality;   //!
   TBranch        *b_MagneticFiled;   //!
   TBranch        *b_n;   //!
   TBranch        *b_multV0A;   //!
   TBranch        *b_multV0C;   //!
   TBranch        *b_partZDC;   //!
   TBranch        *b_pileupspd;   //!
   TBranch        *b_pileupmv;   //!

   TreeLRC(TTree *tree=0);
   virtual ~TreeLRC();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   // virtual void     Means();
   virtual void     Arrayed();
   // virtual void     MeansMoments();
   virtual void     Asymmetric();
   virtual void     Events();
   virtual bool     Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef TreeLRC_cxx
TreeLRC::TreeLRC(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("AnalysisResults_noPileUp.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("AnalysisResults_noPileUp.root");
      }
      TDirectory * dir = (TDirectory*)f->Get("AnalysisResults_noPileUp.root:/fb_768");
      dir->GetObject("TreeLRC",tree);

   }
   Init(tree);
}

TreeLRC::~TreeLRC()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t TreeLRC::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t TreeLRC::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void TreeLRC::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("RunNumber", &RunNumber, &b_RunNumber);
   fChain->SetBranchAddress("VertexZ", &VertexZ, &b_VertexZ);
   fChain->SetBranchAddress("Centrality", &Centrality_V0M, &b_Centrality);
   fChain->SetBranchAddress("MagneticFiled", &MagneticFiled, &b_MagneticFiled);
   fChain->SetBranchAddress("N", N, &b_n);
   fChain->SetBranchAddress("multV0A", &multV0A, &b_multV0A);
   fChain->SetBranchAddress("multV0C", &multV0C, &b_multV0C);
   fChain->SetBranchAddress("partZDC", &partZDC, &b_partZDC);
   fChain->SetBranchAddress("pileupspd", &pileupspd, &b_pileupspd);
   fChain->SetBranchAddress("pileupmv", &pileupmv, &b_pileupmv);
   Notify();
}

bool TreeLRC::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return true;
}

void TreeLRC::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t TreeLRC::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef TreeLRC_cxx

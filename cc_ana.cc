// -*- C++ -*-
#include "Rivet/Analysis.hh"
#include "Rivet/Projections/FinalState.hh"
#include "Rivet/Projections/FastJets.hh"

namespace Rivet {


  class cc_ana : public Analysis {
  public:

    /// Constructor
    cc_ana()
      : Analysis("cc_ana")
    {    }


    /// Book histograms and initialise projections before the run
    void init() {
      const FastJets jets(FinalState(-5., 5., 0.0), FastJets::ANTIKT, 0.4);
      addProjection(jets, "Jets");

      _h_1 = bookHisto1D("h_low_eta_low_pt", 18, 0, M_PI);
      _h_2 = bookHisto1D("h_high_eta_low_pt", 18, 0, M_PI);
      _h_3 = bookHisto1D("h_low_eta_medium_pt", 18, 0, M_PI);
      _h_4 = bookHisto1D("h_high_eta_medium_pt", 18, 0, M_PI);
      _h_5 = bookHisto1D("h_low_eta_high_pt", 18, 0, M_PI);
      _h_6 = bookHisto1D("h_high_eta_high_pt", 18, 0, M_PI);
    }


    /// Perform the per-event analysis
    void analyze(const Event& event) {
      const Jets& jets = applyProjection<FastJets>(event, "Jets").jetsByPt(30.0);
      //std::cout << "jets.size() " << jets.size()<<std::endl;
      // for (auto j : jets){
      // 	std::cout << " j.pt() " << j.pt()<<std::endl;
      // }
      if (jets.size() < 3) vetoEvent;

      const FourMomentum jet1 = jets[0].momentum();
      const FourMomentum jet2 = jets[1].momentum();
      const FourMomentum jet3 = jets[2].momentum();

      // Cut on lead jet pT and lead/sublead jet centrality
      if (jet1.pT() < 100) vetoEvent;
      if (jet1.abseta() > 2.5 || jet2.abseta() > 2.5) vetoEvent;

      double dPhi12 = jet2.phi() - jet1.phi();
      if (dPhi12 > M_PI)  dPhi12 -= 2*M_PI; ///< @todo Use mapTo... functions?
      if (dPhi12 < -M_PI) dPhi12 += 2*M_PI; ///< @todo Use mapTo... functions?
      if (abs(abs(dPhi12) - M_PI) > 1.0) vetoEvent;

      // Construct eta & phi distances between 2nd and 3rd jets
      double dEta23 = jet3.eta() - jet2.eta(); ///< Note not abs
      double dPhi23 = jet3.phi() - jet2.phi(); ///< Note not abs
      if (dPhi23 > M_PI)  dPhi23 -= 2*M_PI; ///< @todo Use mapTo... functions?
      if (dPhi23 < -M_PI) dPhi23 += 2*M_PI; ///< @todo Use mapTo... functions?

      // Cut on distance between 2nd and 3rd jets
      const double R23 = add_quad(dPhi23, dEta23);
      if (!inRange(R23, 0.5, 1.5)) vetoEvent;

      // Cut on dijet mass
      const FourMomentum diJet = jet1 + jet2;
      if (diJet.mass() < 220) vetoEvent;

      // Calc beta and fill histogram (choose central or fwd histo inline)
      double beta = fabs(atan2(dPhi23, sign(jet2.eta())*dEta23));
      //if (inRange(jet1.pT(), 74,220)){
      ((jet2.abseta() < 0.8) ? _h_1 : _h_2)->fill(beta, event.weight());
	 //}
      if (inRange(jet1.pT(), 220,507)){
         ((jet2.abseta() < 0.8) ? _h_3 : _h_4)->fill(beta, event.weight());
      }
      if (inRange(jet1.pT(), 507,2500)){
         ((jet2.abseta() < 0.8) ? _h_5 : _h_6)->fill(beta, event.weight());
      }

    }


    /// Normalise histograms etc., after the run
    void finalize() {
      //const double width = _h_hTotD->bin(0).xWidth();
      //const double width = 1.0;
       
      //normalize(_h_hTotD, width);
      //normalize(_h_hTotDF, width);
      //normalize(_h_1, width);
      //normalize(_h_2, width);
      //normalize(_h_3, width);
      //normalize(_h_5, width);
      //normalize(_h_6, width);

    }


  private:

    /// @name Histograms
    Histo1DPtr _h_1;
    Histo1DPtr _h_2;
    Histo1DPtr _h_3;
    Histo1DPtr _h_4;
    Histo1DPtr _h_5;
    Histo1DPtr _h_6;
    //@}

  };



  // The hook for the plugin system
  DECLARE_RIVET_PLUGIN(cc_ana);

}

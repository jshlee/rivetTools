# rivetTools

```bash
scram p -n rivet CMSSW CMSSW_7_2_0_pre3
cd rivet/src
cmsenv
git cms-addpkg GeneratorInterface/RivetInterface
git clone git@github.com:hyunyong/rivetTools.git
cp rivetTools/cc_ana.cc GeneratorInterface/RivetInterface/src
scram b -j 8
```


#!/usr/bin/env python

import ROOT, array, numpy
ROOT.gROOT.SetBatch()
class yodaReader:
  raw_l = []
  hist_l = []
  hist_raw = []
  def __init__(self, file):
    tmp_f = open(file, 'r')
    for x in tmp_f:
      self.raw_l.append(x)
      if x.startswith("# BEGIN"):
        self.hist_l.append(x.split("/")[-1].split("\n")[0]) 
    for key in self.hist_l:
      read_mod = 0
      tmp_raw = []
      for x in self.raw_l:
        tmp = x.split("\n")[0]
        if tmp.startswith("# BEGIN") and tmp.endswith(key):
          read_mod = 1
        if read_mod == 1:
          tmp_raw.append(tmp.split("\t"))
          if tmp.startswith("# END"):
            read_mod = 0
            self.hist_raw.append(tmp_raw)
            break
            
  def get(self, key):
    index = self.hist_l.index(key)
    hist = Histo1D(self.hist_raw[index])
    return hist
  def keys(self):
    return self.hist_l
 
class Histo1D:
  title = ""
  numOfBins = 0
  numOfEntrie = 0.0
  raw = []
  bin = []
  val = []
  def __init__(self, hist_raw):
    self.bin = []
    self.val = []
    self.raw = hist_raw
    read_mod = 0
    self.title = self.raw[0][0].split("/")[-1]
    for x in self.raw:
      if x[0].startswith("# xlow"):
        read_mod = 1
        continue
      if read_mod == 1:
        if x[0].startswith("# END"):
          break
        self.bin.append([float(x[0]), float(x[1])])
        self.val.append(float(x[2]))
    self.numOfBins = len(self.bin)
  def getBinContent(self, index):
    return self.val[index]

  def getBin(self, index):
    return self.bin[index]

  def makeTH1F(self):
    bin_l = []
    bin_l.append(self.bin[0][0])
    for x in self.bin:
      bin_l.append(x[1])
    #th1 = ROOT.TH1F(self.title, self.title, self.numOfBins, array.array('d',bin_l))
    th1 = ROOT.TH1F(self.title, self.title, 18, 0.0, ROOT.TMath.Pi())
    #th1.Sumw2()
    for x in xrange(self.numOfBins):
      th1.Fill(numpy.mean(self.bin[x]),self.val[x])
      #th1.SetBinContent(x+1,self.val[x])
    return th1
if __name__ =='__main__':
  
  import os, sys, ROOT
  ROOT.gROOT.SetBatch()
  in_file = sys.argv[1]
  tmp = yodaReader(in_file)
  key_l = tmp.keys()
  hist_l = []
  for x in key_l:
    tmp_h = tmp.get(x)
    hist_l.append(tmp_h.makeTH1F())
  out_f = ROOT.TFile(in_file.replace(".yoda", ".root"), "RECREATE")
  out_f.cd()
  for x in hist_l:
    x.Write()
  out_f.Close()
    

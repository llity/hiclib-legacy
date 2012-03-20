import base 
base #Eclipse warning damper 

import scipy.stats

import plotting 
 

import numpy 

import cPickle
  

import matplotlib.pyplot as plt 
def corr(x,y): return scipy.stats.spearmanr(x, y)[0]
    
        
#HG18 = Genome("HG18")


def doBedCoverage(filename):
    chromosomes =  [247199719, 242751149, 199446827, 191263063, 180837866, 170896993, 158821424, 146274826, 140442298, 135374737, 134452384, 132289534, 114127980, 106360585, 100338915, 88822254, 78654742, 76117153, 63806651, 62435965, 46944323, 49528953]
    arrays = [0] + [numpy.zeros(i/100+10,numpy.int32) for i in chromosomes]
    chromosomes = arrays
    a = open(filename).readlines()
    for t,j in enumerate(a):
        t #Warning removal 
        i = j.split("\t")[:3]
        try: ch = int(i[0][3:])
        except: continue
        if ch > 22: continue
        pos1 = int(i[1])
        pos2 = int(i[2])
        #plt.plot(numpy.hist)
        if pos2 - pos1 < 100000: chromosomes[ch][pos1/100:pos2/100] += 1
    #plt.plot(chromosomes[1][::100])
    #plt.show()
    cPickle.dump(chromosomes,open(filename + ".dat",'wb'),-1)
    
    
    
#doBedCoverage("/home/magus/HiC2011/expression/GSM646522_hg18_wgEncodeCshlLongRnaSeqAlignmentsRep1Gm12878CellTotal.bb.bed")
#doBedCoverage("/home/magus/HiC2011/expression/GSM646523_hg18_wgEncodeCshlLongRnaSeqAlignmentsRep1K562CellTotal.bb.bed")
#doBedCoverage("/home/magus/HiC2011/expression/GSM646522_hg18_wgEncodeCshlLongRnaSeqAlignmentsRep2Gm12878CellTotal.bb.bed")
#doBedCoverage("/home/magus/HiC2011/expression/GSM646523_hg18_wgEncodeCshlLongRnaSeqAlignmentsRep2K562CellTotal.bb.bed")


def coolAv(a,resolution=10000):
    a = numpy.array(a,float)
    a = numpy.log(a+1)
    N = len(a)
    result = numpy.zeros(N/resolution + 1)
    for i in xrange(N/resolution):
        cut = numpy.sort(a[i*resolution:(i+1)*resolution])
        #print cut[0.05*M:0.95*M]
        #result[i] = numpy.mean(cut[0.05*M:0.95*M])
        result[i] = numpy.mean(cut)
    return result

def analyzeBeds():
    GM = cPickle.load(open("/home/magus/HiC2011/expression/GSM646522_hg18_wgEncodeCshlLongRnaSeqAlignmentsRep1Gm12878CellTotal.bb.bed.dat",'rb'))
    GM += cPickle.load(open("/home/magus/HiC2011/expression/GSM646522_hg18_wgEncodeCshlLongRnaSeqAlignmentsRep2Gm12878CellTotal.bb.bed.dat",'rb'))
    K = cPickle.load(open("/home/magus/HiC2011/expression/GSM646523_hg18_wgEncodeCshlLongRnaSeqAlignmentsRep1K562CellTotal.bb.bed.dat",'rb'))
    K += cPickle.load(open("/home/magus/HiC2011/expression/GSM646523_hg18_wgEncodeCshlLongRnaSeqAlignmentsRep2K562CellTotal.bb.bed.dat",'rb'))
    
    #gf = scipy.ndimage.filters.gaussian_filter
    chroms = range(1,23)
    
    d1 = numpy.concatenate([coolAv(GM[chrom]) for chrom in chroms])
    d2 = numpy.concatenate([coolAv(K[chrom]) for chrom in chroms])
    d = d1 + d2
    sd = numpy.sort(d)
    mask = (d > sd[0.30  * len(sd)]) *(d < sd[0.70 * len(sd)])     
    #e1 = numpy.concatenate([dnaUtils.load_eigenvector(chrom,0) for chrom in chroms])
    #e2 = numpy.concatenate([dnaUtils.load_eigenvector(chrom,1) for chrom in chroms])
    e1 = None
    e2 = None
    #TODO: redo the "load eigenvector" part 
    
    print len(d1),len(e1)
    def corr(x,y): return scipy.stats.spearmanr(x, y)[0]


    plt.show()

    print corr(d1,e1),corr(d2,e2),corr(d1,e2),corr(d2,e1)
    
    #plt.plot(d1,'g-')
    #plt.plot(d2,'b-')
    #plt.plot(e1,'g--')
    #plt.plot(e2,'b--')
    #mymean = e1+e2


    arg = False
    def rank(x):
        x = numpy.array(x)
        tmp = x.argsort()
        return numpy.array(numpy.arange(len(x)),float)[tmp.argsort()]
    
    if arg == True:
        
        d1 = rank(d1)
        d2 = rank(d2)
        e1 = rank(e1)
        e2 = rank(e2)

    #plt.scatter(e1,e2)
    #plt.show()

    if arg == True:
        a1 = d1 - d2
    else: 
        a1 = (d1 + 0.00000001) / (d1 + d2 + 0.00000002)
    a2 = e1 - e2
    
    a1 = a1[mask]
    a2 = a2[mask]
    
    plt.scatter(a1,a2,s=10,c = (e1 + e2)[mask],cmap = "jet",linewidth = 0)
    
    #a1 = 
    
    
    a1s = numpy.argsort(a1)
    alen = len(a1)
    bins = 20
    xvalues = []
    yvalues = []
    y25 = []
    y75 = []     
    for i in xrange(bins):
        cur = a1s[(alen*i)/bins:(alen*(i+1))/bins]
        xvalues.append(numpy.mean(a1[cur]))
        yvalues.append(numpy.mean(a2[cur]))
        ysort = numpy.sort(a2[cur])
        y25.append(ysort[len(ysort)* 0.05])
        y75.append(ysort[len(ysort)* 0.95])
    plt.plot(xvalues,yvalues,'b',label = "Mean domain difference")

#coltrol
    a2 = a2[:-2]
    a1 = a1[2:]
    a1s = numpy.argsort(a1)
    alen = len(a1)
    bins = 20
    xvalues = []
    yvalues = []
    y25 = []
    y75 = []     
    for i in xrange(bins):
        cur = a1s[(alen*i)/bins:(alen*(i+1))/bins]
        xvalues.append(numpy.mean(a1[cur]))
        yvalues.append(numpy.mean(a2[cur]))
        ysort = numpy.sort(a2[cur])
        y25.append(ysort[len(ysort)* 0.05])
        y75.append(ysort[len(ysort)* 0.95])
    plt.plot(xvalues,yvalues,'b--',label = "Control - shift by 2 Mb")

    
    #plt.plot(xvalues,y25,'b--',linewidth=1)
    #plt.plot(xvalues,y75,'b--',linewidth=1)
        
    
    plt.xlabel("fraction of the GM expression in total expression")
    plt.ylabel("difference between domains in two datasets(GM - K562)")
    plt.title("color denotes mean domains from Erez paper")
    

    plt.colorbar()
    plotting.niceShow()
    
#analyzeBeds()
#exit()
#doBedCoverage("/home/magus/Downloads/test.bed")
 

This is a current version of the pipeline which we used up to May 2017 for processing many Hi-C datasets. This version is for .sra files or fastq.gz files split by two sides. 

This is a small modification of the pipeline2015_python3 designed to work with coolers. 
It was not extensively tested, and is a temporary workaround until we switch to distiller. 

..warning:: * this pipeline will be replaced with distiller in May 2017. 
..warning: If you are reading this after June 2017, you should not be using this pipeline. Just use distiller 

distiller: https://github.com/mirnylab/distiller

Usage: 

1. place .sra files in the fastq folder 
2. edit defineGenome.py. Specify genome paths for genomes you will be using. 
3. edit 01_mapData.py. Specify bowtie path, and all other arguments 
4. provide runs.tsv file as described in 02_makeDatasetsFile.py
5. run makeDatasetsFile.py
6. possibly edit 02_mergeDatasets.py to specify resolutions (especially when working with smaller genomes) 
7. run 02_mergeDatasets.py   -  it will do several things.
    -- merge (if necessary) different .hdf5 files corresponding to one replica of one datasets  
    -- do fragment-level filtering of merged files 
    -- save heatmaps at different resolutions
    -- merge files from different replicas of the same experiment
    -- save heatmaps 


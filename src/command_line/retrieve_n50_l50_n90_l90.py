# python3
import argparse
import os
from pyfaidx import Fasta
import numpy
# input parameters
ap = argparse.ArgumentParser()
ap.add_argument("-dir", "--directory", required=False, default='.', type=str, help="output directory to read the multi-fasta files with scaffolds/chromosomes. Default is the current directory")
ap.add_argument("-txt", "--txt", required=True, help="output txt file with 5 columns filename, N50, L50, N90 and L90 values")
args = vars(ap.parse_args())
# main
# create output file headers
with open(args['txt'], 'a') as filehandle:
            filehandle.write('%s\n' % '\t'.join(["filename","N50","L50","N90","L90"]))
scaffolds = [] # setup empty list
# import each fasta file from the working directory
with open(args['txt'], 'a') as filehandle:
    for filename in sorted(os.listdir(os.chdir(args['directory']))):
        if filename.endswith(".fa") or filename.endswith(".fasta"):
            features = Fasta(filename)
            # retrieve scaffold/chr lengths
            for key in features.keys():
                scaffolds.append(features[key][:].end)
            # sort by size
            scaffolds.sort(reverse=True)
            # calculate the cumulative sum
            csum=numpy.cumsum(scaffolds)
            n2=int(sum(scaffolds)/2)
            # get index for cumsum >= N/2
            csumn50=min(csum[csum >= n2])
            ind50=numpy.where(csum == csumn50)
            n50 = scaffolds[int(ind50[0])]
            l50 = int(ind50[0] +1)
            # get index for cumsum >= N*0.9
            nx90=int(sum(scaffolds) * 0.9)
            csumn90=min(csum[csum >= nx90])
            ind90=numpy.where(csum == csumn90)
            n90 = scaffolds[int(ind90[0])]
            l90 = int(ind90[0] +1)
            # export to txt
            filehandle.write('%s\n' % '\t'.join([filename.split('.fa')[0],str(n50),str(l50),str(n90),str(l90)]))
            # delete objects to be reused by the next file
            del features; scaffolds.clear(); del csum; del ind50; del ind90 
#! /usr/bin/env python
import sima
import sima.motion
import sima.segment
import os
from os.path import *
import getpass

# get feedback about which python packages we are using, aka did the shebangs line work
#import pip
#sorted(["%s==%s" % (i.key, i.version) for i in pip.get_installed_distributions()])
#root_dir='/Users/' + getpass.getuser() + ''
os.chdir('.')

data_dir="./real_data/"
ds_name='example_data.sima'

# Create filenames
tiff_filenames = [ [data_dir + '20150303_AF{n1:02d}_{n2:03d}.tif'.format(n1=animal_nr, n2=session_nr) for animal_nr in range(3,4)] for session_nr in range(2, 3)]

# The resulting filenames are printed for clarification.
print "TIFF filenames:\n", tiff_filenames

# Finally, we construct a MultiPageTIFF iterable using each of the filenames.
sequences = [
    sima.Sequence.join(*[sima.Sequence.create('TIFF', chan) for chan in cycle])
    for cycle in tiff_filenames]


dataset = sima.ImagingDataset(sequences, ds_name)

# load using : 
#dataset = sima.ImagingDataset.load(ds_name)

# Set motion correction parameters
mc_approach = sima.motion.PlaneTranslation2D(max_displacement=[15, 30])

# Apply motion correction
# Needs dataset or sequences and save dir/dataset name
dataset = mc_approach.correct(dataset, ds_name)

# Output corrected frames
output_filenames = [
    [[channel.replace('.tif', '_corrected.tif') for channel in cycle]]
    for cycle in tiff_filenames
]
    
print "TIFF filenames:\n", output_filenames


#output_filenames='20150415_AF11_RM_004_corrected.tif'
dataset.export_frames(output_filenames, fill_gaps=True)




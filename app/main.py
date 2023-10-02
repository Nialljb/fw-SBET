import os, sys
from pathlib import Path
import pandas as pd  

# Pre-run gears:
# 1. Isotropic reconstruction (CISO)
# 2. Bias correction (N4)

# HARDCODING...
# Requires some recoding to make it more flexible

#  -------------------  The main event -------------------  #

# Set up the paths

def bet():
    FLYWHEEL_BASE = "/flywheel/v0"
    INPUT_DIR = (FLYWHEEL_BASE + "/input/input/")
    biasCorrImage = (INPUT_DIR + "/isotropicReconstruction_corrected.nii.gz")
    # WORK = (FLYWHEEL_BASE + "/work")
    OUTPUT_DIR = (FLYWHEEL_BASE + "/output")

    studyHeadReference = FLYWHEEL_BASE + "app/template/UCT-T2.nii.gz"
    studyBrainReference = FLYWHEEL_BASE + "app/template/UCT-T2-brain.nii.gz"
    studyBrainMask = FLYWHEEL_BASE + "app/template/UCT-T2_bet_mask.nii.gz"
    print("head is: ", studyHeadReference)
    print("ref is: ", studyBrainReference)

    # ---  Set up the software ---  #
    # antsWarp =  "ANTS 3 -G -m CC["
    antsImageAlign = "WarpImageMultiTransform 3 "
    antsMIWarp = "ANTS 3 -G -m MI["

    # now perform the nonlinear registration using the whole head as an initial step
    wholeHeadRegisteredImage = OUTPUT_DIR + "/_to_wholeHeadReference.nii.gz"

    os.system(antsMIWarp + studyHeadReference + ", " + biasCorrImage + ", 1, 96] -o " + wholeHeadRegisteredImage + " -i 100x80x40 -r Gauss[3,1] -t SyN[0.25] --use-Histogram-Matching --MI-option 32x16000 --number-of-affine-iterations 10000x10000x10000x10000x10000")

    headWarpField = OUTPUT_DIR + "/_to_wholeHeadReferenceWarp.nii.gz"
    headAffineField = OUTPUT_DIR + "/_to_wholeHeadReferenceAffine.txt"
    headInverseField = OUTPUT_DIR + "/_to_wholeHeadReferenceInverseWarp.nii.gz"

    alignedWholeHeadImage = OUTPUT_DIR + "/_to_wholeHeadReferenceAligned.nii.gz"
    os.system(antsImageAlign + " " + biasCorrImage + " " + alignedWholeHeadImage + " -R " + studyHeadReference + " " + headWarpField + " " + headAffineField + " --use-BSpline")

    # now reverse align the brain mask to the individual
    individualBrainMask = OUTPUT_DIR + "/_brainMask.nii.gz"
    os.system(antsImageAlign + " " + studyBrainMask + " " + individualBrainMask + " -R " + biasCorrImage + " -i " + headAffineField + " " + headInverseField + " --use-BSpline")

    # multiply the brain mask against the whole head image and then bet the image to refine the brain mask
    individualBrainMaskedImage = OUTPUT_DIR + "/_maskedBrain.nii.gz"
    refinedIndividualBrainMaskedImage = OUTPUT_DIR + "/_refinedMaskedBrain.nii.gz"
    os.system("fslmaths " + biasCorrImage + " -mul " + individualBrainMask + " " + individualBrainMaskedImage)
    os.system("bet2 " + individualBrainMaskedImage + " " + refinedIndividualBrainMaskedImage + " -f .1 ")
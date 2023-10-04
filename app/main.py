import os
import subprocess
import pathlib

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
    WORK = (FLYWHEEL_BASE + "/work")
    OUTPUT_DIR = (FLYWHEEL_BASE + "/output")

    studyHeadReference = FLYWHEEL_BASE + "/app/template/UCT-T2.nii.gz"
    studyBrainReference = FLYWHEEL_BASE + "/app/template/UCT-T2-brain.nii.gz"
    studyBrainMask = FLYWHEEL_BASE + "/app/template/UCT-T2_bet_mask.nii.gz"
    print("head is: ", studyHeadReference)
    print("ref is: ", studyBrainReference)
    print("work is: ", WORK)
    # ---  Set up the software ---  #
    # antsWarp =  "ANTS 3 -G -m CC["
    antsImageAlign = "WarpImageMultiTransform 3 "
    antsMIWarp = "ANTS 3 -G -m MI["

    # now perform the nonlinear registration using the whole head as an initial step
    wholeHeadRegisteredImage = OUTPUT_DIR + "/wholeHeadReference.nii.gz"

    subprocess.run([antsMIWarp + studyHeadReference + ", " + biasCorrImage + ", 1, 96] -o " + wholeHeadRegisteredImage + " -i 100x80x40 -r Gauss[3,1] -t SyN[0.25] --use-Histogram-Matching --MI-option 32x16000 --number-of-affine-iterations 10000x10000x10000x10000x10000"], shell=True, check=True)

    headWarpField = OUTPUT_DIR + "/wholeHeadReferenceWarp.nii.gz"
    headAffineField = OUTPUT_DIR + "/wholeHeadReferenceAffine.txt"
    headInverseField = OUTPUT_DIR + "/wholeHeadReferenceInverseWarp.nii.gz"

    alignedWholeHeadImage = OUTPUT_DIR + "/wholeHeadReferenceAligned.nii.gz"
    subprocess.run([antsImageAlign + " " + biasCorrImage + " " + alignedWholeHeadImage + " -R " + studyHeadReference + " " + headWarpField + " " + headAffineField + " --use-BSpline"], shell=True, check=True)

    # # now reverse align the brain mask to the individual
    individualBrainMask = OUTPUT_DIR + "/isotropicReconstruction_corrected_sbet_mask.nii.gz"
    subprocess.run([antsImageAlign + " " + studyBrainMask + " " + individualBrainMask + " -R " + biasCorrImage + " -i " + headAffineField + " " + headInverseField + " --use-BSpline"], shell=True, check=True)

    # multiply the brain mask against the whole head image and then bet the image to refine the brain mask
    individualBrainMaskedImage = OUTPUT_DIR + "/initialBrainMaskedImage.nii.gz"
    refinedIndividualBrainMaskedImage = OUTPUT_DIR + "/isotropicReconstruction_corrected_sbet_brain.nii.gz"
    
    subprocess.run(["fslmaths " + biasCorrImage + " -mul " + individualBrainMask + " " + individualBrainMaskedImage], shell=True)
    subprocess.run(["bet2 " + individualBrainMaskedImage + " " + refinedIndividualBrainMaskedImage + " -f .1 "], shell=True)

    # Check if file exists
    file = pathlib.Path("/flywheel/v0/output/isotropicReconstruction_corrected_sbet_brain.nii.gz")
    if file.is_file():
        print ("Simple BET complete: finishing up...")
    else:
        print ("File does not exist")
        exit(1)
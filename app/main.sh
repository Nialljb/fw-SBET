#! /bin/bash
#
# Run script for flywheel/sbet Gear.
#
# Authorship: Niall bourke
#
##############################################################################
# Define directory names and containers

FLYWHEEL_BASE=/flywheel/v0
INPUT_DIR=$FLYWHEEL_BASE/input/
OUTPUT_DIR=$FLYWHEEL_BASE/output
CONFIG_FILE=$FLYWHEEL_BASE/config.json
CONTAINER='[flywheel/sbet]'

##############################################################################
# Parse configuration
function parse_config {

  CONFIG_FILE=$FLYWHEEL_BASE/config.json
  MANIFEST_FILE=$FLYWHEEL_BASE/manifest.json

  if [[ -f $CONFIG_FILE ]]; then
    echo "$(cat $CONFIG_FILE | jq -r '.config.'$1)"
  else
    CONFIG_FILE=$MANIFEST_FILE
    echo "$(cat $MANIFEST_FILE | jq -r '.config.'$1'.default')"
  fi
}

# define output choise:
config_output_nifti="$(parse_config 'output_nifti')"

##############################################################################
# Handle INPUT file

# Find input file In input directory with the extension
# .nii, .nii.gz
input_file=`find $INPUT_DIR -iname '*.nii' -o -iname '*.nii.gz'`

# Check that input file exists
if [[ -e $input_file ]]; then
  echo "${CONTAINER}  Input file found: ${input_file}"

    # Determine the type of the input file
  if [[ "$input_file" == *.nii ]]; then
    type=".nii"
  elif [[ "$input_file" == *.nii.gz ]]; then
    type=".nii.gz"
  fi
  # Get the base filename
  base_filename=`basename "$input_file" $type`
  
else
  echo "${CONTAINER} inputs were found within input directory $INPUT_DIR"
  exit 1
fi

##############################################################################
# Run hdbet algorithm

# Set initial exit status
mri_sbet_exit_status=0

# Set base output_file name
output_file=$OUTPUT_DIR/"$base_filename"'_sbet'
echo "output_file is $output_file"

# Run hdbet with options
if [[ -e $input_file ]]; then
  echo "Running SBET..."
  hd-bet -i $input_file -o $output_file -device cpu -mode fast -tta 0
  mri_sbet_exit_status=$?
fi

##############################################################################
# Handle Exit status

if [[ $mri_sbet_exit_status == 0 ]]; then
  echo -e "${CONTAINER} Success!"
  exit 0
else
  echo "${CONTAINER}  Something went wrong! mri_hdbet exited non-zero!"
  exit 1
fi

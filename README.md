# Simple Brain Extraction (SBET)

## Overview

[Usage](#usage)

[FAQ](#faq)

### Summary


### Cite

**license:**


**url:** <https://gitlab.com/flywheel-io/flywheel-apps/>

**cite:**  


### Classification

*Category:* analysis

*Gear Level:*

* [ ] Project
* [x] Subject
* [x] Session
* [ ] Acquisition
* [ ] Analysis

----

### Inputs

* api-key
  * **Name**: api-key
  * **Type**: object
  * **Optional**: true
  * **Classification**: api-key
  * **Description**: Flywheel API key.

### Config

* input
  * **Base**: file
  * **Description**: input file (usually isotropic reconstruction)
  * **Optional**: false

### Outputs
* output
  * **Base**: file
  * **Description**: segmentated file 
  * **Optional**: false

#### Metadata

No metadata currently created by this gear

### Pre-requisites

- Bias correction

#### Prerequisite Gear Runs

1. ***dcm2niix***
    * Level: Any
2. ***file-metadata-importer***
    * Level: Any
3. ***file-classifier***
    * Level: Any

#### Prerequisite

## Usage

This section provides a more detailed description of the gear, including not just WHAT
it does, but HOW it works in flywheel

### Description


#### File Specifications

This section contains specifications on any input files that the gear may need

### Workflow

A picture and description of the workflow

```mermaid
  graph LR;
    A[T1w]:::input --> FW;
    FW[FW] --> FC;
    FC((file-classifier)):::gear --> D2N;
    D2N((dcm2niix)):::gear --> CISO;
    CISO((ciso)):::gear --> N4;
    N4((Bias correction)):::gear --> ANA;
    SBET ((BET)):::gear --> VBM;
    VBM[Analysis]:::container;
    
    classDef container fill:#57d,color:#fff
    classDef input fill:#7a9,color:#fff
    classDef gear fill:#659,color:#fff
```

Description of workflow

1. Upload data to container
2. Prepare data by running the following gears:
   1. file metadata importer
   2. file classifier
   3. dcm2niix
   4. MRIQC (optional)
   5. curate bids
3. Select either a subject or a session.
4. Run the ciso gear (Hyperfine triplane aquisitions)
5. Run the synthseg gear
6. Gear places output in Analysis

### Use Cases

## FAQ

[FAQ.md](FAQ.md)

## Contributing

[For more information about how to get started contributing to that gear,
checkout [CONTRIBUTING.md](CONTRIBUTING.md).]

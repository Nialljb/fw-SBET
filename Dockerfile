FROM nialljb/njb-ants-fsl-base:0.0.1 as base

ENV HOME=/root/
ENV FLYWHEEL="/flywheel/v0"
WORKDIR $FLYWHEEL
RUN mkdir -p $FLYWHEEL/input

# Installing the current project (most likely to change, above layer can be cached)
COPY ./ $FLYWHEEL/

# Dev dpendencies
RUN apt-get update && apt-get install --no-install-recommends -y software-properties-common=0.96.20.2-2 && \
    apt-get clean && \
    pip install flywheel-gear-toolkit && \
    pip install flywheel-sdk && \
    pip install importlib_metadata && \
    apt-get update && apt-get install jq -y && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
    
# store the FSL public conda channel
ENV FSL_CONDA_CHANNEL="https://fsl.fmrib.ox.ac.uk/fsldownloads/fslconda/public"
RUN /opt/conda/bin/conda install -n base -c $FSL_CONDA_CHANNEL fsl-bet2 -c conda-forge
# set FSLDIR so FSL tools can use it, in this minimal case, the FSLDIR will be the root conda directory
ENV PATH="/opt/conda/bin:${PATH}"
ENV FSLDIR="/opt/conda"

# Configure entrypoint
RUN bash -c 'chmod +rx $FLYWHEEL/run.py' && \
    bash -c 'chmod +rx $FLYWHEEL/app/main.sh' \
    bash -c 'chmod +rx $FLYWHEEL/start.sh' \
ENTRYPOINT ["bash"] 
# Flywheel reads the config command over this entrypoint
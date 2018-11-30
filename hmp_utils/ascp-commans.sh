#!/bin/bash
export ASCP=/Users/Dporter1/Applications/AsperaCLI/bin/ascp
export ASPERA_USER=dcpchi
export ASPERA_SCP_PASS=deepfeature

/Users/Dporter1/Applications/AsperaCLI/bin/ascp -d  dcpchi@aspera.ihmpdcc.org:ibd/metatranscriptome/microbiome/analysis/CSM5FZ4C_P_genefamilies.biom ./ibd/metatranscriptome/microbiome/analysis/CSM5FZ4C_P_genefamilies.biom

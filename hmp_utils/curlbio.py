
bashCommand = "curl -k --user dcpchi:deepfeature --ftp-ssl ftp://downloads.hmpdacc.org/data/HMR16S/HMDEMO/SRP002422/SRR052230.sff.bz2 > ./results.txt"
import subprocess
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

bashCommand = "./manifest2ascp.py --manifest=manifesttsv.tsv --user=dcp_chi --password=deepfeature --ascp_path=/Users/Dporter1/Applications/AsperaCLI/bin/ascp > ascp-commands.sh"
import subprocess
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

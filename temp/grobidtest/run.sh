#!/bin/ash
# mv /src/lib/grobid_client_python/grobid_client /src/grobid_client
echo "Start running grobid client script"
python grobid.py
ls /src/resources
ls /src/resources/test_out
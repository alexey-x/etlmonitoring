#!/bin/bash

action=$1

APPHOME=/mo/monitor_etl
CURDIR=`pwd`


usage(){
    echo $1
    echo "usage: $0 encrypt|decrypt"
    exit 1
}

case $1 in    
    encrypt) encrypt=1;;
    decrypt) decrypt=1;;
    *) usage "command is not set"; exit 1;;
esac; shift;


cd $APPHOME
source .venv/bin/activate
python app/src/encryption.py --action $action
deactivate
cd $CURDIR

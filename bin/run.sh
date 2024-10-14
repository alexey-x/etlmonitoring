#!/bin/bash

APPNAME=etlmonitoring.py
APPHOME=/mo/monitor_etl

PID_DIR=$APPHOME/pid
PID_FILE=$PID_DIR/pid
LOGGING_FILE=$APPHOME/log/etlmonitoring.log
CURDIR=`pwd`

mkdir -p $PID_DIR

usage(){
    echo $1
    echo "usage: $0 start|stop"
    exit 1
}

case $1 in    
    start) start=1;;
    stop) stop=1;;
    *) usage "command is not set"; 
    exit 1;;
esac; 
shift;

get_pid() {
    if [ -f $PID_FILE ]
    then 
        PROCESS_PID=$(head -n 1 $PID_FILE)
    else
        return
    fi
    echo $PROCESS_PID
    return $PROCESS_PID
}

check_and_clean () {
    PROCESS=$(ps -x | grep $APPNAME | grep -v grep)
    if [ -n "$PROCESS" ]; then
        echo "Found running application"
        echo "$PROCESS"
        echo "You should stop it mannualy!"
        exit
    else
        echo "Running application is not found. Remove file $PID_FILE"
        rm $PID_FILE
    fi
}

start() {
    profile_pid=$(get_pid)
    if [ -n "$profile_pid" ]; then
        echo "There is PID-file telling that application must be running (pid = $profile_pid)"
        check_and_clean
    fi
    
    cd $APPHOME
    echo "ETL-monitoring starting"
    source .venv/bin/activate
    nohup python3 app/etlmonitoring.py > /dev/null 2>&1 &
    echo $! > $PID_FILE
    cd $CURDIR
}

stop() {
    profile_pid=$(get_pid)
    if [ -z "$profile_pid" ]; then
        echo "ETL-monitoring is not running"
        return
    fi
	kill `cat $PID_FILE`
    rm $PID_FILE

    cd $APPHOME
    echo "ETL-monitoring successfully finished"
    echo "`date "+%Y-%m-%d %H:%M:%S"` run.sh: ETL-monitoring finished" >> $LOGGING_FILE
    cd $CURDIR
}

if [ -n "$start" ]; then
    start
elif [ -n "$stop" ]; then
    stop
fi
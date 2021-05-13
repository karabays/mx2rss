#!/bin/bash
PID=$(ps aux | grep 'uvicorn app.main:app' | grep -v grep | awk {'print $2'} | xargs)
if [ "$PID" != "" ]
then
kill -9 $PID
sleep 2
echo "" > nohup.out
echo "Restarting FastAPI server"
echo "You can hit ctrl + c now."
else
echo "No such process. Starting new FastAPI server"
echo "You can hit ctrl + c now."
fi
nohup uvicorn app.main:app --host '0.0.0.0' --port 9123 &
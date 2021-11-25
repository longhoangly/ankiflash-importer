#!/bin/zsh

pid=$(ps -ef | grep AnkiMac | grep Anki.app | awk '{print $2;}')
if [ "$pid" != "" ]; then
    kill -9 $pid
fi
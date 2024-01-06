#!/bin/zsh

SRC="."
DEST="/Users/long.ly/Library/Application Support/Anki2/addons21/1129289384"

echo Starting Deployment...

echo Copying python files...
rm -f "$DEST/"*.py
cp *.py "$DEST"

deploy_folder() {

    echo Copying $1...

    rm -rf $DEST/$1
    mkdir -p $DEST/$1

    if [ "$2" != "" ]; then
        cp -R $SRC/$1/*.py $DEST/$1
    else
        cp -R $SRC/$1/* $DEST/$1
    fi
}

deploy_folder "resources"
deploy_folder "service"
deploy_folder "ui/importer" "py"
deploy_folder "ui/generator" "py"
deploy_folder "ui/mapper" "py"

echo Finished Deployment...

echo Open Anki to run test...

echo
for pid in $(ps -ef | grep Anki.app | awk '{print $2;}' | sed '$d')
do
    echo Killing process $pid
	kill -9 $pid
done

sleep .3
open /Applications/Anki.app

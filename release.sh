#!/bin/zsh

SRC="."
RELEASE="./release"

echo Starting Release...
rm -f __init__.zip

rm -rf $RELEASE
mkdir -p $RELEASE

echo Copying python files...
cp *.py $RELEASE

copy_folder() {

    echo Copying $1...
    mkdir -p $RELEASE/$1

    if [ "$2" != "" ]; then
        cp -R $SRC/$1/*.py $RELEASE/$1
    else
        cp -R $SRC/$1/* $RELEASE/$1
    fi
}

copy_folder "resources"
copy_folder "service"
copy_folder "ui" "py"

echo Compressing release files...
cd $RELEASE
zip -r __init__.zip *

echo Finished Release...
cp __init__.zip ..
cd ..
rm -rf $RELEASE
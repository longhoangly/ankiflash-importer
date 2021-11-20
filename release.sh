#!/bin/zsh

DEST="Library/Application Support/Anki2/addons21/1129289384"

mkdir -p ~/$DEST/Helpers
cp -R ./Helpers/* ~/$DEST/Helpers

mkdir -p ~/$DEST/Resources
cp -R ./Resources/* ~/$DEST/Resources

mkdir -p ~/$DEST/Service
cp -R ./Service/* ~/$DEST/Service

mkdir -p ~/$DEST/Ui
cp -R ./Ui/*.py ~/$DEST/Ui

cp *.py ~/$DEST

echo Finished Deployment...

RELEASE="Release"

rm -rf ./$RELEASE
mkdir ./$RELEASE

mkdir -p ./$RELEASE/Helpers
cp -R ./Helpers/* ./$RELEASE/Helpers

mkdir -p ./$RELEASE/Resources
cp -R ./Resources/* ./$RELEASE/Resources

mkdir -p ./$RELEASE/Service
cp -R ./Service/* ./$RELEASE/Service

mkdir -p ./$RELEASE/Ui
cp -R ./Ui/*.py ./$RELEASE/Ui

cp *.py ./$RELEASE

zip -r __init__.zip ./$RELEASE/*

echo Finished Releasing...

rm -r ./$RELEASE

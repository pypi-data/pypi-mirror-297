#!/bin/bash
# install libimagequant

archive=libimagequant-2.17.0

./download-and-extract.sh $archive https://raw.githubusercontent.com/python-pillow/pillow-depends/main/$archive.tar.gz

pushd $archive

make shared
sudo cp libimagequant.so* /usr/lib/
sudo cp libimagequant.h /usr/include/

popd

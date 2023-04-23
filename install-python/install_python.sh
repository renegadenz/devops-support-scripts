#!/bin/bash

# Check if make and gcc are installed
if ! command -v make &> /dev/null || ! command -v gcc &> /dev/null
then
    echo "make and gcc are required. Please install build-essential package and try again."
    exit 1
fi

# Install Python 3.10.4 in /usr/local/bin
wget https://www.python.org/ftp/python/3.10.4/Python-3.10.4.tgz
tar -xf Python-3.10.4.tgz
cd Python-3.10.4/
./configure --prefix=/usr/local/bin --enable-optimizations
make -j $(nproc)
sudo make altinstall

# Remove installation files
cd ..
rm -rf Python-3.10.4*

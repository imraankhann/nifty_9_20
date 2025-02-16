# Steps to install python 3.11 version virtual env

sudo python3.11 -m venv env


# Steps to install ta-lib 

wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz &&  
tar -xvzf ta-lib-0.4.0-src.tar.gz && 
cd ta-lib && 
./configure --prefix=/usr/local 
&& make && 
sudo make install

pip install ta-lib
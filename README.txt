Required libraries
python3 (sudo apt install python3)
pip (sudo apt install python3-pip)
virtual environment (sudo apt install python3.12-venv)
yfinance (pip install yfinance -> with activated virtual environment)
pymongo (pip install pymongo -> with activated virtual environment)


To create a virtual environment:
python3 -m venv myenv 

To activate virtual environment:
source myenv/bin/activate (Linux/WSL)

To turn off virtual environment:
deactivate


To start mongodb service:
sudo service mongod start

To check status of mongodb to see if its running:
sudo service mongod status

To run program simply type:
./setup_and_run.sh
Note: if says permission denied -> chmod +x setup_and_run.sh -> try again




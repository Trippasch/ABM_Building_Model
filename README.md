This is an agent based model project using Mesa(a Python framework for agent-based modeling).

This project is about finding multiple floor plans of a building using agent based modeling.
The agents are the rooms of the building. Each agent has a set of rules.
According to these rules the model runs till a floor view with the best fitting rules of each agent emerges.

Follow the instructions below in order to install mesa and then run the model.

1) Requirements:
Python3+, pip3

2) Installation:
$ pip3 install mesa

3) Dependencies:
$ pip3 install -r ~/path/to/ABM_Project/requirements.txt

    To install the dependencies needed to run this model simply execute the above command.
    
    *** /path/to/: your path to where ABM_Project is located in your computer.

4) Running the model:
$ mesa runserver

    To run the model execute the above command in the folder path where run.py is located.
    
    *** If you are on Windows make sure to comment out lines 4 and 5 in run.py !!!

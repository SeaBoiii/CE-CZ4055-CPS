# CE4055_CPS
 Implementation of Correlation Power Analysis

｡☆✼★━━━━━━━━━━━━━━━━━★✼☆｡

╭━━━┳━━━┳━━━┳━━━┳━╮╭━┳━━━╮

┃╭━╮┃╭━━┫╭━╮┣╮╭╮┃┃╰╯┃┃╭━━╯

┃╰━╯┃╰━━┫┃╱┃┃┃┃┃┃╭╮╭╮┃╰━━╮

┃╭╮╭┫╭━━┫╰━╯┃┃┃┃┃┃┃┃┃┃╭━━╯

┃┃┃╰┫╰━━┫╭━╮┣╯╰╯┃┃┃┃┃┃╰━━╮

╰╯╰━┻━━━┻╯╱╰┻━━━┻╯╰╯╰┻━━━╯

｡☆✼★━━━━━━━━━━━━━━━━━★✼☆｡

Made by: Team Snakes (Aleem, Ethel, Fatin, Samuel)

## Python Library Requirements
* cycler==0.11.0
* fonttools==4.32.0
* kiwisolver==1.4.2
* matplotlib==3.5.1
* numpy==1.21.6
* packaging==21.3
* pandas==1.3.5
* Pillow==9.1.0
* pyparsing==3.0.8
* PyQt5==5.15.6
* PyQt5-Qt5==5.15.2
* PyQt5-sip==12.10.1
* python-dateutil==2.8.2
* pytz==2022.1
* scipy==1.7.3
* six==1.16.0
* typing_extensions==4.1.1

## Instructions
There are a total of 3 different python files. 
* CPS_Project.ipynb
* PAT.py
* PATGUI.py

CPS_Project.ipynb :- Contains all the testing and plots that were done for the project. 
		 	   Some of the plots cannot be done by the other files due to the constrains of multiprocessing.
			   Especially for plot 2. Running the file is through Jupyter notebook. 

PAT.py		:- A console GUI based application where the user can decode the secret key using the console itself.
			   To run, simply run the Python file in a command environment, e.g. through cmd, then "**python PAT.py**"
																	
PATGUI.py		:- Requires PAT.py as a dependency. This was an external based GUI/application for user to interact
			   and also get the same results as you would get in PAT.py. Running this file will be the same as
			   running the PAT.py through the console. "**python PATGUI.py**"

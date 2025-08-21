# Architectural Views generation
This project revolves around the question of generation of software architectural views. We try to mine architectural knowledge of the system from source code and use this to generate views.
## Overview
This repository contains all the experiments and the results related to them which are conducted as a part of the pilot study for view generation. It contains folders named based on the approaches used with the prompt templates as described in the paper and each of them contain corresponding source code, outputs, analysis and evaluations.

### Instructions
Add your key in .txt file in required places and also add the paths of the files whenever required.
- For the first step, clone your repository.
- We used virtual environment to mitigate all the package dpendency issues. So, before runnig code please activate virtual environment.

```
pip install venv
```

- write the activation of the virtual environment in the main directory of the project.
```
cd CodeToDiagram
write the activation command based on the operating system
eg. for linux 
source venv/bin/activate
```
- As the next step, to install all the packages required execute the below command

```
pip install -r requirements.txt
```
- After completion of above step, navigate to the corresponding folder of the code
and run the below command
```
python <<name_of_file.py>>
```
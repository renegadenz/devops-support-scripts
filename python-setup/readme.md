# Installing Python

```
./install_python.sh
```

This is will install python 3.10.4 on local machine


# Creating a Python Virtual Environment
A virtual environment is a tool that helps to keep dependencies required by different projects separate by creating isolated python virtual environments for them. This is useful in case one project depends on a specific version of a library, while another project requires a different version.

To create a Python virtual environment, you can use the venv module that is included in the Python standard library.


## Steps
1. Open a terminal or command prompt.

2. Navigate to the directory where you want to create your virtual environment.

3. Run the following command to create a new virtual environment:

```
python3 -m venv env_name
```
Where env_name is the name of your virtual environment.

To activate the virtual environment, run the activate script:
```
source env_name/bin/activate
For windows :

```
env_name\Scripts\activate
```
You should now see the name of your virtual environment in the command prompt, indicating that it is active.

To deactivate the virtual environment, simply run the command:

```
deactivate
```
You can also use virtualenv or pipenv library to create virtual environment.

Note
It's highly recommended to use virtual environment while working on a project and installing packages. This will help you to keep your global environment clean and avoid conflicts and compatibility issues between different projects.
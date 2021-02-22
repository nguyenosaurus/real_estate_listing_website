# real_estate_listing_website
## Python Virtualenv
I use the virtualenv tool to install Python versions on my Windows. I find it a very useful tool, and the instructions that follow use it, and are based on having Python version 3.8.6 installed using the following command:

```
pip install virtualenv
```
## Installing The Project
From the main folder take the following steps:

* Install a Python virtual environment for this project
  * `python -m venv venv`
* Activate the virtual environment
  * `cd venv/Scripts`
  * `activate`
* Install the project:
  * `cd ../..`
  * `pip install -r requirements.txt`
  * `python -m pip install -e .`

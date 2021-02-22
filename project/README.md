# Execute the program
* Create a Postgres database
* Edit settings.py according to your database
* cd into the build_data directory
* `python build_region.py` - create table region and import data from region.csv
* `python build_database.py` - normalize data from real_estate_integrated.csv
* cd back to project directory
* `python -m flask run`

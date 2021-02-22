"""
This program builds the region Postgresql table from the
region.csv file.
"""

import os
import csv
from importlib import resources
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project.modules.models import Base, Address, Author, Project, Property_type, Transaction_type, Post, Region


def get_real_estate_data(filepath):
    """
    This function gets the data from the csv file
    """
    with open(filepath, encoding='UTF-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = [row for row in csv_reader]
        return data


def populate_database(session, real_estate_data):
    # insert the data
    for row in real_estate_data:

        region = Region(
            city = row["city"], district = row["district"], ward = row["ward"]
        )
        session.add(region)

        session.commit()

    session.close()


def main():
    print("starting")

    # get the region data into a dictionary structure
    with resources.path(
        "project.data", "region.csv"
    ) as csv_filepath:
        data = get_real_estate_data(csv_filepath)
        real_estate_data = data

    engine = create_engine('postgresql://postgres:fuckyou2810@localhost:5432/real_estate_dev')
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    populate_database(session, real_estate_data)

    print("finished")


if __name__ == "__main__":
    main()

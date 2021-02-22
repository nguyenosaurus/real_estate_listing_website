"""
This program builds the region Postgresql table from the
region.csv file.
"""

import os
import csv
from importlib import resources
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from project import settings
from project.modules.models import Base, Address, Author, Project, Property_type, Transaction_type, Post, Region


def get_region_data(filepath):
    """
    This function gets the data from the csv file
    """
    with open(filepath, encoding='UTF-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = [row for row in csv_reader]
        return data


def populate_database(session, region_data):
    # insert the data
    for row in region_data:
        
        region = (
            session.query(Region)
            .filter(
                Region.city == row["city"], Region.district == row["district"], Region.ward == row["ward"]
            )
            .one_or_none()
        )
        if region is None:
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
        data = get_region_data(csv_filepath)
        region_data = data

    engine = create_engine(URL(**settings.DATABASE))
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    populate_database(session, region_data)

    print("finished")


if __name__ == "__main__":
    main()

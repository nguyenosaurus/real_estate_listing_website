"""
This program builds the real_estate_dev Postgresql database from the
real_estate_integrated.csv file.
"""
import re
import os
import csv
from importlib import resources
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from project import settings
from project.modules.models import Base, Address, Author, Project, Property_type, Transaction_type, Post


def get_real_estate_data(filepath):
    """
    This function gets the data from the csv file
    """
    with open(filepath, encoding='UTF-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = [row for row in csv_reader]
        return data

def normalize_address(address, prefix):
    res = re.sub('(Huyện |Thành Phố |Thị Xã |Quận |Phường |Thị Trấn |Xã |Tỉnh )','',address.title())
    if res.isnumeric():
        return prefix+res
    return res

def populate_database(session, real_estate_data):
    # insert the data
    for row in real_estate_data:

        author = (
            session.query(Author)
            .filter(Author.post_author == row["post_author"], Author.phone_number == row["phone_number"])
            .one_or_none()
        )
        if author is None:
            author = Author(
                post_author = row["post_author"], phone_number = row["phone_number"]
            )
            session.add(author)

        # row['addr_province'] = normalize_address(row['addr_province'], '')
        # row['addr_city'] = normalize_address(row['addr_city'],'Quận ')
        # row['addr_district'] = normalize_address(row['addr_district'],'Quận ')
        # row['addr_ward'] = normalize_address(row['addr_ward'],'Phường ')
        row['addr_province'] = re.sub('(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )','',row['addr_province'].lower())
        row['addr_city'] = re.sub('(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )','',row['addr_city'].lower())
        row['addr_district'] = re.sub('(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )','',row['addr_district'].lower())
        row['addr_ward'] = re.sub('(huyện |thành phố |thị xã |quận |phường |thị trấn |xã |tỉnh )','',row['addr_ward'].lower())
        # if row['add_province'].isnumeric():

        address = (
            session.query(Address)
            .filter(
                Address.addr_province == row["addr_province"], Address.addr_city == row["addr_city"],
                Address.addr_district == row["addr_district"], Address.addr_ward == row["addr_ward"],
                Address.addr_street == row["addr_street"]
            )
            .one_or_none()
        )
        if address is None:
            address = Address(
                addr_province = row["addr_province"], addr_city = row["addr_city"],
                addr_district = row["addr_district"], addr_ward = row["addr_ward"],
                addr_street = row["addr_street"]
            )
            session.add(address)

        project = (
            session.query(Project)
            .filter(Project.project == row["project"], Project.project_size == row["project_size"])
            .one_or_none()
        )
        if project is None:
            project = Project(project = row["project"], project_size = row["project_size"])
            session.add(project)

        property_type = (
            session.query(Property_type)
            .filter(Property_type.property_type == row["property_type"])
            .one_or_none()
        )
        if property_type is None:
            property_type = Property_type(property_type = row["property_type"])
            session.add(property_type)

        transaction_type = (
            session.query(Transaction_type)
            .filter(Transaction_type.transaction_type == row["transaction_type"])
            .one_or_none()
        )
        if transaction_type is None:
            transaction_type = Transaction_type(transaction_type = row["transaction_type"])
            session.add(transaction_type)

        post = (
            session.query(Post)
            .filter(Post.url == row["url"])
            .one_or_none()
        )
        if post is None:
            post = Post(
                url = row["url"], price = row["price"], price_unit = row["price_unit"], area = row["area"],
                num_bedrooms = row["num_bedrooms"], num_bathrooms = row["num_bathrooms"],
                created_date = row["created_date"], expired_date = row["expired_date"],
                num_floors = row["num_floors"], floorth = row["floorth"], direction = row["direction"],
                legal = row["legal"], front = row["front"], alley = row["alley"]
            )
            session.add(post)

        # add the items to the relationships
        author.posts.append(post)
        address.posts.append(post)
        project.posts.append(post)
        property_type.posts.append(post)
        transaction_type.posts.append(post)
        session.commit()

    session.close()


def main():
    print("starting")

    # get the real estate data into a dictionary structure
    with resources.path(
        "project.data", "real_estate_integrated.csv"
    ) as csv_filepath:
        data = get_real_estate_data(csv_filepath)
        real_estate_data = data

    engine = create_engine(URL(**settings.DATABASE))
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    populate_database(session, real_estate_data)

    print("finished")


if __name__ == "__main__":
    main()

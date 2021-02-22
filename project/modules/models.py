from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Address(Base):
   __tablename__ = 'address'
   addr_id = Column(Integer, primary_key=True)

   addr_province = Column(String)
   addr_city = Column(String)
   addr_district = Column(String)
   addr_ward = Column(String)
   addr_street = Column(String)
   posts = relationship("Post", backref=backref("address"))

class Region(Base):
   __tablename__ = 'region'
   region_id = Column(Integer, primary_key=True)

   city = Column(String)
   district = Column(String)
   ward = Column(String)

class Author(Base):
   __tablename__ = 'author'
   author_id = Column(Integer, primary_key=True)

   phone_number = Column(String)
   post_author = Column(String)
   posts = relationship("Post", backref=backref("author"))

class Project(Base):
   __tablename__ = 'project'
   project_id = Column(Integer, primary_key=True)

   project = Column(String)
   project_size = Column(String)
   posts = relationship("Post", backref=backref("project"))

class Property_type(Base):
   __tablename__ = 'property_type'
   property_type_id = Column(Integer, primary_key=True)

   property_type = Column(String)
   posts = relationship("Post", backref=backref("property_type"))

class Transaction_type(Base):
   __tablename__ = 'transaction_type'
   transaction_type_id = Column(Integer, primary_key=True)

   transaction_type = Column(String)
   posts = relationship("Post", backref=backref("transaction_type"))

class Post(Base):
   __tablename__ = 'post'
   url = Column(Text, primary_key=True)

   price = Column(String)
   price_unit = Column(String)
   area = Column(String)
   num_bedrooms = Column(String)
   num_bathrooms = Column(String)
   created_date = Column(String)
   expired_date = Column(String)
   num_floors = Column(String)
   floorth = Column(String)
   direction = Column(String)
   legal = Column(String)
   front = Column(String)
   alley = Column(String)
   addr_id = Column(Integer, ForeignKey("address.addr_id"))
   project_id = Column(Integer, ForeignKey("project.project_id"))
   property_type_id = Column(Integer, ForeignKey("property_type.property_type_id"))
   transaction_type_id = Column(Integer, ForeignKey("transaction_type.transaction_type_id"))
   author_id = Column(Integer, ForeignKey("author.author_id"))
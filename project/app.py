from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify, request, render_template
import math
from sqlalchemy.engine.url import URL
import settings
from project.modules.models import Base, Address, Author, Project, Property_type, Transaction_type, Post, Region
app = Flask(__name__)

engine = create_engine(URL(**settings.DATABASE))
Base.metadata.create_all(engine)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    per_page_record = 10
    # Look for a GET variable page if not found default is 1.        
    if request.args.get('page'):  
        page  = int(request.args['page'])        
    else:  
        page=1  
  
    start_from = (page-1) * per_page_record
    province = request.args.get("province")
    district = request.args.get("district")
    ward = request.args.get("ward")
    project_id = request.args.get("project_id")
    property_type_id = request.args.get("property_type_id")
    transaction_type_id = request.args.get("transaction_type_id")
    # if request.args.get("province") and request.args.get("district") and request.args.get("ward"):
    cities = ['hồ chí minh', 'hà nội', 'hải phòng', 'cần thơ', 'đà nẵng']
    if province in cities: 
        filter_data = {'addr_city': province, 'addr_district': district, 'addr_ward':ward}
        filter_data = {key: value for (key, value) in filter_data.items() if value}
        post_data = {'project_id': project_id, 'property_type_id': property_type_id, 'transaction_type_id': transaction_type_id}
        post_data = {key: value for (key, value) in post_data.items() if value}
        res = session.query(Post).filter_by(**post_data).join(Address).filter_by(**filter_data).limit(per_page_record).offset(start_from)
        total_records = session.query(Post).filter_by(**post_data).join(Address).filter_by(**filter_data).count()
        # res = session.query(Address, Post)\
        #             .filter(Address.addr_id == Post.addr_id)\
        #             .filter_by(**filter_data).limit(per_page_record).offset(start_from)
        # total_records = session.query(Address, Post)\
        #             .filter(Address.addr_id == Post.addr_id)\
        #             .filter_by(**filter_data).count()
        # else:
        #     res = session.query(Address, Post)\
        #             .filter(Address.addr_id == Post.addr_id,\
        #             Address.addr_province == province, Address.addr_city == district, Address.addr_ward == ward).limit(per_page_record).offset(start_from)
        #     total_records = session.query(Address, Post)\
        #             .filter(Address.addr_id == Post.addr_id,\
        #             Address.addr_province == province, Address.addr_city == district, Address.addr_ward == ward).count()
    else:
        filter_data = {'addr_province': province, 'addr_city': district, 'addr_ward':ward}
        filter_data = {key: value for (key, value) in filter_data.items() if value}
        post_data = {'project_id': project_id, 'property_type_id': property_type_id, 'transaction_type_id': transaction_type_id}
        post_data = {key: value for (key, value) in post_data.items() if value}
        # res = session.query(Address, Post)\
        #             .filter(Address.addr_id == Post.addr_id)\
        #             .filter_by(**filter_data).limit(per_page_record).offset(start_from)
        # total_records = session.query(Address, Post)\
        #             .filter(Address.addr_id == Post.addr_id)\
        #             .filter_by(**filter_data).count()
        res = session.query(Post).filter_by(**post_data).join(Address).filter_by(**filter_data).limit(per_page_record).offset(start_from)
        total_records = session.query(Post).filter_by(**post_data).join(Address).filter_by(**filter_data).count()
    result = []
    for p in res:
        result.append({"price":p.price, "price_unit":p.price_unit, "area": p.area, "transaction_type":p.transaction_type.transaction_type,
            "property_type":p.property_type.property_type, "addr_province":p.address.addr_province, "addr_city":p.address.addr_city,
            "addr_district":p.address.addr_district, "addr_ward":p.address.addr_ward, "addr_street":p.address.addr_street,
            "num_bedrooms":p.num_bedrooms, "num_bathrooms":p.num_bathrooms, "project":p.project.project,
            "project_size":p.project.project_size, "created_date":p.created_date, "expired_date":p.expired_date,
            "num_floors":p.num_floors, "floorth":p.floorth, "direction":p.direction, "legal":p.legal,
            "front":p.front, "alley":p.alley, "post_author":p.author.post_author, "phone_number":p.author.phone_number,
            "url":p.url})
    total_pages = math.ceil(total_records / per_page_record)
    if request.args.get("province") and request.args.get("district") and request.args.get("ward"):
        return render_template("index.html",province=province, district=district, ward=ward, rows = result, total_records = total_records, page = page, total_pages=total_pages)
    else:
        return render_template("index.html",province="", district="", ward="", rows = result, total_records = total_records, page = page, total_pages=total_pages)

@app.route('/province')
def getProvince():
    result=[]
    for value in session.query(Region.city).distinct().order_by(Region.city.asc()):
        result.append(value.city)
    return jsonify(result)

@app.route('/district', methods=['GET'])
def getDistrict():
    city = request.args.get('id')
    result=[]
    for value in session.query(Region.district).filter(Region.city == city).distinct().order_by(Region.district.asc()):
        result.append(value.district)
    return jsonify(result)

@app.route('/ward', methods=['GET'])
def getWard():
    district = request.args.get('district_id')
    city = request.args.get('city_id')
    result=[]
    for value in session.query(Region.ward).filter(Region.city == city, Region.district == district).distinct().order_by(Region.ward.asc()):
        result.append(value.ward)
    return jsonify(result)

@app.route('/project')
def getProject():
    result={}
    for value in session.query(Project).all():
        result[value.project_id] = value.project
    return jsonify(result)

@app.route('/property')
def getProperty():
    result={}
    for value in session.query(Property_type).all():
        result[value.property_type_id] = value.property_type
    return jsonify(result)

@app.route('/transaction')
def getTransaction():
    result={}
    for value in session.query(Transaction_type).all():
        result[value.transaction_type_id] = value.transaction_type
    return jsonify(result)
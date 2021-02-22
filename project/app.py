from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify, request, render_template
import math
from project.modules.models import Base, Address, Author, Project, Property_type, Transaction_type, Post, Region
app = Flask(__name__)

engine = create_engine('postgresql://postgres:fuckyou2810@localhost:5432/real_estate_dev')
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
    if request.args.get("province") and request.args.get("district") and request.args.get("ward"):
        province = request.args.get("province")
        district = request.args.get("district")
        ward = request.args.get("ward")
        cities = ['hồ chí minh', 'hà nội', 'hải phòng', 'cần thơ', 'đà nẵng']
        if province in cities: 
            res = session.query(Address, Post)\
                    .filter(Address.addr_id == Post.addr_id,\
                    Address.addr_city == province, Address.addr_district == district, Address.addr_ward == ward).limit(per_page_record).offset(start_from)
            total_records = session.query(Address, Post)\
                    .filter(Address.addr_id == Post.addr_id,\
                    Address.addr_city == province, Address.addr_district == district, Address.addr_ward == ward).count()
        else:
            res = session.query(Address, Post)\
                    .filter(Address.addr_id == Post.addr_id,\
                    Address.addr_province == province, Address.addr_city == district, Address.addr_ward == ward).limit(per_page_record).offset(start_from)
            total_records = session.query(Address, Post)\
                    .filter(Address.addr_id == Post.addr_id,\
                    Address.addr_province == province, Address.addr_city == district, Address.addr_ward == ward).count()
    else:
        res = session.query(Address, Post)\
                    .filter(Address.addr_id == Post.addr_id).limit(per_page_record).offset(start_from)
        total_records = session.query(Address, Post)\
                    .filter(Address.addr_id == Post.addr_id).count()
    result = []
    for a, p in res:
        result.append({"price":p.price, "price_unit":p.price_unit, "area": p.area, "transaction_type":p.transaction_type.transaction_type,
            "property_type":p.property_type.property_type, "addr_province":a.addr_province, "addr_city":a.addr_city,
            "addr_district":a.addr_district, "addr_ward":a.addr_ward, "addr_street":a.addr_street,
            "num_bedrooms":p.num_bedrooms, "num_bathrooms":p.num_bathrooms, "project":p.project.project,
            "project_size":p.project.project_size, "created_date":p.created_date, "expired_date":p.expired_date,
            "num_floors":p.num_floors, "floorth":p.floorth, "direction":p.direction, "legal":p.legal,
            "front":p.front, "alley":p.alley, "post_author":p.author.post_author, "phone_number":p.author.phone_number,
            "url":p.url})
    total_pages = math.ceil(total_records / per_page_record)
    if request.args.get("province") and request.args.get("district") and request.args.get("ward"):
        return render_template("index.html",province=province, district=district, ward=ward, rows = result, total_records = total_records, page = page, total_pages=total_pages)
    else:
        return render_template("index.html", rows = result, total_records = total_records, page = page, total_pages=total_pages)

@app.route('/province')
def getProvince():
    result=[]
    for value in session.query(Region.city).distinct():
        result.append(value.city)
    return jsonify(result)

@app.route('/district', methods=['GET'])
def getDistrict():
    city = request.args.get('id')
    result=[]
    for value in session.query(Region.district).filter(Region.city == city).distinct():
        result.append(value.district)
    return jsonify(result)

@app.route('/ward', methods=['GET'])
def getWard():
    district = request.args.get('district_id')
    city = request.args.get('city_id')
    result=[]
    for value in session.query(Region.ward).filter(Region.city == city, Region.district == district).distinct():
        result.append(value.ward)
    return jsonify(result)
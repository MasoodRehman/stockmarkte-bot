from flask import Flask, request, render_template, jsonify
import sqlite3 as sql
import json
from helpers import getCompaniesFromJsonFile, dict_factory

app = Flask(__name__)


@app.route('/')
def home():
    """
    Homepage
    ==========================================================
    This function testing purpose to make shure the app is working.

    @method GET
    @return JSON
    """
    return jsonify({
        "status": "success",
        "message": "I am working"
    })


@app.route('/dumpdata')
def dumpdata():
    """
    Data dump function
    ==========================================================
    This function will dump json file data into database.

    @method GET
    @return JSON
    """
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            
            """read companies data from jason line file and insert into datbase"""
            content = getCompaniesFromJsonFile('company_profiles.jl')
            total_items = 0
            if content:
                for item in content:
                    total_items = total_items + 1

                    columns = ', '.join(item.keys())
                    placeholders = ', '.join('?' * len(item))
                    query = 'INSERT INTO companies ({}) VALUES ({})'.format(columns, placeholders)
                    cur.execute(query, item.values())
                    con.commit()
            else:
                raise Exception("Json file is empty")
        message = { 
            "status": "success", 
            "message": "Data dumped successfully, {} items dumped.".format(total_items) 
        }

    except Exception as e:
        message = { 
            "status": "fail", 
            "message": "Unable to dump data: "+ str(e) 
        }
        
    finally:
        return jsonify(message)
        con.close()


@app.route('/companies')
def companies():
    """
    Companies list function
    ==========================================================
    This function will return all the companies saved in database.

    @method GET
    @return JSON
    """
    con = sql.connect("database.db")
    con.row_factory = dict_factory

    cur = con.cursor()

    # Filters
    company_name = request.args.get('company_name')
    industry = request.args.get('industry')
    revenue_gte = request.args.get('revenue_gte')
    if company_name:
        cur.execute("SELECT * FROM companies WHERE company_name = '{}'".format(company_name))
    elif industry:
        cur.execute("SELECT * FROM companies WHERE business = '{}'".format(industry))
    else:
        cur.execute("SELECT * FROM companies")
    
    # Load database data
    data = cur.fetchall()
    
    # Revenu filter
    if revenue_gte:
        _data = list()
        for d in data:
            financial_summary = json.loads(d.get('financial_summary'))
            if financial_summary and financial_summary.get('market_cap').replace(',', '') >= revenue_gte:
                # decode json column string into dictionary of filtered records
                d['business_registration'] = json.loads(d['business_registration'])
                d['company_phone_number'] = json.loads(d['company_phone_number'])
                d['financial_summary'] = json.loads(d['financial_summary'])
                d['crawled_at'] = json.loads(d['crawled_at'])
                _data.append(d)
        data = _data
    else:
        # decode json column string into dictionary of all records
        _data = list()
        for d in data:
            d['business_registration'] = json.loads(d['business_registration'])
            d['company_phone_number'] = json.loads(d['company_phone_number'])
            d['financial_summary'] = json.loads(d['financial_summary'])
            d['crawled_at'] = json.loads(d['crawled_at'])
            _data.append(d)
        data = _data

    return jsonify({ 
        "status_code": 200, 
        "message": "successful",
        "data": data
    })


if __name__ == '__main__':
    app.run(debug = True)

import mysql.connector
from dns.resolver import Resolver
from flask import Flask, jsonify, request
from CapstoneBackend.OUIManager.Config.DatabaseCreds import DatabaseCreds

app = Flask(__name__)
dns_servers = ['1.1.1.1', '1.0.0.1', '208.67.222.222', '208.67.220.220']


@app.route('/macouilookup')
def get_oui():
    resultset = []
    json = request.get_json()
    conn = mysql.connector.connect(
        user=DatabaseCreds.CapstoneDev.user,
        password=DatabaseCreds.CapstoneDev.password,
        host=DatabaseCreds.CapstoneDev.host,
        database='CapStone'
    )
    cur = conn.cursor()
    sql = "select oui, shortName, longName from ouiTbl"
    try:
        cur.execute(sql)
        for (oui, shortName, longName) in cur:
            resultset.append(dict({'oui': oui, 'shortname': shortName, 'longname': longName}))
    except mysql.connector.errors.DatabaseError:
        pass
        # print("SQL:" + str(sql))
    cur.close()
    conn.close()
    return jsonify(resultset)


@app.route('/macouilookup', methods=['POST'])
def lookup_oui():
    resultset = []
    json = request.get_json()
    # json = {"oui": "FC:99:47"}
    conn = mysql.connector.connect(
        user=DatabaseCreds.CapstoneDev.user,
        password=DatabaseCreds.CapstoneDev.password,
        host=DatabaseCreds.CapstoneDev.host,
        database='CapStone'
    )
    cur = conn.cursor()
    sql = "select oui, shortName, longName from ouiTbl WHERE (oui='{}')".format(json['oui'])
    try:
        cur.execute(sql)
        for (oui, shortName, longName) in cur:
            resultset.append(dict({'oui': oui, 'shortname': shortName, 'longname': longName}))
    except mysql.connector.errors.DatabaseError:
        pass
        # print("SQL:" + str(sql))
    cur.close()
    conn.close()
    return jsonify(resultset)


@app.route('/dnscheck')
def lookup_dns():
    r = Resolver()
    resultset = []
    topsites = ['google.com', 'facebook.com', 'apple.com', 'amazon.com']
    r.nameservers = dns_servers
    for topsite in topsites:
        answer = r.query(topsite, 'soa')
        try:
            for soa in answer.rrset.items:
                soa_split = str(soa).split(' ')
                serial = soa_split[2]
                resultset.append(dict({'domain': topsite, 'soa': str(soa), 'serial': serial}))
        except Exception:
            pass
    return jsonify(resultset)


@app.route('/dnscheck', methods=['POST'])
def lookup_dns_byname():
    r = Resolver()
    resultset = []
    json = request.get_json()
    site = json['domain']
    r.nameservers = dns_servers
    answer = r.query(str(site), 'soa')
    try:
        for soa in answer.rrset.items:
            soa_split = str(soa).split(' ')
            serial = soa_split[2]
            resultset.append(dict({'domain': site, 'soa': str(soa), 'serial': serial}))
    except Exception:
        pass
    return jsonify(resultset)

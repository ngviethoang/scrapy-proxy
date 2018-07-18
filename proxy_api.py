# -*- coding: utf-8 -*-
""" RESTful API for getting proxies in database """

import pymongo
from crawl_proxy.custom_settings import mongo_settings
from flask import Flask, request, jsonify, abort


client = pymongo.MongoClient(mongo_settings['URI'])
db = client[mongo_settings['DATABASE']]

app = Flask(__name__)


@app.route('/proxies')
def get_proxies():
    limit = request.args.get('limit', 0)
    has_details = request.args.get('dt', False)
    if has_details is not False:
        has_details = True

    try:
        limit = int(limit)
    except ValueError:
        limit = 0

    proxies = db[mongo_settings['PROXIES_COLLECTION']].find({'run_time': {'$exists': True}}, {'_id': False})\
        .sort([('run_time', 1)]).limit(limit)

    if not has_details:
        proxies = [proxy['proxy'] for proxy in proxies]
    else:
        proxies = [proxy for proxy in proxies]

    return jsonify(proxies)


@app.route('/brands')
def get_brand_urls():
    brand_urls = db[mongo_settings['RESULTS_COLLECTION']].distinct('brand_url')

    return jsonify(brand_urls)


@app.route('/proxy/update')
def update_proxy():
    proxy = request.args.get('p', None)

    run_time = request.args.get('r', '')
    try:
        run_time = int(run_time)
    except ValueError:
        run_time = None

    if proxy is None or run_time is None:
        return 'Error', 500
    else:
        db[mongo_settings['PROXIES_COLLECTION']].update_one(filter={'proxy': proxy},
                                                            update={'$set': {'run_time': run_time}})
        return 'Success', 200


if __name__ == '__main__':
    app.run(port='5000', debug=True)

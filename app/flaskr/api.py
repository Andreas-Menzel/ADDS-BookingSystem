import functools

from flask import (
    Blueprint, flash, g, jsonify, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# Import own files
from functions_collection import *


bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/warehouse_info')
def warehouse_info():
    response = get_response_template(payload=True)

    # Get values from URL (or POST)
    warehouse_id = request.values.get('id')

    # Check if all required values were given
    response = check_argument_not_null(response, warehouse_id, 'warehouse_id')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    #
    db_warehouse_info = db.execute(
        'SELECT * FROM warehouses WHERE id = ?', (warehouse_id,)).fetchone()
    if db_warehouse_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Warehouse with id "{warehouse_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    response['payload']['id'] = db_warehouse_info['id']
    response['payload']['name'] = db_warehouse_info['name']
    response['payload']['address'] = db_warehouse_info['address']

    return jsonify(response)


@bp.route('/product_info')
def product_info():
    response = get_response_template(payload=True)

    # Get values from URL (or POST)
    product_id = request.values.get('id')

    # Check if all required values were given
    response = check_argument_not_null(response, product_id, 'product_id')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    #
    db_product_info = db.execute(
        'SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    if db_product_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Product with id "{product_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    response['payload']['id'] = db_product_info['id']
    response['payload']['name'] = db_product_info['name']
    response['payload']['description'] = db_product_info['description']
    response['payload']['weight'] = db_product_info['weight']

    return jsonify(response)


@bp.route('/stocks')
def stocks():
    response = get_response_template(payload=True)

    # Get values from URL (or POST)
    warehouse_id = request.values.get('warehouse_id')
    include_product_info = request.values.get('include_product_info')

    # Check if all required values were given
    response = check_argument_not_null(response, warehouse_id, 'warehouse_id')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    if include_product_info is None:
        include_product_info = False
    else:
        response, include_product_info = check_argument_type(
            response, include_product_info, 'include_product_info', 'boolean')

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db = get_db()

    # Check if warehouse exists
    db_warehouse_info = db.execute(
        'SELECT id FROM warehouses WHERE id = ?', (warehouse_id,)).fetchone()
    if db_warehouse_info is None:
        response = add_error_to_response(
            response,
            1,
            f'Warehouse with id "{warehouse_id}" not found.',
            False
        )

    # Return if an error already occured
    if not response['executed']:
        return jsonify(response)

    db_stocks = db.execute(
        'SELECT * FROM stocks WHERE warehouse_id = ?', (warehouse_id,)).fetchall()

    response['payload']['stocks'] = []
    for stock in db_stocks:
        stock_info = {
            'warehouse_id': stock['warehouse_id'],
            'product_id': stock['product_id'],
            'quantity': stock['quantity']
        }

        if include_product_info:
            stock_info['product_info'] = {}
            db_product_info = db.execute(
                'SELECT * FROM products WHERE id = ?', (stock['product_id'],)).fetchone()
            stock_info['product_info']['id'] = db_product_info['id']
            stock_info['product_info']['name'] = db_product_info['name']
            stock_info['product_info']['description'] = db_product_info['description']
            stock_info['product_info']['weight'] = db_product_info['weight']

        response['payload']['stocks'].append(stock_info)

    return jsonify(response)

import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp
from utils.utils import ROOT_PATH, tpl_path
import simplejson
from google.appengine.api import urlfetch
import urllib

import utils.gchecky.model as gmodel
import utils.gchecky.controller as gcontroller
import uuid


PQ_MERCHANT_ID = 214037498108639

PQ_MERCHANT_KEY = "heGOVhmPg4oFuIr_ruIzOw"


class Level2Controller(gcontroller.Controller):
    def __init__(self,merchant_id,merchant_key,is_sandbox=True,currency='USD'):
        gcontroller.Controller.__init__(self,merchant_id,merchant_key,
                                        is_sandbox,currency)
    def handle_new_order(self, message, order_id, order, context):
        id=int(message.shopping_cart.items[0].merchant_item_id)
        db(db.order.id==id).update(order_id=order_id,status='SUBMITTED')
        return gmodel.ok_t()
    def handle_order_state_change(self, message, order_id, order, context):
        db(db.order.order_id==order_id).update(status=message.financial_order_state)
        return gmodel.ok_t()
    def handle_charge_amount(self, message, order_id, order, context):
        db(db.order.order_id==order_id).update(status='CHARGED')
        return gmodel.ok_t()


mycontroller=Level2Controller(GOOGLE_MERCHANT_ID,GOOGLE_MERCHANT_KEY,is_sandbox=True)




def notify():
    response.headers['Content-Type']='text/xml'
    return mycontroller.receive_xml(request.body.read())

def index(): redirect(URL(r=request,f='checkout'))

def checkout():
    session.id=db.order.insert(status='PRE-PROCESSING')
    order=gmodel.checkout_shopping_cart_t()
    order.shopping_cart=gmodel.shopping_cart_t(items=[])
    order.shopping_cart.items.append(
        gmodel.item_t(merchant_item_id = session.id,
                      name             = 'apple',
                      description      = 'a tasty fruit!',
                      unit_price       = gmodel.price_t(value=0.99,currency='USD'),
                      quantity         = 1))
    next='http://web2py.appspot.com/plugin_checkout/default/checkorder'
    order.checkout_flow_support=gmodel.checkout_flow_support_t(
        continue_shopping_url=next,request_buyer_phone_number=False)
    prepared = mycontroller.prepare_order(order)
    return dict(button=XML(prepared.html()))

def checkorder():
    if not session.id: redirect('checkout')
    rows=db(db.order.id==session.id).select()
    if not rows: redirect('checkout')
    return dict(status=rows[0].status)

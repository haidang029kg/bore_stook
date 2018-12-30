from Book_Flask import db
from datetime import datetime, timedelta
from Book_Flask.models import Orders, OrderDetails, generate_id
from assoRule import *


# Trans-id | Items        min_sup = .6
# 1        | ACD          min_conf = .75
# 2        | BCE
# 3        | ABCE
# 4        | BE
# 5        | ABCE

# rule     | conf
# BC->E    | 1
# BE->C    | 1/4
# CE->B    | 1
# B->CE    | 1/4
# C->BE    | 1/4
# E->BC    | 1/4
# Mapping
# Items | BookID
# A     | 64857
# B     | 64864
# C     | 89165
# D     | 102525
# E     | 257990


#Transaction 1
order_id = generate_id('order')
data_order = Orders(OrderID=order_id,
                        UserID=1,
                        Address='transaction 1',
                        Phone='0912345678',
                        Date=datetime.now() - timedelta(4),
                        TotalPrice=28.18,
                        IsPaid=1,
                        Status=1,
                        PaymentMethod=1)
data_order_details = []
order_details = {64857:2, 89165:1, 102525:1}
for k,v in order_details.items():
    each_detail = OrderDetails(OrderID=order_id,
                               BookID=k,
                               Quantity=v)
    data_order_details.append(each_detail)

if (data_order):
    if (data_order_details):
        db.session.add(data_order)

        for i in data_order_details:
            db.session.add(i)
        db.session.commit()


#Transaction 2
order_id = generate_id('order')
data_order = Orders(OrderID=order_id,
                        UserID=1,
                        Address='transaction 2',
                        Phone='0912345678',
                        Date=datetime.now() - timedelta(3),
                        TotalPrice=40.05,
                        IsPaid=1,
                        Status=1,
                        PaymentMethod=1)
data_order_details = []
order_details = {64864:2, 89165:1, 257990:3}
for k,v in order_details.items():
    each_detail = OrderDetails(OrderID=order_id,
                               BookID=k,
                               Quantity=v)
    data_order_details.append(each_detail)

if (data_order):
    if (data_order_details):
        db.session.add(data_order)

        for i in data_order_details:
            db.session.add(i)
        db.session.commit()


#Transaction 3
order_id = generate_id('order')
data_order = Orders(OrderID=order_id,
                        UserID=1,
                        Address='transaction 3',
                        Phone='0912345678',
                        Date=datetime.now() - timedelta(2),
                        TotalPrice=33.88,
                        IsPaid=1,
                        Status=1,
                        PaymentMethod=1)
data_order_details = []
order_details = {64857:2, 64864:1, 89165:1, 257990:1}
for k,v in order_details.items():
    each_detail = OrderDetails(OrderID=order_id,
                               BookID=k,
                               Quantity=v)
    data_order_details.append(each_detail)

if (data_order):
    if (data_order_details):
        db.session.add(data_order)

        for i in data_order_details:
            db.session.add(i)
        db.session.commit()


#Transaction 4
order_id = generate_id('order')
data_order = Orders(OrderID=order_id,
                        UserID=1,
                        Address='transaction 4',
                        Phone='0912345678',
                        Date=datetime.now() - timedelta(1),
                        TotalPrice=30.58,
                        IsPaid=1,
                        Status=1,
                        PaymentMethod=1)
data_order_details = []
order_details = {64864:2, 257990:2}
for k,v in order_details.items():
    each_detail = OrderDetails(OrderID=order_id,
                               BookID=k,
                               Quantity=v)
    data_order_details.append(each_detail)

if (data_order):
    if (data_order_details):
        db.session.add(data_order)

        for i in data_order_details:
            db.session.add(i)
        db.session.commit()


#Transaction 5
order_id = generate_id('order')
data_order = Orders(OrderID=order_id,
                        UserID=1,
                        Address='transaction 5',
                        Phone='0912345678',
                        Date=datetime.now(),
                        TotalPrice=32.17,
                        IsPaid=1,
                        Status=1,
                        PaymentMethod=1)
data_order_details = []
order_details = {64857:1, 64864:1, 89165:1, 257990:2}
for k,v in order_details.items():
    each_detail = OrderDetails(OrderID=order_id,
                               BookID=k,
                               Quantity=v)
    data_order_details.append(each_detail)

if (data_order):
    if (data_order_details):
        db.session.add(data_order)

        for i in data_order_details:
            db.session.add(i)
        db.session.commit()



items, rules = runApriori(0.6,0.75)


printResults(items, rules)


saveRules(rules)

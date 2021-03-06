from models import Coupon, User, Restaurant
from datetime import date

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def insert_coupon(rid, name, points, description, level, begin, expiration, indefinite):
    """
    Inserts a coupon into Coupon table.

    Args:
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
            table. An integer.
        name: A name for the coupon. A 64 character string.
        points: A point value for the coupon. An integer.
        description: A description of the coupon. A 1024 character string.
        level: A level that restricts only users reach this level or above in 
            the restaurant can purchase/use(available). An unsigned Int
        begin: A starting date for the coupon. A DateTime.
        expiration: An ending date for the coupon. A DateTime.
        indefinite: A boolean with the following property:
          true == coupon has no begining/ending date.
          false == coupon has a begining/ending date.

    Returns:
        None if coupon was successfully added to the Coupon table, a list of
        error messages otherwise.
    """
    errmsg = []

    if points == "" or int(points) < 0:
        errmsg.append("Invalid amount for points.")
    if name == "":
        errmsg.append("Invalid coupon name, please give your coupon a name.")
    if level == "" or int(level) < 0:
        errmsg.append("Invalid level requirement, please give a non-negative value.")
    if not indefinite and ((expiration == None or begin == None) or (expiration == "" or begin == "")):
        errmsg.append("Missing start or expiration date.")
    elif not indefinite and expiration < begin:
        errmsg.append("Invalid date interval, begin date must be before expiration date.")

    if not errmsg:
        if indefinite:
            coupon = Coupon(rid = rid, name = name, points = points, description = description, level = level, deleted = 0)
        else:
            coupon = Coupon(rid = rid, name = name, points = points, description = description, level = level, expiration = expiration, begin = begin, deleted = 0)
        db.session.add(coupon)
        db.session.commit()
        return None

    return errmsg


def get_coupons(rid):
    """
    Fetches rows from the Coupon table.

    Retrieves a list of coupons from the Coupon table that belong to the
    restaurant with the given restaurant ID.

    Args:
        rid: A restaurant ID that corresponds to a restaurant in the Restaurant
          table. A integer.

    Returns:
        A list of coupons containing for a restaurant with restaurant ID that
        matches rid.
    """
    coupon_list = []
    coupons = Coupon.query.filter(Coupon.rid == rid).all()
    for c in coupons:
        dict = {
            "cid": c.cid,
            "name": c.name,
            "description": c.description,
            "points": c.points,
            "level": c.level,
            "begin": c.begin,
            "expiration": c.expiration,
            "deleted": c.deleted
        }
        coupon_list.append(dict)
    return coupon_list

def is_today_in_coupon_date_range(coupon):
    """
    Checks whether today is in, before, or after the range of
    valid dates for a coupon.

    Args:
        coupon: The coupon to be checked

    Returns:
        -1, if today is before the coupon date range;
        0, if today is within the coupon date range;
        1, if today is after the coupon date range.
    """
    today = date.today()
    if coupon.expiration:
        if today > coupon.expiration:
            return 1
        if today < coupon.begin:
            return -1
    return 0

def delete_coupon(cid):
    """
    Removes a row from the Coupon table.

    Deletes a coupon from the database.

    Args:
        cid: A coupon ID that corresponds to a coupon in the Coupon table. A
          integer.

    Returns:
        None.
    """
    coupon = Coupon.query.filter(Coupon.cid == cid).first()
    coupon.deleted = 1
    db.session.commit()
    return None


def filter_valid_coupons(coupons):
    """
    Removes invalid coupons from the coupons list.

    Deletes coupons that are either deleted or expired.

    Args:
        coupons: A list of dictinaries, each dictinary must have the keys,
          int 'deleted' and DateTime 'expiration'.

    Returns:
        A the list coupons with the invalid dictinaries removed.
    """
    today = date.today()
    copy = coupons[:]
    for c in copy:
        if (c["deleted"] == 1) or (c["expiration"] != None and today > c["expiration"]):
            coupons.remove(c)

    return coupons


def get_coupon_by_cid(cid):
    """
    Get a list of dictionary which contains all coupon info by the given cid

    Args:
        cid: A coupon ID that corresponds to a coupon in the Coupon table.

    Returns"
        (if found) a list of dictionary
        (if not) None
    """

    coupon = Coupon.query.filter(Coupon.cid == cid).first()

    if coupon:
        c = {
            "cid": coupon.cid,
            "rid": coupon.rid,
            "points": coupon.points,
            "cname": coupon.name,
            "cdescription": coupon.description,
            "clevel": coupon.level,
            "begin": coupon.begin,
            "expiration": coupon.expiration,
            "status": is_today_in_coupon_date_range(coupon)
        }

        return c
    else:
        return None


def find_res_name_of_coupon_by_cid(cid):
    """
    Get the restaurant name by the given cid

    Args:
        cid: A coupon ID that corresponds to a coupon in the Coupon table.

    Returns:
        (if found) restaurant name
        (if not) 'Not Found'
    """
    coupon = Coupon.query.filter(Coupon.cid == cid).first()
    if coupon:
        restaurant = Restaurant.query.filter(Restaurant.rid == coupon.rid).first()
        if restaurant:
            return restaurant.name
        return "Not Found"
    else:
        return "Not Found"


def find_res_addr_of_coupon_by_cid(cid):
    """
    Get the restaurant address by the given cid

    Args:
        cid: A coupon ID that corresponds to a coupon in the Coupon table.

    Returns:
        (if found) restaurant address
        (if not) 'Not Found'
    """
    coupon = Coupon.query.filter(Coupon.cid == cid).first()
    if coupon:
        restaurant = Restaurant.query.filter(Restaurant.rid == coupon.rid).first()
        if restaurant:
            return restaurant.address
        return "Not Found"
    else:
        return "Not Found"

def get_rid_by_cid(cid):
    """
    Get rid by the given cid

    Args:
        cid: A coupon ID that corresponds to a coupon in the Coupon table.

    Returns:
        (if found) restaurant id
        (if not) 'Not Found'
    """
    c = Coupon.query.filter(Coupon.cid == cid).first()
    if c:
        return c.rid
    return "Not Found"

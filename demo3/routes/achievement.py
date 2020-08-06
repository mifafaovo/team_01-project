###################################################
#                                                 #
#   Includes all routes to achievement page.      #
#   This includes my achievements and create an   #
#   achievement.                                  #
#                                                 #
###################################################

from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from databaseHelpers.achievement import *
from databaseHelpers.restaurant import *
from databaseHelpers.qr_code import *
from databaseHelpers.achievementProgress import *
from databaseHelpers.employee import *
from databaseHelpers.restaurant import verify_scan_list

achievement_page = Blueprint('achievement_page', __name__, template_folder='templates')

@achievement_page.route('/achievement.html', methods=['GET', 'POST'])
@achievement_page.route('/achievement', methods=['GET', 'POST'])
def achievement():
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners and employees only, if user is a customer, redirect to home page
    elif session['type'] == -1:
        return redirect(url_for('home_page.home'))

    else:
        if request.method == 'POST':
            aid = request.form['achievement']
            delete_achievement(aid)
    #get achievements
    if session['type'] == 1:
        rid = get_rid(session["account"])
    else:
        rid = get_employee_rid(session["account"])
    achievement_list = filter_expired_achievements(rid)

    return render_template("achievement.html", achievements = achievement_list)


# To create an achievement
@achievement_page.route('/createAchievement.html', methods=['GET', 'POST'])
@achievement_page.route('/createAchievement', methods=['GET', 'POST'])
def create_achievement():
    # If someone is not logged in redirects them to login page, same as coupon
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to owners only, if user is not an owner, redirect to home page
    elif session['type'] != 1:
        return redirect(url_for('home_page.home'))

    if request.method == 'POST':
        rid = get_rid(session["account"])
        name = request.form['name']
        experience = request.form['experience']
        points = request.form['points']
        type = int(request.form.get('type'))
        item = request.form['item'].replace(";", "")
        amount = request.form['amount' + str(type)]
        end = request.form['end']
        begin = request.form['start']
        indefinite = "indefinite" in request.form

        value = item + ";" + amount + ";" + str(indefinite) + ";" + begin + ";" + end

        errmsg = get_errmsg(name, experience, points, type, value)

        if not errmsg:
            insert_achievement(rid, name, experience, points, type, value)
            return redirect(url_for('achievement_page.achievement'))
        else:
            return render_template('createAchievement.html', errmsg = errmsg)

    return render_template('createAchievement.html')

@achievement_page.route('/verifyAchievement/<aid>/<uid>', methods=['GET', 'POST'])
def use_achievement(aid, uid):
    scanner = session['account']
    rid = get_rid_by_aid(aid)
    access = verify_scan_list(rid)
    # If someone is not logged in redirects them to login page
    if 'account' not in session:
        return redirect(url_for('login_page.login'))

    # Page is restricted to employee/owner only, if user is a customer, redirect to home page
    elif session['type'] == -1 or scanner not in access:
        return redirect(url_for('qr_page.scan_failure'))

    # get achievement
    achievement = get_exact_achivement_progress(aid, uid)
    if achievement:
        add_one_progress_bar(achievement, aid, uid)
        return redirect(url_for('qr_page.scan_successful'))

    return redirect(url_for('qr_page.scan_no_coupon'))

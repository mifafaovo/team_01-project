from models import Achievements, Customer_Achievement_Progress, Points

import config
if config.STATUS == "TEST":
    from models import db
else:
    from exts import db


def get_achievement_progress_by_uid(uid):
    """
    Fetches rows from the Achievement Progress table.

    Retrieves a list of achievement progress from the Achievement Progress table that
    belongs to the user with the given user ID.

    Args:
        uid: A user ID that corresponds to a user in the User
          table. An integer.

    Returns:
        A list of achievement progress for a user with user ID that
        matches uid.
    """
    achievement_progress_list = []
    achievement_progress = Customer_Achievement_Progress.query.filter(Customer_Achievement_Progress.uid == uid).all()
    for a in achievement_progress:
        dict = {
            "aid": a.aid,
            "progress": a.progress,
            "progressMax": a.total,
        }
        achievement_progress_list.append(dict)
    return achievement_progress_list

def get_achievements_with_no_progress(achievements, uid):
    """
    Filters achievements with zero progress by the given user from a
    list of achievements and appends progress data to each achievement.

    Args:
        achievements: The achievements to be filtered. A list of dict items
            with aid, description, experience, points, and progressMax keys.
        uid: A user ID that corresponds to a user in the User
            table. An integer.

    Returns:
        A list of achievements with progress data.
    """
    achievement_progress_list = get_achievement_progress_by_uid(uid)
    filtered_achievements = []
    for a in achievements:
        has_progress = False
        for p in achievement_progress_list:
            if a["aid"] == p["aid"]:
                has_progress = True
                break
        if not has_progress:
            a["progress"] = 0
            filtered_achievements.append(a)
    return filtered_achievements

def get_exact_achivement_progress(aid, uid):
    """
    Get the exact achivement progress by applying both aid and uid to it
    :param aid: achievement id
    :param uid: user id
    :return: Customer_Achievement_Progress if found
             'Not Found' if not found
    """
    achievement_progress = Customer_Achievement_Progress.query.filter(Customer_Achievement_Progress.aid==aid,
                                                                      Customer_Achievement_Progress.uid==uid).first()

    if achievement_progress:
        return achievement_progress
    else:
        return 'Not Found'


def add_one_progress_bar(achievements_progress):
    achievements_progress.progress += 1
    if achievements_progress.progress == achievements_progress.total:
        complete_progress(achievements_progress)
    db.session.commit()
    return None


def complete_progress(achievement_progress):
    rid = get_rid_points_by_aid(achievement_progress.aid)['rid']
    uid = achievement_progress.uid
    points = get_rid_points_by_aid(achievement_progress.aid)['points']

    user_point = Points.query.filter(Points.uid==uid, Points.rid==rid).first()
    if not user_point:
        user_point = Points(uid=uid, rid=rid, points=points)
        db.session.add(user_point)
    else:
        user_point.points += points
    db.session.delete(achievement_progress)
    db.session.commit()
    return None


def get_rid_points_by_aid(aid):
    achievement = Achievements.query.filter(Achievements.aid==aid).first()
    if achievement:
        return {'rid': achievement.rid,
                'points': achievement.points}
    return 'Not Found'




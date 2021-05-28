#!/usr/bin/env python3

import instaloader
import pytz, datetime, time
import random

from config import *
from text_vars import *

debug_mode = False

class Commenter:
    def __init__(self, name, min_tags):
        self.name = name
        self.tags_count = 0
        self.tags_ids = []
        self.invalid_tags = []
        self.invalid_tags_count = 0
        self.invalid_date = 'N/A'
        self.is_follower = True
        self.is_liker = True
        self.has_min_tags = False
        self.min_tags = min_tags
        self.date = 'N/A'
        self.valid = False
    def process_tags(self, text, comment_date, deadline):
        if min_tags != 0:
            for item in text.split():
                if item.startswith('@'):
                    if item not in self.tags_ids:
                        self.verify_date(item, comment_date, deadline)
        else:
            self.verify_date(text, comment_date, deadline)

    def verify_date(self, item, comment_date, deadline):
        if (comment_date > deadline):
            self.invalid_tags_count += 1
            self.invalid_tags.append(item)
            self.invalid_date = comment_date
        else:
            self.tags_ids.append(item)
            self.tags_count += 1
            if self.date != 'N/A':
                if self.date < comment_date:
                    self.date = comment_date
            if self.tags_count >= self.min_tags:
                self.valid = True
                self.has_min_tags = True

def debug(status='d', msg=""):
    if debug_mode:
        now = datetime.datetime.now()
        dt_str = now.strftime("%d/%m/%Y %H:%M:%S")
        debug_str = "[{}] ".format(dt_str)
        if status.lower() == 'd':
            debug_str += "DEBUG: "
        elif status.lower() == 'i':
            debug_str += "INFO:  "
        elif status.lower() == 'w':
            debug_str += "WARN:  "
        elif status.lower() == 'e':
            debug_str += "ERROR: "
        else:
            debug_str += "MESG:  "
        debug_str += msg
        print(debug_str)

def utc_to_custom_tz(utc_dt, tz_name):
    user_tz = pytz.timezone(tz_name)
    user_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(user_tz)
    return user_tz.normalize(user_dt)

def set_deadline(deadline_dict, tz_name):
    dl_date = datetime.datetime(deadline_dict['year'], deadline_dict['month'], deadline_dict['day'])
    dl_time = datetime.time(deadline_dict['hour'], deadline_dict['minute'])
    return datetime.datetime.combine(dl_date.date(), dl_time, tzinfo=pytz.timezone(tz_name))

def login_insta(username="not_defined", password="not_defined"):
    L = instaloader.Instaloader()
    if username != "not_defined":
        if password == "not_defined":
            L.interactive_login(username)
        else:
            L.login(username, password)
    if debug_mode:
        debug(msg="The user '{}' is logged in.".format(username))
    return L

def fetch_post(L, post_id):
    debug(msg="Fetching the post id '{}'".format(post_id))
    post = instaloader.Post.from_shortcode(L.context, post_id)
    return post

def get_followers_count(L, profile_name):
    # debug(msg="Fetching the number of followers of the user '{}'".format(profile_name))
    profile = instaloader.Profile.from_username(L.context, profile_name)
    return profile.followers

def get_followers_list(L, profile_name):
    debug(msg="Fetching the follower list of the user '{}'".format(profile_name))
    followers_list = []
    profile = instaloader.Profile.from_username(L.context, profile_name)
    followers = profile.get_followers()
    for follower in followers:
        followers_list.append(follower.username)
    return followers_list

def get_followers_list_from_file():
    with open("{}-followers-list.csv".format(profile_name)) as f:
        followers_list = f.read().splitlines()
    return followers_list

def save_followers_list(followers_list):
    with open("{}-followers-list.csv".format(profile_name), 'w') as f:
        for follower in followers_list:
            f.write("%s\n" % follower)

def get_likes_list(post):
    debug(msg="Listing the users clicked LIKE for the post")
    likes_list = []
    likes = post.get_likes()
    for like in likes:
        likes_list.append(like.username)
    return likes_list

def process_comments(post, deadline, tz_name):
    debug(msg="Proccessing the comments of the post")
    commenter = {}
    comments = post.get_comments()
    for comment in comments:
        comment_owner = comment.owner.username
        comment_date = utc_to_custom_tz(comment.created_at_utc, tz_name)
        comment_text = comment.text
        if comment_owner not in list(commenter.keys()):
            commenter[comment_owner] = Commenter(comment_owner, min_tags)
        commenter[comment_owner].process_tags(comment_text, comment_date, deadline)
    return commenter

def verify_likers(commenters_list,liker_list):
    for commenter, object in commenters_list.items():
        if commenter not in liker_list:
            object.valid = False
            object.is_liker = False

def verify_followers(commenters_list,followers_list):
    for commenter, object in commenters_list.items():
        if commenter not in followers_list:
            object.valid = False
            object.is_follower = False

def list_invalid_commenters(commenters_list):
    invalid_count = 1
    print("*** List of invalid users ***")
    for commenter, object in commenters_list.items():
        if not object.valid:
            print("{}. User '{}' :".format(invalid_count, commenter))
            if (object.invalid_date != 'N/A'):
                print("  - Comment after the deadline (on {})".format(object.invalid_date))
            if (not object.is_liker):
                print("  - NOT pressed the LIKE button")
            if (not object.is_follower):
                print("  - NOT following the profile {}".format(profile_name))
            if (not object.has_min_tags):
                print("  - Not sufficient tags (tagged {} users < min tags {})".format(object.tags_count, object.min_tags))
            invalid_count += 1

def list_valid_commenters(L, commenters_list):
    valid_count = 1
    print("*** List of valid users ***")
    for commenter, object in commenters_list.items():
        if object.valid:
            print("{}. User '{}' tagged {} users:".format(valid_count, commenter, object.tags_count))
            # for id in object.tags_ids:
            #     print("  # {}".format(id))
            #     print("  # {} - {} followers".format(id, get_followers_count(L, id[1:])))
            valid_count += 1

def init_candidates(commenters_list):
    candidates_list = []
    tags_count_list = []
    weights_list = []
    for commenter, object in commenters_list.items():
        if object.valid:
            if commenter not in exclude_list:
                candidates_list.append(commenter)
                tags_count_list.append(int(object.tags_count))
            else:
                debug('d',"User '{}' skipped due to exclude_list".format(commenter))
    tags_sum = sum(tags_count_list)
    for tags_count in tags_count_list:
        weights_list.append(tags_count/tags_sum)
    return candidates_list, weights_list, tags_count_list

def init_text():
    print(init_text_1)
    input("->  Press Enter to start the program and randomly select the winner(s)! READY ?????")
    print(init_text_2)

def winner_picker(candidates_list, weights_list, tags_count_list, total_winner):

    if weighted_list_enable:
        winners_list = random.choices(candidates_list, weights=weights_list, k=total_winner)
    else:
        winners_list = random.choices(candidates_list, weights=None, k=total_winner)

    for winner_cnt, winner in enumerate(winners_list):
        winner_count = winner_cnt + 1
        index = candidates_list.index(winner)
        winner_tags_count = 0
        if tags_count_list:
            winner_tags_count = tags_count_list[index]
        if not debug_mode:
            print("\n\n\n\n\n")
            print("  THE ----------  {}  ---------- WINNER  ".format(winner_count).center(100,"="))
            time.sleep(5)
            print(str(winner_count)*100)
            print("*"*100)
            print("*"*100)
            print("||||||||||  {}  ||||||||||".format(winner).center(100,"*"))
            print("*"*100)
            if min_tags == 0 or not weighted_list_enable:
                print("*"*100)
            else:
                print("((((( Tagged {} Persons )))))".format(winner_tags_count).center(100,"*"))
            print(str(winner_count)*100)
        else:
            debug('i', "Winner {} is '{}' with {} number of tags.".format(winner_count, winner, winner_tags_count))

    if not debug_mode:
        time.sleep(5)
        print("\n\n\n\n\n")
        print("  CONGRATULATIONS  ".center(100,"*"))
        print("\n\n\n\n\n")
        print("- This service is provided by =====>  YEGANEDIA  <=====")
        print("- For more information please visit:  www.yeganedia.com")
        print("-------------------------------------------------------")


def main():
    tz_name = tz_dict[tz_country]
    deadline = set_deadline(deadline_dict, tz_name)

    ### Login to instagram with only username (and interactive password) or
    ### username/password or anonymous
    # login = login_insta(username, password)
    login = login_insta(username)

    ### Use this option to first fetch the list of the followers in a file,
    ### then execute the program to pick the winner!
    ### when the number of followers are high, it avoids lenghty execution.
    # followers_list = get_followers_list(login, profile_name)
    # save_followers_list(followers_list)

    if not debug_mode:
        init_text()

    post = fetch_post(login, post_id)

    commenters_list = process_comments(post, deadline, tz_name)
    if condition_is_follower:
        # followers_list = get_followers_list(login, profile_name)
        followers_list = get_followers_list_from_file()
        verify_followers(commenters_list,followers_list)

    if condition_liked_post:
        liker_list = get_likes_list(post)
        verify_likers(commenters_list,liker_list)

    if condition_only_likes:
        winner_picker(liker_list, weights_list=None, tags_count_list=[], total_winner=total_winner)
    else:
        candidates_list, weights_list, tags_count_list = init_candidates(commenters_list)
        winner_picker(candidates_list, weights_list, tags_count_list, total_winner)

    # list_invalid_commenters(commenters_list)
    #
    # list_valid_commenters(login, commenters_list)

if __name__ == "__main__":
    main()

### EOF

#!/usr/bin/env python3

import instaloader
import pytz, datetime, time
import random

from config import *
from text_vars import *

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
        self.min_tags = min_tags
        self.date = 'N/A'
        self.valid = False
    def process_tags(self, text, comment_date, deadline):
        for item in text.split():
            if item.startswith('@'):
                if item not in self.tags_ids:
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
            L.login(username, tmp_pass)
    return L

def fetch_post(L, post_id):
    post = instaloader.Post.from_shortcode(L.context, post_id)
    return post

def get_followers_list(L, profile_name):
    followers_list = []
    profile = instaloader.Profile.from_username(L.context, profile_name)
    for follower in profile.get_followers():
        followers_list.append(follower.username)
    return followers_list

def get_likes_list(post):
    likes_list = []
    for like in post.get_likes():
        likes_list.append(like.username)
    return likes_list

def process_comments(post, deadline, tz_name):
    commenter = {}
    for comment in post.get_comments():
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
    for commenter, object in commenters_list.items():
        if not object.valid:
            print("The comment of user {} is not valid, because:".format(commenter))
            if (object.invalid_date != 'N/A'):
                print("- The comment was entered on {} after the deadline.".format(object.invalid_date))
            if (not object.is_liker):
                print("- The user has not pressed the like button")
            if (not object.is_follower):
                print("- The user has not followed the profile {}".format(profile_name))

def init_text():
    print(init_text_1)
    input("->  Press Enter to start the program and randomly select the winner(s)! READY ?????")
    print(init_text_2)

def winner_picker(commenters_list, total_winner):
    winner_count = 1
    while winner_count <= total_winner:
        winner = random.choice(list(commenters_list.keys()))
        if not commenters_list[winner].valid:
            print("\n\n\n\n\n->  The selected winner is NOT qualified. NEXT CHANCE...")
            pass
        else:
            print("\n\n\n\n\n")
            print("  THE ----------  {}  ---------- WINNER  ".format(winner_count).center(100,"="))
            time.sleep(5)
            print(str(winner_count)*100)
            print("*"*100)
            print("*"*100)
            print("||||||||||  {}  ||||||||||".format(winner).center(100,"*"))
            print("*"*100)
            print("*"*100)
            print(str(winner_count)*100)
            winner_count += 1
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
    login = login_insta(username)

    init_text()

    post = fetch_post(login, post_id)

    followers_list = get_followers_list(login, profile_name)

    liker_list = get_likes_list(post)

    commenters_list = process_comments(post, deadline, tz_name)

    verify_likers(commenters_list,liker_list)

    verify_followers(commenters_list,followers_list)

    winner_picker(commenters_list, total_winner)

    # list_invalid_commenters(commenters_list)

if __name__ == "__main__":
    main()

### EOF

import urllib

import requests
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from model import *

# api_response = requests.get('https://jsonbin.io/b/59d0f30408be13271f7df29c').json()

# MY API TOKEN KEY
APP_ACCESS_TOKEN = '1637909013.94f874b.be94d57a755c4bc5af32ab2884718c14'

# Token Owner : amarjeetkashyap2
# Sandbox Users : bansal.divam

BASE_URL = 'https://api.instagram.com/v1/'

'''
# Function declaration to get your own info                                  
'''


def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get ( request_url ).json ()

    # DECLARED CONSTRAINTS
    if user_info[ 'meta' ][ 'code' ] == 200:
        if len ( user_info[ 'data' ] ) > 0:
            print 'Username: %s' % (user_info[ 'data' ][ 'username' ])
            print 'No. of followers: %s' % (user_info[ 'data' ][ 'counts' ][ 'followed_by' ])
            print 'No. of people you are following: %s' % (user_info[ 'data' ][ 'counts' ][ 'follows' ])
            print 'No. of posts: %s' % (user_info[ 'data' ][ 'counts' ][ 'media' ])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the ID of a user by username
'''


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get ( request_url ).json ()

    if user_info[ 'meta' ][ 'code' ] == 200:
        if len ( user_info[ 'data' ] ) > 0:
            return user_info[ 'data' ][ 0 ][ 'id' ]
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit ()


'''
Function declaration to get the info of a user by username
'''


def get_user_info(insta_username):
    user_id = get_user_id ( insta_username )
    if user_id == None:
        print 'User does not exist!'
        exit ()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get ( request_url ).json ()

    if user_info[ 'meta' ][ 'code' ] == 200:
        if len ( user_info[ 'data' ] ) > 0:
            a = user_info[ 'data' ][ 'username' ]
            b = user_info[ 'data' ][ 'counts' ][ 'followed-by' ]
            c = user_info[ 'data' ][ 'counts' ][ 'follows' ]
            d = user_info[ 'data' ][ 'counts' ][ 'media' ]
            print 'Username: %s' % (a)
            print 'No. of followers: %s' % (b)
            print 'No. of people you are following: %s' % (c)
            print 'No. of posts: %s' % (d)
            new_user = User ( user_id=user_id, username=a, full_name="full_name", follows_count=c, followed_by_count=b )
            new_user.save ()
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get your recent post
'''


def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get ( request_url ).json ()

    if own_media[ 'meta' ][ 'code' ] == 200:
        if len ( own_media[ 'data' ] ) > 0:
            image_name = own_media[ 'data' ][ 0 ][ 'id' ] + '.jpeg'
            image_url = own_media[ 'data' ][ 0 ][ 'images' ][ 'standard_resolution' ][ 'url' ]
            urllib.urlretrieve ( image_url, image_name )
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the recent post of a user by username
'''


def get_user_post(insta_username):
    user_id = get_user_id ( insta_username )
    if user_id == None:
        print 'User does not exist!'
        exit ()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get ( request_url ).json ()
    media_id = user_media[ 'data' ][ 0 ][ 'id' ]

    if user_media[ 'meta' ][ 'code' ] == 200:
        if len ( user_media[ 'data' ] ) > 0:
            image_name = user_media[ 'data' ][ 0 ][ 'id' ] + '.jpeg'
            image_url = user_media[ 'data' ][ 0 ][ 'images' ][ 'standard_resolution' ][ 'url' ]
            urllib.urlretrieve ( image_url, image_name )
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function declaration to get the ID of the recent post of a user by username
'''


def get_post_id(insta_username):
    user_id = get_user_id ( insta_username )
    if user_id == None:
        print 'User does not exist!'
        exit ()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get ( request_url ).json ()

    if user_media[ 'meta' ][ 'code' ] == 200:
        if len ( user_media[ 'data' ] ) > 0:
            return user_media[ 'data' ][ 0 ][ 'id' ]
        else:
            print 'There is no recent post of the user!'
            exit ()
    else:
        print 'Status code other than 200 received!'
        exit ()


'''
Function declaration to like the recent post of a user
'''


def like_a_post(insta_username):
    media_id = get_post_id ( insta_username )
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post ( request_url, payload ).json ()
    if post_a_like[ 'meta' ][ 'code' ] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'


'''
Function declaration to make a comment on the recent post of the user
'''


def post_a_comment(insta_username):
    media_id = get_post_id ( insta_username )
    comment_text = raw_input ( "Your comment: " )
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post ( request_url, payload ).json ()

    if make_comment[ 'meta' ][ 'code' ] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


'''
Function declaration to make delete negative comments from the recent post
'''


def delete_negative_comment(insta_username):
    media_id = get_post_id ( insta_username )
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get ( request_url ).json ()

    if comment_info[ 'meta' ][ 'code' ] == 200:
        if len ( comment_info[ 'data' ] ):
            # code to delete a comment
            for x in range ( 0, len ( comment_info[ 'data' ] ) ):
                comment_id = comment_info[ 'data' ][ x ][ 'id' ]
                comment_text = comment_info[ 'data' ][ x ][ 'text' ]
                blob = TextBlob ( comment_text, analyzer=NaiveBayesAnalyzer () )
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (
                        media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete ( delete_url ).json ()

                    if delete_info[ 'meta' ][ 'code' ] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'


# PRINTING STATEMENT OF WHAT USER WANT(kripya small letter hi choose kare)
def start_bot():
    while True:
        print '\n'
        print 'Hey! .......Welcome to InstaBot....... (BOLE TOH AAPKA SWAGAT HAI)!'
        print 'Here are your menu options:'
        print "a.Get your own details\n"
        print "b.Get details of a user by username\n"
        print "c.Get your own recent post\n"
        print "d.Get the recent post of a user by username\n"
        print "e.Get a list of people who have liked the recent post of a user\n"
        print "f.Like the recent post of a user\n"
        print "g.Get a list of comments on the recent post of a user\n"
        print "h.Make a comment on the recent post of a user\n"
        print "i.Delete negative comments from the recent post of a user\n"
        print "j.get user details to database\n"
        print "k.get media to database\n"
        print "l.get user comments to database\n"
        print "m.Exit"  # CASES OF VARIOUS COMMANDS

        choice = raw_input ( "Enter you choice: " )
        if choice == "a":
            self_info ()
        elif choice == "b":
            insta_username = raw_input ( "Enter the username of the user: " )
            get_user_info ( insta_username )
        elif choice == "c":
            get_own_post ()
        elif choice == "d":
            insta_username = raw_input ( "Enter the username of the user: " )
            get_user_post ( insta_username )
        elif choice == "e":
            insta_username = raw_input ( "Enter the username of the user: " )
            get_post_id ( insta_username )
        elif choice == "f":
            insta_username = raw_input ( "Enter the username of the user: " )
            like_a_post ( insta_username )
        elif choice == "g":
            insta_username = raw_input ( "Enter the username of the user: " )
            get_post_id ( insta_username )
        elif choice == "h":
            insta_username = raw_input ( "Enter the username of the user: " )
            post_a_comment ( insta_username )
        elif choice == "i":
            insta_username = raw_input ( "Enter the username of the user: " )
            delete_negative_comment ( insta_username )
        elif choice == "j":
            insta_username = raw_input ( "Enter the username of the user: " )
            add_user_id ( insta_username )
        elif choice == "k":
            insta_username = raw_input ( "Enter the username of the user: " )
            add_user_details ( insta_username )
        elif choice == "l":
             add_comments ( insta_username )
        elif choice == "m":
            exit_bot ()
        else:
            print "wrong choice"  # LAUNCHING OF  ".................MY INSTABOT............." :-)


initialize_db ()


def add_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get ( request_url ).json ()

    if user_info[ 'meta' ][ 'code' ] == 200:
        if len ( user_info[ 'data' ] ):
            return user_info[ 'data' ][ 0 ][ 'id' ]
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit ()


    #


def add_user_details(insta_username, followed=None):
    user_id = get_user_id ( insta_username )
    request_url = (BASE_URL + 'users/%s/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    response = requests.get ( request_url ).json ()

    if response[ 'meta' ][ 'code' ] == 200:
        username = response[ 'data' ][ 'username' ]
        full_name = response[ 'data' ][ 'full_name' ]
        follows = response[ 'data' ][ 'counts' ][ 'follows' ]
        followed_by_count = response[ 'data' ][ 'counts' ][ 'followed_by_count' ]

        query = User.select ().where ( User.user_id == user_id )
        if len ( query ) > 0:
            query[ 0 ].username = username
            query[ 0 ].full_name = full_name
            query[ 0 ].follows_count = follows
            query[ 0 ].followed_by_count = followed_by_count
            query[ 0 ].save ()

        else:
            new_user = User ( user_id=user_id, username=username, full_name=full_name, follows_count=follows,
                              followed_by_count=followed_by_count )
            new_user.save ()  # Need to Specify force_insert when using manual Primary Keys.

        query = User.select ().where ( User.user_id == user_id )
        print query[ 0 ].username
        print query[ 0 ].followed_by_count
        print query[ 0 ].full_name
        print query[ 0 ].follows_count
        print query[ 0 ].user_id
    else:
        exit ()

    def add_user_post(insta_username):
        user_id = get_user_id ( insta_username )
        if user_id == None:
            request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        response = requests.get ( request_url ).json ()

        if user_media[ 'meta' ][ 'code' ] == 200:
            if len ( user_media[ 'data' ] ) > 0:
                # # if response[ 'meta' ][ 'code' ] == 200:
                # #     media_type = response[ 'data' ][ 'type' ]
                # #     media_link = response[ 'data' ][ 'media_type' ][ 'standard_resolution' ][ 'url' ]
                # #     media_id = response[ 'data' ][ 'id' ]
                # #     user_id = response[ 'data' ][ 'id' ]
                for data_items in user_media[ 'data' ]:
                    media_id = response[ 'data_item' ][ 'id' ]
                    media_type = response[ 'data_item' ][ 'type' ]

                    media_link = [ 'data_item' ][ 'media_type' ][ 'standard_resolution' ][ 'url' ]

                query = Media.select ().where ( Media.media_id == media_id )
                if len ( query ) > 0:
                    query[ 0 ].media_type = media_type
                    query[ 0 ].media_link = media_link
                    query[ 0 ].media_id = media_id
                    query[ 0 ].save ()

                else:

                    new_media = Media ( user_id=user_id, media_id=media_id, media_type=media_type,
                                        media_link=media_link )
                    new_media.save ()
                    query = Media.select ().where ( Media == media_id )
                    print query[ 0 ].media_id
                    print query[ 0 ].media_type
                    print query[ 0 ].media_link
                    print query[ 0 ].user_id

        # return user_media['data'][0]['id']
        else:
            print 'Post does not exist!'


        # else:
        #     print 'Status code other than 200 received!'


def add_comments(insta_username):
    user_id = get_user_id ( insta_username )
    if user_id == None:
        print 'User does not exist!'
        exit ()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get ( request_url ).json ()
    if user_media[ 'meta' ][ 'code' ] == 200 and len ( user_media[ 'data' ] ) > 0:
        for index in range ( len ( user_media[ 'data' ] ) ):

            media_id = user_media[ 'data' ][ index ][ 'id' ]

            comment_request = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
            print 'GET request url : %s' % (comment_request)
            response = requests.get ( comment_request ).json ()

            if response[ 'meta' ][ 'code' ] == 200:
                for index in range ( len ( response[ 'data' ] ) ):
                    for data_item in user_media[ 'data' ]:
                        media_id = data_item[ 'id' ]
                        comment_id = data_item[ 'id' ]
                        user_id = data_item[ 'id' ]
                        comment_text = data_item[ 'type' ]

                    query = Comment.select ().where ( Comment.comment_id == comment_id )
                    if len ( query ) > 0:
                        query[ 0 ].media_id = media_id
                        query[ 0 ].Comment_id = comment_id
                        query[ 0 ].user_id = user_id
                        query[ 0 ].comment_text = comment_text
                        query[ 0 ].save ()
        else:

            new_Comment = Comment ( user_id=user_id, media_id=media_id, comment_id=comment_id,
                                    comment_text=comment_text )
            new_Comment.save ()
        query = Comment.select ().where ( Comment == comment_id )
        print query[ 0 ].media_id
        print query[ 0 ].Comment_id
        print query[ 0 ].user_id
        print query[ 0 ].comment_text

        return user_Comment[ 'data' ][ 0 ][ 'id' ]
    else:
        print 'Comment does not exist!'


start_bot ()

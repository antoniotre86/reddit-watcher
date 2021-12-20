'''
Created on 18/12/2021

@author: trentaa
'''

import json
import os
from reddit_watcher.reddit_watcher import RedditWatcher
import logging


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Load env variables
    client_id = os.getenv("REDDIT_APP_CLIENT_ID")
    client_secret = os.getenv("REDDIT_APP_SECRET")
    reddit_username = os.getenv("REDDIT_UNAME")
    reddit_password = os.getenv("REDDIT_PW")
    subreddit_terms = json.loads(os.getenv("SUBREDDIT_TERMS_JSON"))
    output_subreddit = os.getenv("OUTPUT_SUBREDDIT")

    # Find submissions
    rw = RedditWatcher(
        client_id,
        client_secret,
        reddit_username,
        reddit_password,
        output_subreddit
    )
    submissions = rw.subreddits_submissions_by_terms(subreddit_terms)
    logger.info(f"{len(submissions)} found.")

    # Find already posted
    existing_submissions = rw.find_existing_submissions(submissions)
    submissions_to_post = list(set(submissions).difference(existing_submissions))
    logger.info(f"{len(existing_submissions)} submissions were already cross-posted.")

    # Crosspost submissions
    posted = rw.post_submissions(submissions_to_post)
    logger.info(f"Cross-posted {len(posted)} submissions on r/{rw.output_subreddit}.")

    msg = f'{len(posted)} posts found.'
    return {
        'statusCode': 200,
        'body': json.dumps(msg)
    }

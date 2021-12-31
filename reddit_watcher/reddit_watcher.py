'''
Created on 18/12/2021

@author: trentaa
'''
import re
import praw
import time


class RedditWatcher(object):

    version = "0.0"

    def __init__(self, client_id, secret, reddit_username, reddit_password, output_subreddit):
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=secret,
            user_agent=f'python:{reddit_username}:{self.version} (by u/{reddit_username})',
            username=reddit_username,
            password=reddit_password,
        )
        self.output_subreddit = output_subreddit

    def subreddit_submissions_by_terms(self, subreddit, terms):
        submissions = []

        subreddit = self.reddit.subreddit(subreddit)
        for submission in subreddit.new():
            if submission.created_utc < time.time() - 24*3600:
                continue
            there = False
            term_found = []
            for term in terms:
                title = submission.title.lower()
                if re.search(term, title):
                    there = True
                    term_found.append(term)
            if there:
                submissions.append(submission)

        return submissions

    def subreddits_submissions_by_terms(self, subreddit_terms):
        """

        :param subreddit_terms: format `[{'subreddit': <subreddit>, 'terms': (<term1>, <term2>, ...)}, ...]`
        :return:
        """
        submissions = []
        for st in subreddit_terms:
            submissions_ = self.subreddit_submissions_by_terms(st["subreddit"], st["terms"])
            submissions += submissions_
        return submissions

    def post_submission(self, submission):
        return submission.crosspost(self.output_subreddit)

    def post_submissions(self, submissions):
        posts = []
        for submission in submissions:
            post = self.post_submission(submission)
            posts.append(post)
        return posts

    def _get_existing(self):
        subreddit = self.reddit.subreddit(self.output_subreddit)
        return [s for s in subreddit.new()]

    def _get_parents(self, submissions):
        return [self.reddit.submission(id=s.crosspost_parent.split("_")[-1]) for s in submissions]

    def find_existing_submissions(self, submissions):
        output_subreddit_submissions = self._get_existing()
        output_subreddit_submissions_parents = self._get_parents(output_subreddit_submissions)
        existing_submissions = list(set(submissions).intersection(output_subreddit_submissions_parents))
        return existing_submissions

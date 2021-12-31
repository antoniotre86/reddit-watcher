# Reddit Watcher Bot

Reddit bot that runs on AWS Lambda and scans recent submission titles for given terms or regexes. 
The submissions it finds are then cross-posted to a separate subreddit. 

## Requirements
* Python 3.8
* praw https://praw.readthedocs.io
* AWS account

## Installation

Clone the repository to your local machine
```
git clone git@github.com:antoniotre86/reddit-watcher.git
```

Navigate into the repo root directory and run the deployment script; this downloads the required dependencies and packages the code into a zip file, ready to be uploaded to a new Lambda function
```
cd reddit-watcher

chmod +x deploy.sh

./deploy.sh
```

Create a new [AWS Lambda function](https://docs.aws.amazon.com/lambda/?id=docs_gateway) and upload the "deployment-package.zip" file created in the previous step, which can be found in the root directory.

On Reddit:
1. make a new account for your bot
2. register a new script application https://www.reddit.com/prefs/apps
3. note down the "client ID" (under "personal use script") and "secret"
4. create a new subreddit where you want the relevant posts to be cross-posted (you need to be admin of this subreddit)

Configure the Lambda function
1. On your Lambda function main page, go to the tab "Configuration" and then "Environment variables"
2. Add the following environment variables (key: value)
   1. OUTPUT_SUBREDDIT: name of the subreddit you have created where you want the posts to be cross-posted
   2. REDDIT_APP_CLIENT_ID: your reddit application client ID
   3. REDDIT_APP_SECRET: your reddit application secret
   4. REDDIT_UNAME: your reddit bot user name
   5. REDDIT_PW: your reddit bot user password
   6. SUBREDDIT_TERMS_JSON: search query in json format, as follows `[{"subreddit": <subreddit name 1>, "terms":[<term 1>, <term 2>, ...]}, {"subreddit": <subreddit name 2>, "terms":[<term 1>, <term 2>, ...]}, ... ]` (terms can be also regex strings -- see example below)	

Search query example:
```
[{"subreddit":"europe", "terms":["italy", "covid", "uk\b"]},{"subreddit":"italy", "terms":["covid", "macron"]}]
```

You can then run the Lambda function manually on the "Test" tab, or you can set up Event Bridge to run your Lambda on a schedule: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-run-lambda-schedule.html

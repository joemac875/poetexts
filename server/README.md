# Poem Web Service

A Flask application that parses poems stored as XML files and serves poems to users.

## Usage

`http://yourhostname/`

Returns the available tags and accepted tag values that can be used to make requests

`http://yourhostname/poem`

Returns the JSON for a random poem from all poems

`yourhostname/poem?tag1=something&tag2=somethingelse`

Returns the JSON for a random poem matching some or all of the tags

`http://yourhostname/issues`

Shows all the XML files with problems


# Deploying

## Local

The server can be tested locally.

First, install a virtual environment on your machine.

`python3 -m venv /path/to/new/virtual/environment`

Then, activate your virtual environment (command might be different for different shells)

`source /path/to/new/virtual/environment/bin/activate`

Now, install all of the required libraries

`pip install -r requirements.txt`

You should now be able to run the server locally using

`python application.py`

## Elastic Beanstalk

The application can be easily deployed using the AWS EB command line interface.

First install the [EB Command Line Interface](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)

Now, in the directory containing the Flask app (`application.py`) run

`eb init`

This will set up a hidden `elasticbeanstalk` folder containing all of the information needed to deploy the app. Next, run

`eb create`

This creates an EB environment to house your application in and deploys the app (it will prompt you for a few things,
but the default values should suffice).

**From now on**, if you make changes to the server, like adding tags, changing tags, adding poems, or changing poems, just use

`eb deploy`

to push them to the web service.

# Changing Tags and Tag Values

Open up `application.py` using your favorite editor. Find

```python
application.config.update(dict(
    XML_PATH='poems/', # the directory containing the XML files
    XML_NAMESPACE='http://www.tei-c.org/ns/1.0', # the namespace used in the XML files
    csv='poems.csv',
    ERROR='errors.txt',
    # analysis tags are used to set bounds on the types of analysis that can be picked from and the
    # range of values for each tag that can be added
    analysis_tags={'form': ['sonnet', 'free','haiku'], 'tone': ['happy', 'sad','indifferent'], \
                   'topic': ['love', 'war','environment','education','history'],\
                   'figurative': ['yes', 'no']}
))
```

The `analysis_tags` here is a Python dictionary containing key value pairs. The keys are the analysis tags. The values
attached are lists of accepted strings for these tags. Just change this dictionary to make changes to the analysis tags
the server looks for while parsing and will serve to clients.







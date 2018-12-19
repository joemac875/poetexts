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






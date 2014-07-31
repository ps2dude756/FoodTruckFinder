Project
=======

I chose the project Food Trucks because it seemed both interesting and 
practical, and would cause me to learn some interesting new frameworks.

Technical Track
===============
I chose the Back-end track because I have very little experience with 
front-end technologies such as JavaScript.

Technical Choices
=================

Back-end
--------
I chose Python as the back-end language because it is my preferred language 
and the language most of Uber's back-end code is written in. I then decided to use
Flask for the web framework because some of my colleagues have recommended it
in the past, and I have read that since it is smaller and more minimalistic than
other frameworks such as Django, it works better for creating REST apis.
While I have used Python in the past, I had never used Flask before, nor had I
done any web coding in Python. Because of this, one of my early tasks for this
project was to read large sections of the documentation on the Flask website,
detailed in Issue #1.

Front-end
---------
Because I chose the back-end track, I focused very little on the front-end code, 
writing a front-end mostly to act as a proof of concept. As a result of this,
the front-end is written in HTML and a small amount of Javascript, using no
frameworks or CSS. The one significant activity the front-end code does preform
is converting the address provided by the user into latitude and longitude to 
pass to the back-end. To do this I chose to use Google's Maps API, because this
would allow for further extension of the front-end using Maps. While Google provides
and HTTP endpoint for their geocoding service, they recommend using the JavaScript
client for any real-time geocoding.

Hosting
-------
I chose to use Heroku to host the project, because I had heard using Heroku was
very simple and straight-foward. Additionally, Heroku has an article detailing
deploying up a Flask app on their site. I had never used Heroku before this 
project.

Trade-offs
==========
If given more time to work on the project, there are several changes I'd like to make.
The largest change I'd make is to spend time learning JavaScript and CSS so I could 
make a proper front-end and choose the Full Stack track over the Back-End track. I'd
have liked to display a map on the page as opposed to a table, with markers for the 
returned restaurants and the user's location.
For smaller changes, I'd have liked to include a basic admin page that can be logged into
to manually add or remove foodtrucks from, exposing more API endpoints as appropriate. 
Additionally, there were some foodtrucks on [DataSF: Food Trucks](https://data.sfgov.org/Permitting/Mobile-Food-Facility-Permit/rqzj-sfat)
that did not have latitude and longitude coordinates, so I was unable to add 
them to the database. I'd like to have included a function to geocode them using
Google's HTTP Maps API at index-time.
Finally, I would have researched Heroku more before starting this project. I 
was unaware that Heroku only supports Postgresql, and additionally that it does 
not support PL/Python. Had I known this, I would not have spent time developing 
my code to work with sqlite, and would have developed for Postgresql without 
PL/Python from the beginning.

Link to other code
==================
Here is a link to [RikkaBot](https://github.com/ps2dude756/RikkaBot), an ongoing
project I've been working on over the last month.

Link to resume
==============
Here is a link to my [resume](https://www.dropbox.com/s/vib7s3qd2uue8pe/resume.pdf)
Here is a link to my [LinkedIn profile](https://www.linkedin.com/pub/andrew-roth/58/293/3a9)

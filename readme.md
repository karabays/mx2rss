
# mx2rss

Read your newsletters with RSS. Inspired by [Kill-the-newsletter!](https://kill-the-newsletter.com/) website. 
It's also self-hostable but requires also to maintain your own mail server.

You need MXRoute account for this to work. Program uses DirectAdmin api to create email 
forwarders. I have no ability to test it but in theory it should work with other email 
service providers using DirectAdmin.


## Installation 

### Repository

Clone the repo, install the `requirements.txt`

    pip install -r requirements.txt

Go to `app` folder

    cd app

a) and run the `main.py` file

    python3 main.py

Or b) run with gunicorn in daemon mode:

    gunicorn main:app --bind 0.0.0.0:9123 -k 'uvicorn.workers.UvicornWorker' --daemon

### Docker

Once I figure out how to do it, I will tell you.


    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`SITE_URL`  The url you want the site to be accessed. http://192.168.1.1:9123

`EMAIL_DOMAIN`  email domain you manage with MXroute

`DAPANEL_URL`   

`DAPANEL_USER`

`DAPANEL_PASS`

`INBOX_URL`  IMAP server

`INBOX` Mail address to collect all newsletters in the backgroun

`INBOX_PASS`

`FETCH_FREQUENCY` how oftern you want to check for mail (in seconds)



  

  
## Acknowledgements

Developed with FastApi, lots of googling and ductape. As the code manifests, I am just an hoppyist.
If you find a bug or something, let me know I may or may not fix it...

## Related

Here are some related projects.

https://github.com/leafac/kill-the-newsletter

[FreshRSS](https://freshrss.org/) is the RSS reader I am using for everyting.

I also heavily used these resources:

https://fastapi.tiangolo.com/

https://fastapi-utils.davidmontague.xyz/user-guide/repeated-tasks/

https://pydantic-docs.helpmanual.io/






  
## License

[MIT](https://choosealicense.com/licenses/mit/)

  

# mx2rss

Read your newsletters with RSS. Inspired by [Kill-the-newsletter!](https://kill-the-newsletter.com/) website. 
Which is also self-hostable but requires to maintain your own mail server. So here is a solution for the lazy.

You need [MXRoute](https://mxroute.com/) account for this to work.
Program uses DirectAdmin api to create email forwarders. 
I have no ability to test it but in theory it should work with other email service providers using DirectAdmin.

I wouldn't trust myself to expose this website to the internet. My suggestion is to run this in your local network
and use it with a self hosted RSS reader like freshrss.


## Installation 

### Repository

Clone the repo, install the `requirements.txt`

    pip install -r requirements.txt


Run the `start.sh` file.

### Docker

Once I figure out how to do it, I will tell you.

## Update

Pull the repository again and run the start script. It will restart the uvicorn if there is already a running process.

    git pull
    bash start.sh
    
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

https://www.directadmin.com/api.php




  
## License

[MIT](https://choosealicense.com/licenses/mit/)

  
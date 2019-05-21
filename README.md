       
# Meta-Music
Meta-Music is an open-source project that lets people add metadata to their Music library using audio recognition system for accurate retrival of data incase of mismatched song names. 


 ***Note: since, this branch uses audio recognition to find correct song names which were mismatched by the API provider. And  the audio recognition system only recognizes songs within the local database, its not ideal for real world use cases.
 Please refer to  [pypi_package](https://github.com/unique1o1/Meta-Music/tree/pypi_package) branch for your use.***
 

# Quickstart
       `
       $ git clone https://github.com/unique1o1/Meta-Music 
       $ cd Meta-Music
       $ sudo pip install -r requirements.txt
       $ python3 app.py
       `
# Database Setup
### Database Configuration 

       $ nano Metamusic/config
       

       
# Using docker

       cd Meta-Music
       docker build -t meta-music:latest . 
       docker run --rm -ti -v /your/local/pathto/Music:/music meta-music:latest
 ## Creating database on docker
       docker run --name postgres-sql -e POSTGRES_PASSWORD=0 -d postgres
       docker exec -ti -u root postgres-sql bash
       psql -U postgres
       create database metamusic
 ## Database table Creation
       $ python3.6
       >>> from Metamusic import database
       >>> database.metadata.create_all()
   
 **Note: do change IP in /static/dist/Worker.js to your docker containers IP**
       
       docker inspect <your container's name> | grep -i 'ipaddress'  //to find your docker container's IP
       


# Fingerprinting

To start filling the database with your music's fingerprints follow the instruction below:
       
       python3.6 metamusic.py -l 10 -f /path/to/your/Music/file/or/directory
       
# Recognizing from File/ Directory

       python3.6 metamusic.py -l 10 -r file /path/to/your/Music/file

# Recognizing from Microphone

       python3.6 metamusic.py -r mic 10
       
**Note: Recognizing from Microphone doesn't work for docker containers for now**
## Tuning

Inside `Metamusic/fingerprint.py`, you may want to adjust following parameters.

    FINGERPRINT_REDUCTION 
    PEAK_SORT 
    DEFAULT_OVERLAP_RATIO 
    DEFAULT_FAN_VALUE 
    DEFAULT_AMP_MIN 
    PEAK_NEIGHBORHOOD_SIZE 
    
These parameters are described in the `Metamusic/fingerprint.py` in detail. Read that in-order to understand the impact of changing these values.


# Demo

![demo](https://media.giphy.com/media/8PBFETWIZ39tme3vow/giphy.gif)


**Note for MacOS users**: If you experience problems with fork in macOS, put `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` in your environment variable to fix the issue. This is an issue with macOS 10.13 where Apple changed the way fork() works on the OS which is incompatible with Python fork().
 

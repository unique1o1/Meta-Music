       
# Meta-Music
Meta-Music is an open-source project that lets people add metadata to their Music library.


 **Note: This branch is not for your personal use. Please use the [pypi_package](https://github.com/unique1o1/Meta-Music/tree/pypi_package) branch for your use.**
 
# Installation from source:

        cd static
        npm install 
        cd ..
        virtualenv py3
        pip install -r requirements
        python app.py
        npm run watch
# Using PIP
        sudo pip install MetaMusic
        sudo npm install -g random-material-color react react-dom
        meta-music
        # Or
        meta-music /path/to/music.mp3 #absolute path only
# Using docker
       cd Meta-Music
       docker build -t meta-music:latest . 
       docker run --rm -ti -v /your/local/pathto/Music:/music meta-music:latest
       
 **Note: do change IP in /static/dist/Worker.js to your docker containers IP**
       
       docker inspect <your container's name> | grep -i 'ipaddress'  //to find your docker container's IP
       
# Demo

![demo](https://media.giphy.com/media/8PBFETWIZ39tme3vow/giphy.gif)


**Note for MacOS users**: If you experience problems with fork in macOS, put `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` in your environment variable to fix the issue. This is an issue with macOS 10.13 where Apple changed the way fork() works on the OS which is incompatible with Python fork().
 

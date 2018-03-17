       
# Meta-Music
Meta-Music is an open-source project that lets people add metadata to their Music library.

# Using PIP
        sudo pip install MetaMusic
        meta-music
        # Or
        meta-music /path/to/folder or song
# Using source
        
        cd Meta-Music
        git checkout pypi_package 
        python3.6 setup.py install
        meta-music
        # Or
        meta-music /path/to/folder or song
# Demo

![demo](https://media.giphy.com/media/8PBFETWIZ39tme3vow/giphy.gif)


**Note for MacOS users**: If you experience problems with fork in macOS, put `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` in your environment variable to fix the issue. This is an issue with macOS 10.13 where Apple changed the way fork() works on the OS which is incompatible with Python fork().
 
**Note for Windows users**: Also install python-magic-bin using pip i.e `pip install python-magic-bin`. But current the program is not working for windows
       

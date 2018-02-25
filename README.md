# Meta-Music
Meta-Music is an open-source project that lets people add metadata to their Music library.

installation for you guys:

        cd static
        npm install 
        cd ..
        virtualenv py3
        pip install -r requirements
        python app.py
        npm run watch

**Note for MacOS users**: If you experience problems with fork in macOS, put `OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES` in your environment variable to fix the issue. This is an issue with macOS 10.13 where Apple changed the way fork() works on the OS which is incompatible with Python fork().
 
        

## Steps to install node.js and python venv in local machines(including the libraries and dependencies):

1) For Node.js: After cloning your repository, run:
(This will recreate the node_modules/ folder based on your package.json file)

 ```
 npm install
 ```

2) For Python: After cloning, run the following commands:
```
python -m venv venv      # Create a new virtual environment
source venv/bin/activate # Activate the virtual environment (Linux/Mac)
venv\Scripts\activate    # Activate on Windows
pip install -r requirements.txt  # Install the Python dependencies
```
## How to run node.js
After installation run:
```
node server.js
```
Server will be runing in http://localhost:3000 



# IF YOU NEED SNY HELP PLESSE LET ME KNOW
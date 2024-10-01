Steps to install node.js and python venv in local machines(including the libraries):
1) For Node.js: After cloning your repository, run:
- npm install  #(This will recreate the node_modules/ folder based on your package.json file).

2) For Python: After cloning, run the following commands:
python -m venv venv      # Create a new virtual environment
source venv/bin/activate # Activate the virtual environment (Linux/Mac)
venv\Scripts\activate    # Activate on Windows
pip install -r requirements.txt  # Install the Python dependencies
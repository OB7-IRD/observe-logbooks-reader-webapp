# LTO-webapp

Web application for automatically transfer logbooks

## LTO-webapp installation

pip install -r requirements.txt

There might be an issue with the versions asked for numpy and pandas - if so, remove the versions on requirements.txt

install node.js
python manage.py tailwind start

There might be a conflict between flake-8 and pylint. If so, remove pylint

Then add the connexion profiles


## Documentation through Sphinx
pip install pydata-sphinx-theme
sphinx-quickstart docs

pip install mystr_parser
pip install sphinx_design
pip install sphinx_copybutton
pip install sphinx_codeautolink
pip install sphinx-serve

```
To launch the documentation :

```         
cd docs
.\make html # Build the documentation 
sphinx-serve & # Launch the serveur 
sphinx-serve -b build -h 127.0.0.1

if issue : sphinx-build -b html source build
```

# To build the CSS style 

```bash
python3 manage.py tailwind build
```

# To build the auto docstring 

```
cd source
sphinx-apidoc -o api palangre-syc # toward a folder with an __init__ file
```

## To use Django translation
```
django-admin makemessages -a
django-admin compilemessages
```
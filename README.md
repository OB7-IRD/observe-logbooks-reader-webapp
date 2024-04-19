# observe-logbooks-reader-webapp

Application web pour l'interprétation automatisée des livres de bord

## Documentation réalisée avec Sphinx
```
pip install pydata-sphinx-theme
sphinx-quickstart docs

pip install myst_parser
pip install sphinx_design
pip install sphinx_copybutton
pip install sphinx_codeautolink
pip install sphinx-serve

```
Pour lancer la documentation :

```         
cd docs
.\make html # Build the documentation 
sphinx-serve -h 127.0.0.1 # Lance le serveur 

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
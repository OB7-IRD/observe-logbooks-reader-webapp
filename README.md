# observe-logbooks-reader-webapp

Application web pour l'interprétation automatisée des livres de bord

## Documentation réalisée par le biais de MkDocs

Il faut péralablement installer [MkDocs](https://www.mkdocs.org) :

```         
pip install mkdocs
pip install mkdocs-material
pip install mkdocstrings
```

Pour lancer la documentation :

```         
cd website-documentation
mkdocs serve --dev-addr 127.0.0.1:8005
mkdocs -h # Print help message and exit.
```

## Documentation réalisée par le biais de Sphinx
```
pip install pydata-sphinx-theme
sphinx-quickstart docs

pip install mystr_parser
pip install sphinx_design
pip install sphinx_copybutton
pip install sphinx_codeautolink
pip install sphinx-serve

```
Pour lancer la documentation :

```         
cd docs
make html # Build the documentation 
sphinx-serve & # Lance le serveur 
sphinx-serve -b build -h 127.0.0.1
```

# To build the CSS style 

```bash
python3 manage.py tailwind build
```

# To build the auto docstring 

```
cd docs
sphinx-apidoc -o source palangre-syc # toward a folder with __init__ file
```
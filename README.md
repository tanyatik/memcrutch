## Memcrutch

Welcome to Memcrutch! It helps your bad memory with things like programming langugage syntax
and other details of your work you tend to forget, by allowing to search through your notes, fast.

### How to run

First, change the constant in https://github.com/tanyatik/memcrutch/blob/main/local_search.py#L8

To run, do this:

```
# Setting up virtual environment
virtualenv venv
. venv/bin/activate

# Installing dependencies
brew install python-tk
python3 -m pip install tk md2html pillow requests markdown2 pyyaml pygments markdown2 tkhtmlview

# Running app
python3 memcrutch.py
```

### Building a Mac app

```
# Installing dependencies
python3 -m pip install py2app

# Building app
python3 setup.py py2app

# Run the app
./dist/memcrutch.app/Contents/MacOS/memcrutch

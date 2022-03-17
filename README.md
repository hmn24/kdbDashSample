# Dash MES Form Submission

## About this app

This app allows the user to call a kdb process and presents it out in a dash plotly DataTable format

## Reference github

```
https://github.com/plotly/dash-sample-apps/tree/main/apps/dash-mes-form-submission
```

## How to run this app

(The following instructions apply to Posix/bash. Windows users should check
[here](https://docs.python.org/3/library/venv.html).)

First, clone this repository and open a terminal inside the root folder.

Create and activate a new virtual environment (recommended) by running
the following:

```bash
python -m venv myvenv
source myvenv/bin/activate
```

Install the requirements:

```bash
pip install -r requirements.txt
```
Run the app:

```bash
python app.py
```
Open a browser at http://127.0.0.1:8050

Or alternatively:
```
gunicorn app:server -b :8050 -w 4 -c config/gunicorn.cfg.py
```

## Have pre-commit install available
```
pre-commit install
```


## Resources

- To learn more about Dash, check out our [documentation](https://plot.ly/dash).


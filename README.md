## What is Atelier?
Atelier is a simple customer and order management system written
especially with photographers in mind.

It's designed to accommodate the needs of a small company with 4-5
users and has been running practically with no maintenance since May
2008 (exactly six years at the time of writing).

It was originally written in Java but was in 2015 re-written in
Python.

## Can I use it too?

Yes you can. We release the source code as open source under the GPLv3
in the hope that it might be useful for others too, either as a simple
customer & order system or as a show case of an application using
Python and Flask.

See the [COPYING](COPYING) file for more information on licensing.

## What do I need to run it?

You need a Python 2.7 runtime environment a MySQL compatible database,
like [Percona](http://percona.com).

## Upgarde notes

If you're running an older version of the Atelier DB (pre 2015-03-31),
you need to remove the `total_amount` column from the `customer_order`
table and add a new `internet_allowed` column:

```
alter table customer_order drop column total_amount;
alter table customer_order add internet_allowed integer not null;
```

## 3rd party libraries used

- [Flask](http://flask.pocoo.org/) for web development
- [Jinja](http://jinja.pocoo.org/docs/dev/) for templating
- [MySQL for Python](http://sourceforge.net/projects/mysql-python/)
  for DB connectivity
- [Chart.js](https://github.com/nnnick/Chart.js)
  for fancy HTML5 graphs
- [Bootsrap](http://getbootstrap.com/) for nice layout of web pages
- [HTML5](http://www.w3.org/TR/html5/) as GUI platform  :-)
- And last, but not least, [Python](http://python.org) for the
  programming language itself :-)

## Installation notes
- NOT finished

```
# apt-get install python-pip
# apt-egt install python-mysqldb
# pip install flask

```

Ensure you've got a valid `atelier-conf.json` file in the diretory
where you start up atelier:
```
{
    "db": {
        "host": "localhost",
        "user": "atelieruser",
        "password": "foo",
        "db" : "atelierdb"
    },
    "locale": "nb_NO.utf8"
}
```

Download `Chart.js`:
```
$ cd src/main/python/files
$ wget https://raw.githubusercontent.com/nnnick/Chart.js/master/Chart.js
```


Cheers,

-Torstein

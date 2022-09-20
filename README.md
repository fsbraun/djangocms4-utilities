# djangocms4-utilities

Djangocms-4 Utilities bundles little helpers to support debugging of Django CMS 4.

Install djangocms4-utilities directly from github:

    pip install git+https:/github.com/fsbraun/djangocms4-utilities#egg=djangocms4-utilities


Add `djangocms4_utilities` to your `INSTALLED_APPS``

## Management command fixtree

Attention: **Always test this command on a copy of the database first and check
that you do not lose data.**

### Usage

    ./manage.py fixtree

### Effect

`fixtree` takes all placeholders of draft pages and rebuilds their plugin tree.
This is helpful if you encounter an 
[issue (#7391) with moving plugins](https://github.com/django-cms/django-cms/issues/7391).

The rebuilt tree will have the following properties:

1. All plugins will be assigned to the same placeholder. (Sometimes caused by )
   [issue #7392](https://github.com/django-cms/django-cms/issues/7392).
2. All child plugins will have a position behind their respective parents. 
3. All descendants of a plugin (children and grandchildren) will have consecutive positions
   immediately following the parent.

## Middleware to watch for plugin tree consistency


Add `djangocms4_utilities.middleware.plugin_tree.watch` to your `MIDDLEWARE` settings to
use the watch middleware to warn you over the console output if `fix_tree` sees inconsistencies 
in plugin trees.

Do avoid too much overhead for each request set

    WATCH_PLACEHOLDER = id
    
or

    WATCH_PLACEHOLDER = [id1, id2, id3]

in your `settings.py`.

# djangocms4-utilities

Djangocms-4 Utilities bundles little helpers to support debugging of Django CMS 4.

Install djangocms4-utilities directly from github:

    pip install git+https:/github.com/fsbraun/djangocms4-utilities#egg=djangocms4-utilities


## Middleware to watch for plugin tree consistency


Add `djangocms4_utilities.middleware.plugin_tree.watch` to your `MIDDLEWARE` settings to
use the watch middleware to warn you over the console output if `fix_tree` sees inconsistencies 
in plugin trees.

Do avoid too much overhead for each request set

    WATCH_PLACEHOLDER = id
    
or

    WATCH_PLACEHOLDER = [id1, id2, id3]

in your `settings.py`.

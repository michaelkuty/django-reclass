
========================
Django Service Templates
========================

Manage your service templates via Django Admin. Store, render and then transform or push to engine.

.. contents::
    :local:

Installation
------------

.. code-block:: bash

    pip install django-reclass

It's standard django app run it standalone or include it where you want. It works great with Leonardo CMS.


Import your reclass::

    python manage.py import_reclass --name=reclass -p /path/to/your/reclass/
    Successfully collected 11090 paths for import.
    Successfully imported 90 nodes and 11000 classes


Test your api::

    majklk@samsung:~⟫ http 10.10.10.166/reclass/.leonardo-multi.webapp.dev.mjk.robotice.cz

    {
        "context": null, 
        "extra": null, 
        "id": 6807, 
        "label": ".leonardo-multi.webapp.dev.mjk.robotice.cz", 
        "modified": null, 
        "path": "/home/majklk/reclass9/nodes/_generated/leonardo-multi.webapp.dev.mjk.robotice.cz.yml", 
        "polymorphic_ctype": 202, 
        "rendered": "{'classes': ['system.linux.system.virtualbox', 'system.leonardo.server.multi', 'system.leonardo.server.app.steakhousepisek'], 'parameters': {'_param': {'salt_master_host': '10.10.10.1'}, 'linux': {'system': {'domain': 'webapp.dev.mjk.robotice.cz', 'name': 'leonardo-multi'}}}}", 
        "sync": null, 
        "template": 4453, 
        "user": null
    }



Read More
=========

* https://www.majklk.cz/howto/salt-reclass-remote/
* https://github.com/django-leonardo/django-leonardo

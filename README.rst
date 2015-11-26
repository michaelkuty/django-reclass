
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

Snippet for server side API::

    from flask import jsonify
    from flask import Flask
    from flask import request
    import yaml

    app = Flask(__name__)


    @app.route("/<path:path>", methods=['POST'])
    def dump_relass(path):
        print path
        reclass = yaml.load(request.data)
        print reclass
        stream = file('/' + path, 'w')
        yaml.dump(reclass, stream)
        stream.close()
        return jsonify({"result": "Success! See /%s" % path})

    if __name__ == "__main__":
        app.debug = True
        app.run(host="0.0.0.0")

Warning: Never use this snippet in production !


Read More
=========

* https://github.com/django-leonardo/django-leonardo

sphinx-json-schema
==================

A JSON Schema renderer for Sphinx_

Installation
------------


As simple as it can be with ``pip``::

   pip install sphinx-json-schema


Usage
-----

Add the extension name to your ``conf.py``::

   extensions = [
      ...
      'sphinx_json_schema',
      ...
   ]

If necessary, add a root directory to look for json schemas::

   json_schema_root_dir = os.path.join('path', 'to', 'root', 'dir')

In your documentation::

   .. json_schema:: path/to/json/schema.json

The file is looked up relatively from the ``.rst`` file the directive is called in, or, if not
found from the ``json_schema_root_dir`` specified in the ``conf.py`` file.

allOf, oneOf, anyOf, not support
--------------------------------

``sphinx_json_schema`` supports the ``allOf``, ``oneOf``, ``anyOf`` and ``not`` keywords. It can
also parse references to other schemas. The final JSON output is the result of the operations and
inclusions of other schemas. This means it can be quite long even if the original ``.json`` file
is very short!

.. warning::

   This is still experimental


.. _Sphinx: http://www.sphinx-doc.org/

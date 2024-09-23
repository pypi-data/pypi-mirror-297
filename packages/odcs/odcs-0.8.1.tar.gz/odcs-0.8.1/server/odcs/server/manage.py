# -*- coding: utf-8 -*-
# Copyright (c) 2017  Red Hat, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import os
import ssl
import sys

import click
import flask_migrate

from flask.cli import FlaskGroup
from werkzeug.serving import run_simple

from odcs.server import app, conf, db


def _establish_ssl_context():
    if not conf.ssl_enabled:
        return None
    # First, do some validation of the configuration
    attributes = (
        "ssl_certificate_file",
        "ssl_certificate_key_file",
        "ssl_ca_certificate_file",
    )

    for attribute in attributes:
        value = getattr(conf, attribute, None)
        if not value:
            raise ValueError("%r could not be found" % attribute)
        if not os.path.exists(value):
            raise OSError("%s: %s file not found." % (attribute, value))

    # Then, establish the ssl context and return it
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_ctx.load_cert_chain(conf.ssl_certificate_file, conf.ssl_certificate_key_file)
    ssl_ctx.verify_mode = ssl.CERT_OPTIONAL
    ssl_ctx.load_verify_locations(cafile=conf.ssl_ca_certificate_file)
    return ssl_ctx


@click.group(cls=FlaskGroup, create_app=lambda *args, **kwargs: app)
def cli():
    """Manage ODCS application"""


migrations_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "migrations")
flask_migrate.Migrate(app, db, directory=migrations_dir)


@cli.command()
@click.option("-h", "--host", default=conf.host, help="Bind to this address")
@click.option("-p", "--port", type=int, default=conf.port, help="Listen on this port")
@click.option("-d", "--debug", is_flag=True, default=conf.debug, help="Debug mode")
def runssl(host, port, debug):
    """Runs the Flask app with the HTTPS settings configured in config.py"""
    logging.info("Starting ODCS frontend")

    ssl_ctx = _establish_ssl_context()
    run_simple(host, port, app, use_debugger=debug, ssl_context=ssl_ctx)


@cli.command()
def openapispec():
    """Dump OpenAPI specification"""
    import json

    if app.openapispec:
        print(json.dumps(app.openapispec.to_dict(), indent=2))
    else:
        logging.error("Can't generate OpenAPI specification.")
        sys.exit(1)


if __name__ == "__main__":
    cli()

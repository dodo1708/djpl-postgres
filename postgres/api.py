from __future__ import unicode_literals, print_function
import subprocess
import tempfile



class DumpDataError(Exception):
    """
    Raise whenever a dump error occurs
    """

def dump_database(host, db_name):
    """
    Dumps the passed database for the current product.
    :param db_name:
    :return:
    """

    temp = tempfile.NamedTemporaryFile()

    print(
        subprocess.check_output('pg_dump --no-owner --host {host} --username postgres  -f {tmp} {db}'.format(
            host=host,
            tmp=temp.name,
            db=db_name
        ), shell=True)
    )

    dump = temp.read()
    temp.close()

    if len(dump) < 200:
        # in case the dump has less than 5 lines, it probably failed
        raise DumpDataError('Dumping database failed: {content}'.format(content=dump))

    return dump


def list_database_names():
    """
    Returns all database names.
    :param host:
    :return:
    """
    from django_productline.context import PRODUCT_CONTEXT
    output = subprocess.check_output('psql --username postgres --host {host} -q -A -t -c "SELECT datname FROM pg_database"'.format(
        host=PRODUCT_CONTEXT.DB_HOST
    ), shell=True)
    return output

def restore_database(target_path, db_name, owner):
    """
    Restore a postgresql database from a dumpfile.
    :param target_path:
    :param db_name:
    :param owner:
    :return:
    """

    from django.conf import settings
    host = settings.DATABASES['default']['HOST']

    print(
        subprocess.check_output('psql --host {host} --username {owner} -f {path} {db}'.format(
            host=host,
            owner=owner,
            path=target_path,
            db=db_name
        ), shell=True)
    )

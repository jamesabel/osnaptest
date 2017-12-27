
import sys

from osnap import init_logger, get_logger
import osnap.installer

from osnaptest import __application_name__, __version__, __author__, __python_version__


log = get_logger(__application_name__)


def make_installer():

    verbose = '-v' in sys.argv
    init_logger(__application_name__, __author__, verbose=verbose)
    log.info(f'verbose={verbose}')
    osnap.installer.make_installer(__python_version__, __application_name__, __version__, __author__,
                                   'osnap_test_example', 'www.abel.co', variant='window'
                                   )


if __name__ == '__main__':
    make_installer()


from PyQt5.QtWidgets import QApplication, QLabel

import cryptography.fernet

from osnap import AppUpdaterGithubEmulationLocal

from osnaptest import __application_name__, __author__, __version__
from osnaptest import init_logger, get_logger

log = get_logger(__application_name__)


def osnaptest():

    init_logger(__application_name__, __author__, 'log', True)

    app = QApplication([])

    m = b'osnap works!'

    k = cryptography.fernet.Fernet.generate_key()
    fernet = cryptography.fernet.Fernet(k)
    t = fernet.encrypt(m)
    d = fernet.decrypt(t)

    assert(m == d)

    github_account = 'jamesabel'  # github account, not app author
    updater = AppUpdaterGithubEmulationLocal(__application_name__, github_account, __version__)
    um = '%s (current:%s, latest:%s)' % (updater.check_if_update_available(), __version__, updater.get_latest_version())

    window = QLabel(f'original message:\n{m}\n\nkey:\n{k}\n\ntoken:\n{t}\n\ndecoded message:\n{d}\n\nupdate available:{um}')
    window.show()

    app.exec_()

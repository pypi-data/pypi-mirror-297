from qtstrap import OPTIONS
from qtstrap.extras.style import apply_theme
from .qt import *
import signal
import sys
from pathlib import Path
import qtawesome as qta


def install_ctrlc_handler(app):
    def ctrlc_handler(sig=None, frame=None):
        app.closeAllWindows()   # this makes sure the MainWindow's .close() method gets called
        app.quit()

    # grab the keyboard interrupt signal
    signal.signal(signal.SIGINT, ctrlc_handler)

    # empty timer callback
    def update():
        pass

    # create timer to force python interpreter to get some runtime
    app._ctrlc_timer = QTimer()
    app._ctrlc_timer.timeout.connect(update)
    app._ctrlc_timer.start(10)


def install_app_info(app):
    if OPTIONS.app_info:
        info = OPTIONS.app_info

        if info.AppPublisher:
            app.setOrganizationName(info.AppPublisher)
        if info.AppPublisher:
            app.setOrganizationDomain(info.AppPublisher)
        if info.AppName:
            app.setApplicationName(info.AppName)
        if info.AppVersion:
            app.setApplicationVersion(info.AppVersion)

        if files := list(Path(OPTIONS.APPLICATION_PATH).rglob(info.AppIconName)):
            app.setWindowIcon(QIcon(files[0].as_posix()))


class BaseApplication(QApplication):
    theme_changed = Signal()

    def __init__(self, register_ctrlc_handler=True) -> None:
        super().__init__(sys.argv)

        install_app_info(self)

        if register_ctrlc_handler:
            install_ctrlc_handler(self)

        default_theme = 'light'
        theme = QSettings().value('theme', default_theme)
        self.change_theme(theme)

    def change_theme(self, theme: str, force=False):
        if not force and theme == OPTIONS.theme:
            return

        OPTIONS.theme = theme
        QSettings().setValue('theme', theme)

        # TODO: find and redraw all icons
        qta.reset_cache()
        apply_theme(theme, self)

        self.theme_changed.emit()

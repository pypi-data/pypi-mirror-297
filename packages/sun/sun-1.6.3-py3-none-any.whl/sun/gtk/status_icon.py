#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf

from sun.licenses import ABOUT, LICENSE
from sun.__metadata__ import (
    __prgnam__,
    __email__,
    __author__,
    __version__,
    __website__,
    data_configs
)

from sun.utils import Utilities
from sun.configs import Configs
from sun.cli.tool import Tools


class GtkStatusIcon(Configs):

    """ GTK Status Icon
    """

    def __init__(self):
        super(Configs, self).__init__()
        self.data_configs: dict = data_configs
        self.menu = None
        self.tool = Tools()

        self.sun_icon: str = f'{self.data_configs["icon_path"]}/{__prgnam__}.png'
        self.status_icon = Gtk.StatusIcon()
        self.status_icon.set_from_file(self.sun_icon)
        self.status_icon.connect('popup-menu', self.right_click_event)

    def right_click_event(self, icon, button, time) -> None:  # pylint: disable=[R0914,R0915]
        """ Handler menu and submenu. """

        # Set Gtk menu and submenu
        submenu = Gtk.Menu()
        self.menu = Gtk.Menu()

        # Creating Start submenu handler
        img_start = Gtk.Image()
        img_start.set_from_stock(Gtk.STOCK_MEDIA_PLAY, 1)
        start = Gtk.ImageMenuItem('Start')
        start.connect('activate', self.daemon_start)
        start.set_image(img_start)

        # Creating Stop submenu handler
        img_stop = Gtk.Image()
        img_stop.set_from_stock(Gtk.STOCK_MEDIA_STOP, 1)
        stop = Gtk.ImageMenuItem('Stop')
        stop.connect('activate', self.daemon_stop)
        stop.set_image(img_stop)

        # Creating Restart submenu handler
        img_restart = Gtk.Image()
        img_restart.set_from_stock(Gtk.STOCK_REFRESH, 1)
        restart = Gtk.ImageMenuItem('Restart')
        restart.connect('activate', self.daemon_restart)
        restart.set_image(img_restart)

        # Creating Status submenu handler
        img_status = Gtk.Image()
        img_status.set_from_stock(Gtk.STOCK_PROPERTIES, 1)
        status = Gtk.ImageMenuItem('Status')
        status.connect('activate', self.show_daemon_status)
        status.set_image(img_status)

        # Creating the submenu fot the daemon
        submenu.append(start)
        submenu.append(stop)
        submenu.append(restart)
        submenu.append(status)
        img_daemon = Gtk.Image()
        img_daemon.set_from_stock(Gtk.STOCK_PREFERENCES, 1)
        daemon = Gtk.ImageMenuItem('Daemon')
        daemon.set_submenu(submenu)
        daemon.set_image(img_daemon)
        self.menu.append(daemon)

        # Creating Check Updates menu handler
        img_check = Gtk.Image()
        img_check.set_from_stock(Gtk.STOCK_OK, 1)
        check = Gtk.ImageMenuItem('Check Updates')
        check.connect('activate', self.show_check_updates)
        check.set_image(img_check)
        self.menu.append(check)

        # Creating Os Info menu handler
        img_info = Gtk.Image()
        img_info.set_from_stock(Gtk.STOCK_INFO, 1)
        os_info = Gtk.ImageMenuItem('Os Info')
        os_info.connect('activate', self.show_os_info)
        os_info.set_image(img_info)
        self.menu.append(os_info)

        # Creating separator
        sep = Gtk.SeparatorMenuItem()
        self.menu.append(sep)

        # Creating About menu handler
        img_about = Gtk.Image()
        img_about.set_from_stock(Gtk.STOCK_ABOUT, 1)
        about = Gtk.ImageMenuItem('About')
        about.connect('activate', self.show_about_dialog)
        about.set_image(img_about)
        self.menu.append(about)

        # Creating Quit menu handler
        img_quit = Gtk.Image()
        img_quit.set_from_stock(Gtk.STOCK_QUIT, 1)
        quit_and_exit = Gtk.ImageMenuItem('Quit')
        quit_and_exit.connect('activate', Gtk.main_quit)
        quit_and_exit.set_image(img_quit)
        self.menu.append(quit_and_exit)

        self.menu.show_all()

        self.menu.popup(None, None, None, self.status_icon, button, time)

    def message(self, data, title) -> None:
        """ Method to display messages to the user. """
        msg = Gtk.MessageDialog(type=Gtk.MessageType.INFO,
                                buttons=Gtk.ButtonsType.CLOSE)
        msg.set_resizable(0)
        msg.set_title(title)
        msg.format_secondary_text(data)
        msg.set_icon_from_file(self.sun_icon)
        msg.run()
        msg.destroy()

    def show_check_updates(self, widget) -> None:
        """ Show message updates. """
        title: str = 'SUN - Check Updates'
        data, packages = self.tool.check_updates()
        count: int = len(packages)
        if count > 0:
            packages: list = packages[:10]
            if count > 10:
                packages += ['\nand more...']
            self.message('{0}\n{1}'.format(data, '\n'.join(packages)), title)
        else:
            self.message(data, title)

    def show_os_info(self, widget) -> None:
        """ Show message OS info. """
        title: str = 'SUN - OS Info'
        data: str = Utilities().os_info()
        self.message(data, title)

    def show_about_dialog(self, widget) -> None:
        """ Show message About info. """
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name('SUN - About')
        about_dialog.set_icon_from_file(self.sun_icon)
        about_dialog.set_program_name('SUN')
        about_dialog.set_version(__version__)
        about_dialog.set_authors([f'{__author__} <{__email__}>'])
        about_dialog.set_license('\n'.join(LICENSE))
        about_dialog.set_website(__website__)
        about_dialog.set_logo(Pixbuf.new_from_file(self.sun_icon))
        about_dialog.set_comments(ABOUT)
        about_dialog.run()
        about_dialog.destroy()

    def daemon_start(self, widget) -> None:
        """ Show message and start the daemon. """
        title: str = 'SUN daemon'
        data: str = 'SUN daemon starts...'
        data: str = self.tool.daemon_process('start', data)
        self.message(data, title)

    def daemon_stop(self, widget) -> None:
        """ Show message and stop the daemon. """
        title: str = 'SUN daemon'
        data: str = 'SUN daemon stops'
        data: str = self.tool.daemon_process('stop', data)
        self.message(data, title)

    def daemon_restart(self, widget) -> None:
        """ Show message and restart the daemon. """
        title: str = 'SUN daemon'
        data: str = 'SUN daemon restarts...'
        data: str = self.tool.daemon_process('restart', data)
        self.message(data, title)

    def show_daemon_status(self, widget) -> None:
        """ Show message status about the daemon. """
        title: str = 'SUN daemon'
        data: str = ('SUN is running...' if self.tool.daemon_status() else 'SUN is not running')
        self.message(data, title)


def main() -> None:
    """ GTK Main function.
    """
    try:
        GtkStatusIcon()
        Gtk.main()
    except KeyboardInterrupt as e:
        raise SystemExit(1) from e

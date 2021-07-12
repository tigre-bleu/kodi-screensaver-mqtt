import sys
import xbmcaddon
import xbmcgui
import xbmc
import paho.mqtt.publish as publish 

Addon = xbmcaddon.Addon('screensaver.mqtt')

__scriptname__ = Addon.getAddonInfo('name')
__path__ = Addon.getAddonInfo('path')


class Screensaver(xbmcgui.WindowXMLDialog):

    class ExitMonitor(xbmc.Monitor):

        def __init__(self, exit_callback):
            self.exit_callback = exit_callback

        def onScreensaverDeactivated(self):
            print '3 ExitMonitor: sending exit_callback'
            self.exit_callback()

    def publish(self, status):
        publish.single(Addon.getSetting("topic"), payload=status, retain=False, hostname=Addon.getSetting("host"), port=Addon.getSettingInt("port"))

    def onInit(self):
        print '2 Screensaver: onInit'
        self.monitor = self.ExitMonitor(self.exit)
        self.publish('ON')

    def exit(self):
        print '4 Screensaver: Exit requested'
        self.publish('OFF')
        self.close()


if __name__ == '__main__':
    print '1 Python Screensaver Started'
    screensaver_gui = Screensaver(
            'script-main.xml',
            __path__,
            'default',
        )
    screensaver_gui.doModal()
    print '5 Python Screensaver Exited'
    del screensaver_gui
    sys.modules.clear()

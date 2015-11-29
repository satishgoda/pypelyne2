import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import src.conf.settings.SETTINGS as SETTINGS


class CompositeIcon(QtGui.QPixmap):
    def __init__(self, plugin=None, *__args):
        super(CompositeIcon, self).__init__()

        self.plugin = plugin

        if self.plugin.icon is None:
            icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON)
        else:
            icon = QtGui.QPixmap(self.plugin.icon)
        self._icon = icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT, QtCore.Qt.SmoothTransformation)

        self._pixmap = QtGui.QPixmap(SETTINGS.PLUGINS_ICON_HEIGHT, SETTINGS.PLUGINS_ICON_HEIGHT)

        if self.plugin.architecture == 'x32':
            self.arch_icon = QtGui.QPixmap(SETTINGS.ICON_X32)
        elif self.plugin.architecture == 'x64':
            self.arch_icon = QtGui.QPixmap(SETTINGS.ICON_X64)
        self.arch_icon = self.arch_icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT,
                                                       QtCore.Qt.SmoothTransformation)

    @property
    def pixmap(self):
        color = QtGui.QColor(0, 0, 0, 0)
        _pixmap = self._pixmap
        _pixmap.fill(color)

        painter = QtGui.QPainter()
        painter.begin(_pixmap)
        painter.drawPixmap(0, 0, self._icon)
        painter.setCompositionMode(painter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, self.arch_icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT/2.5,
                                                               QtCore.Qt.SmoothTransformation))
        painter.end()

        return _pixmap

    @property
    def pixmap_hovered(self):
        color_hovered = QtGui.QColor(0, 0, 0, 0)
        _pixmap_hovered = self._icon.alphaChannel()
        _pixmap_hovered.fill(color_hovered)

        painter_hovered = QtGui.QPainter()
        painter_hovered.begin(_pixmap_hovered)
        painter_hovered.drawPixmap(0, 0, self.arch_icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT/2.5,
                                                                       QtCore.Qt.SmoothTransformation))
        painter_hovered.setCompositionMode(painter_hovered.CompositionMode_SourceOver)
        painter_hovered.drawPixmap(0, 0, self._icon)
        painter_hovered.end()

        return _pixmap_hovered

    @property
    def pixmap_no_arch(self):
        return self._icon
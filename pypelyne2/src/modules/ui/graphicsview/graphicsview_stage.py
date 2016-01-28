import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.graphicsview.graphicsview as graphicsview
import pypelyne2.src.modules.ui.graphicsscene.graphicsscene as graphicsscene
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class GraphicsViewStage(graphicsview.GraphicsView):
    def __init__(self):
        super(GraphicsViewStage, self).__init__()
        self.scene = graphicsscene.GraphicsScene(self)
        self.setScene(self.scene)

        self.cursor = QtGui.QCursor(QtCore.Qt.CrossCursor)
        # QtGui.QApplication.setCur(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.viewport().setCursor(self.cursor)

        self.setMouseTracking(False)

        self.setDragMode(self.RubberBandDrag)

        self.point = QtGui.QGraphicsRectItem(-10, -10, 20, 20)
        self.scene.addItem(self.point)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.mouse_position_previous = QtCore.QPoint(0, 0)

        self.navigator_rect = None

        self.navigator()

    def navigator(self):
        nav_width = 30
        nav_height = 20
        self.navigator_rect = QtGui.QGraphicsRectItem(0, 0, nav_width, nav_height)
        self.navigator_rect.setPos(self.rect().width()-nav_width, self.rect().height()-nav_height)
        self.scene.addItem(self.navigator_rect)

    def adjust_navigator(self):
        # nav_width = 30
        # nav_height = 20

        self.navigator_rect.setRect(0,
                                    0,
                                    self.scene.itemsBoundingRect().width()*0.1,
                                    self.scene.itemsBoundingRect().height()*0.1)

        self.navigator_rect.setPos(self.rect().width()-self.navigator_rect.rect().width(),
                                   self.rect().height()-self.navigator_rect.rect().height())

    def mouseMoveEvent(self, event):
        self.setDragMode(self.RubberBandDrag)
        event_pos_scene = event.pos()
        previous_pos = self.mouse_position_previous
        delta = previous_pos - event_pos_scene

        mouse_modifiers = QtGui.QApplication.mouseButtons()
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()

        if mouse_modifiers == QtCore.Qt.MidButton \
                or keyboard_modifiers == QtCore.Qt.ControlModifier and mouse_modifiers == QtCore.Qt.LeftButton:
            # QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
            self.setDragMode(self.NoDrag)
            group = self.scene.createItemGroup(self.scene.node_items)
            self.point.setPos(event_pos_scene)
            group.translate(-1*delta.x(), -1*delta.y())
            self.scene.destroyItemGroup(group)
            # self.setDragMode(self.RubberBandDrag)

            # return

        self.mouse_position_previous = event_pos_scene

        # QtGui.QApplication.restoreOverrideCursor()

        return QtGui.QGraphicsView.mouseMoveEvent(self, event)

    # def mousePressEvent(self, event):
    #     mouse_modifiers = QtGui.QApplication.mouseButtons()
    #     keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
    #
    #     if mouse_modifiers == QtCore.Qt.MidButton \
    #             or keyboard_modifiers == QtCore.Qt.ControlModifier and mouse_modifiers == QtCore.Qt.LeftButton:
    #         QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
    #
    #     return QtGui.QGraphicsView.mousePressEvent(self, event)
    #
    # def mouseReleaseEvent(self, event):
    #     QtGui.QApplication.restoreOverrideCursor()
    # #     if self.dragMode() != self.RubberBandDrag:
    # #         self.setDragMode(self.RubberBandDrag)
    #
    #     return QtGui.QGraphicsView.mousePressEvent(self, event)

    def wheelEvent(self, event):
        # QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

        self.adjust_navigator()

        group = self.scene.createItemGroup(self.scene.node_items)

        # absolute pos of mouse cursor in scene
        event_pos_scene = self.mapToScene(event.pos())

        self.point.setPos(event_pos_scene)

        group.setTransformOriginPoint(event_pos_scene)

        if event.delta() > 0:
            self.point.setScale(self.point.scale() * (1+SETTINGS.ZOOM_INCREMENT))
            group.setScale(group.scale() + SETTINGS.ZOOM_INCREMENT)
            # self.scene.item_group.setScale(group.scale() + SETTINGS.ZOOM_INCREMENT)
            self.scene.global_scale *= (1+SETTINGS.ZOOM_INCREMENT)
        else:
            self.point.setScale(self.point.scale() * (1-SETTINGS.ZOOM_INCREMENT))
            group.setScale(group.scale() - SETTINGS.ZOOM_INCREMENT)
            # self.scene.item_group.setScale(group.scale() - SETTINGS.ZOOM_INCREMENT)
            self.scene.global_scale *= (1-SETTINGS.ZOOM_INCREMENT)

        self.scene.destroyItemGroup(group)

        # QtGui.QApplication.restoreOverrideCursor()

        return QtGui.QGraphicsView.wheelEvent(self, event)

    def resizeEvent(self, event):
        self.setSceneRect(0, 0, self.width(), self.height())
        self.scene.base_rect.setRect(QtCore.QRectF(self.rect()))

        self.adjust_navigator()

        return QtGui.QGraphicsView.resizeEvent(self, event)

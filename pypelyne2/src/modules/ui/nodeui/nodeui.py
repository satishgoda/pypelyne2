import os
import logging
import random
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.nodecore.nodecore as nodecore
import pypelyne2.src.modules.ui.qgraphicsproxywidgetnowheel.qgraphicsproxywidgetnowheel as qgraphicsproxywidgetnowheel
import pypelyne2.src.modules.ui.compositeicon.compositeicon as compositeicon
import pypelyne2.src.parser.parse_plugins as parse_plugins
# import pypelyne2.src.modules.ui.resourcebarwidget.resourcebarwidget as resourcebarwidget
import pypelyne2.src.modules.ui.portwidget.portwidget as output
import pypelyne2.src.modules.ui.connection.connection as connection
import pypelyne2.src.modules.ui.nodedroparea.nodedroparea as nodedroparea
import pypelyne2.src.modules.ui.labelcollapseexpand.labelcollapseexpand as labelcollapseexpand
import pypelyne2.src.modules.ui.labelgif.labelgif as labelgif


class QLabelMaximize(QtGui.QLabel):
    def __init__(self):
        super(QLabelMaximize, self).__init__()

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on QLabelMaximize ({0})'.format(self))
        if event.button() == QtCore.Qt.RightButton:
            self.emit(QtCore.SIGNAL('clicked'))
        else:
            return QtGui.QLabel.mousePressEvent(self, event)


class WidgetNode(QtGui.QWidget):
    def __init__(self, node_object=None):
        super(WidgetNode, self).__init__()

        self.node = node_object

        self.ui = None

        self.palette = QtGui.QPalette()

    def dragMoveEvent(self, event):
        logging.info('dragMoveEvent on QWidgetNode ({0})'.format(self))

        return QtGui.QWidget.dragMoveEvent(self, event)

    def set_palette(self):
        self.palette.setColor(QtGui.QWidget().backgroundRole(), QtGui.QColor(50, 50, 50, 0))
        self.ui.setPalette(self.palette)

    def wheelEvent(self, event):
        logging.info('wheelEvent on QWidgetNode ({0})'.format(self))
        event.ignore()


class WidgetTitle(WidgetNode):
    def __init__(self, node_object=None):
        super(WidgetTitle, self).__init__()

        self.node = node_object

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'nodeui',
                                          'nodeui_widget_title.ui'), self)

        self.set_palette()

        self.preview_icon = labelgif.LabelGif(self.node)

        self.setup_title()

    def setup_title(self):
        self.ui.label_title.setToolTip('shift+left click to change name')
        self.ui.label_title_edit.setToolTip('enter to submit')
        self.ui.label_title_edit.setText(self.ui.label_title.text())

        self.ui.label_title.setVisible(False)
        self.ui.label_title_edit.setVisible(True)

        self.ui.vlayout_preview.addWidget(self.preview_icon)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on OutputHover ({0})'.format(self))
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()

        if keyboard_modifiers == QtCore.Qt.ShiftModifier and event.button() == QtCore.Qt.LeftButton:
            self.ui.label_title.setVisible(False)
            self.ui.label_title_edit.setVisible(True)
            self.ui.label_title_edit.setReadOnly(False)
            self.ui.label_title_edit.setFocus()
            self.ui.label_title_edit.selectAll()

        return WidgetNode.mouseMoveEvent(self, event)


class WidgetElements(WidgetNode):
    def __init__(self):
        super(WidgetElements, self).__init__()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'nodeui',
                                          'nodeui_widget_elements.ui'), self)

        self.set_palette()

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on QWidgetElements ({0})'.format(self))
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
        mouse_modifiers = QtGui.QApplication.mouseButtons()
        if mouse_modifiers == QtCore.Qt.MidButton \
                or keyboard_modifiers == QtCore.Qt.ControlModifier and mouse_modifiers == QtCore.Qt.LeftButton:
            event.ignore()
            return

        return WidgetNode.mouseMoveEvent(self, event)


class NodeUI(nodecore.NodeCore, QtGui.QGraphicsItem):
    def __init__(self, puppeteer, position=QtCore.QPoint(0, 0), plugin=None, scene_object=None):
        super(NodeUI, self).__init__()

        self.puppeteer = puppeteer

        # TODO: maybe add a shortcut/button to references?

        reload(SETTINGS)

        self.scene_object = scene_object

        self.plugin = plugin or parse_plugins.get_plugins()[random.randint(0, len(parse_plugins.get_plugins())-1)].x64
        self.compositor = compositeicon.CompositeIcon(self.plugin)

        self.rect = QtCore.QRectF()

        self.drop_area = nodedroparea.NodeDropArea(self)

        self.drop_area.setZValue(self.zValue() + 1)
        self.drop_area.setParentItem(self)

        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.gradient = QtGui.QLinearGradient(self.rect.topLeft(), self.rect.bottomLeft())

        self.setAcceptHoverEvents(True)
        # self.setAcceptTouchEvents(True)

        self.task_color_item = QtGui.QColor(0, 0, 0)
        self.application_color_item = QtGui.QColor(0, 0, 0)

        self.setPos(position)

        self.hovered = False
        self.output_list = []
        self.input_list = []
        # self.outputs = []
        # self.inputs = []
        self.connections = []

        # self._users = []

        # self.label = QtGui.QGraphicsTextItem()

        # self.set_label(self.plugin.abbreviation)

        self.widget_title = WidgetTitle(self)
        self.widget_elements = WidgetElements()

        self.widget_title_proxy = qgraphicsproxywidgetnowheel.QGraphicsProxyWidgetNoWheel()
        self.widget_elements_proxy = qgraphicsproxywidgetnowheel.QGraphicsProxyWidgetNoWheel()

        # cpu usage bar is just a placeholder for future "progress"
        # self.progress_bar = resourcebarwidget.NodeBarWidget(monitor_item='cpu', maximum=100)
        # # self.widget_title.status_layout.insertWidget(0, self.progress_bar)
        # self.widget_title.vlayout_performance.addWidget(self.progress_bar)
        # self.widget_title.vlayout_title.addWidget(self.progress_bar)
        self.widget_title.vlayout_title.insertStretch(-1)
        # self.progress_bar_proxy = QGraphicsProxyWidgetNoWheel()

        self.collapse = labelcollapseexpand.LabelCollapseExpand()
        self.expand = labelcollapseexpand.LabelCollapseExpand()
        self.maximize = QLabelMaximize()
        self.minimize = QLabelMaximize()

        self.icon = None
        self.arch_icon = None
        self.set_label(str(' '.join([self.plugin.family, self.plugin.release_number])))
        self.lock_icon = None
        self.maximize_icon = None
        self.set_task_icon()
        self.set_arch_icon()
        self.set_lock_icon()
        self.preview_icon_path = None
        self.set_thumbnail_icon()
        # self.task = None
        self.task_color_default = '#FFFFFF'
        self.task_color = None
        self.set_task_color()
        self.set_label_task()
        self.set_label_assignee()
        self.set_label_status()

        self.add_ui_elements()
        self.setup_expand_collapse()
        # self.setup_maximize()
        self.add_task_menu_items()
        self.add_assignee_menu_items()
        self.add_status_menu_items()
        self.add_supervisor_menu_items()

        self.update_title(init=True)

        self.widget_title.label_title_edit.returnPressed.connect(self.update_title)

        self.set_ui_widgets_position()

        self.resize()

        if SETTINGS.AUTO_GENERATE_RANDOM_OUTPUTS:
            for i in range(SETTINGS.AUTO_GENERATE_RANDOM_OUTPUTS_COUNT):
                self.add_output()

        if SETTINGS.AUTO_GENERATE_RANDOM_INPUTS:
            for i in range(SETTINGS.AUTO_GENERATE_RANDOM_INPUTS_COUNT):
                self.add_input(create_connection=False)

    def add_connection(self, start_item, end_item):
        connection_line = connection.Connection(start_item=start_item,
                                                end_item=end_item,
                                                scene_object=self.scene_object)
        self.connections.append(connection_line)
        self.scene_object.addItem(connection_line)
        self.scene_object.connection_items.append(connection_line)

        start_item.downstream_connections.append(connection_line)
        start_item.downstream_ports.append(end_item)
        end_item.upstream_connections.append(connection_line)

    def add_input(self, output_object=None, port_id=None, create_connection=True):

        start_item = self.puppeteer.find_output_graphics_item(scene=self.scene_object, port_id=port_id)
        # start_item = self.scene_object.find_output_graphics_item(port_id=port_id)

        end_item = output.Input(node_object=self,
                                output_object=output_object,
                                port_id=port_id,
                                start_item=start_item)

        self.inputs.append(end_item)
        end_item.setParentItem(self)

        if create_connection:
            self.add_connection(start_item=start_item, end_item=end_item)

        self.resize()

    def add_output(self, output_object=None, port_id=None):
        port = output.Output(node_object=self,
                             output_object=output_object,
                             port_id=port_id)
        self.outputs.append(port)
        port.setParentItem(self)
        self.resize()

    def update_title(self, init=False):
        title = self.widget_title.label_title
        title_edit = self.widget_title.label_title_edit

        title_edit.setReadOnly(True)

        if init:
            new_title = self.name_string
        else:
            new_title = title_edit.text()
            self.name_string = new_title

        title.setText(new_title)
        title_edit.setText(new_title)
        title_edit.setVisible(False)
        title.setVisible(True)
        self.resize()

    def setup_maximize(self):
        self.maximize.setToolTip('right click to minimize node')
        self.minimize.setToolTip('right click to maximize node')
        # self.widget_title.hlayout_minimize.addWidget(self.maximize)
        self.widget_title.hlayout_minimize.addWidget(self.maximize)
        self.widget_title.hlayout_minimize.addWidget(self.minimize)

        self.maximize.setPixmap(self.compositor.maximize_icon)
        self.minimize.setPixmap(self.compositor.minimize_icon)

        self.update_maximize_minimize()

        self.maximize.connect(self.maximize, QtCore.SIGNAL('clicked'), self.maximize_node)
        self.minimize.connect(self.minimize, QtCore.SIGNAL('clicked'), self.minimize_node)

    def update_maximize_minimize(self):
        pass

    def maximize_node(self):
        # self.widget_title.vlayout_preview.setVisible(True)
        self.widget_title_proxy.setVisible(True)
        # pass

    def minimize_node(self):
        # self.widget_title.vlayout_preview.setVisible(False)
        self.widget_title_proxy.setVisible(False)
        # pass

    def setup_expand_collapse(self):
        self.collapse.setToolTip('right click to collapse combo boxes')
        self.expand.setToolTip('right click to expand combo boxes')

        self.widget_title.hlayout_expand_collapse.addWidget(self.collapse)
        self.widget_title.hlayout_expand_collapse.addWidget(self.expand)

        self.expand.setPixmap(self.compositor.expand_icon)
        self.collapse.setPixmap(self.compositor.collapse_icon)

        self.update_expand_collapse()

        self.expand.connect(self.expand, QtCore.SIGNAL('clicked'), self.collapse_layout)
        self.collapse.connect(self.collapse, QtCore.SIGNAL('clicked'), self.expand_layout)

    def update_expand_collapse(self):
        self.expand.setVisible(False)
        self.collapse.setVisible(False)

        self.expand.setVisible(bool(not self.widget_elements.widget_comboboxes.isVisible()))
        self.collapse.setVisible(bool(self.widget_elements.widget_comboboxes.isVisible()))

    def expand_layout(self):
        self.collapse_layout_widgets(layout=self.widget_elements,
                                     size=0.0)
        self.widget_elements_proxy.setMaximumHeight(0.0)
        self.widget_elements_proxy.setMaximumWidth(0.0)
        self.widget_elements_proxy.setVisible(False)
        self.update_expand_collapse()
        self.resize()

    def collapse_layout(self):
        self.collapse_layout_widgets(layout=self.widget_elements,
                                     size=16777215.0)
        self.widget_elements_proxy.setMaximumHeight(16777215.0)
        self.widget_elements_proxy.setMaximumWidth(16777215.0)
        self.widget_elements_proxy.adjustSize()
        self.widget_elements_proxy.setVisible(True)
        self.update_expand_collapse()
        self.resize()

    def collapse_layout_widgets(self, layout, size):
        for i in layout.findChildren(QtCore.QObject):
            try:
                i.setMaximumHeight(float(size))
            except AttributeError, e:
                logging.info('{0} (occurred on {1})'.format(e, self))
            try:
                i.setMaximumWidth(float(size))
            except AttributeError, e:
                logging.info('{0} (occurred on {1})'.format(e, self))

    def reset_proxy_sizes(self):

        self.widget_title_proxy.resize(0, 0)
        self.widget_elements_proxy.resize(0, 0)
        self.widget_title_proxy.adjustSize()
        self.widget_elements_proxy.adjustSize()

    def update_thumbnail_icon(self, path):
        path = str(path)
        # self.preview_icon_path = path
        self.set_thumbnail_icon(path)

    def set_thumbnail_icon(self, icon_path=None):

        thumbnail_dict = self.get_thumbnail_icon(icon_path=icon_path)

        # img_pixmap = QtGui.QPixmap(thumbnail_dict[u'thumbnail'])
        img_pixmap = QtGui.QPixmap(thumbnail_dict[u'thumbnail'])
        pixmap_width = img_pixmap.width()
        pixmap_height = img_pixmap.height()

        if thumbnail_dict[u'extension'] == '.gif' and SETTINGS.ENABLE_GIF_PREVIEW:
            movie = QtGui.QMovie(thumbnail_dict[u'thumbnail'])
            movie.setCacheMode(movie.CacheAll)

            if pixmap_width > pixmap_height:
                logging.info('gif has landscape format')
                ratio = pixmap_height/float(pixmap_width)
                movie.setScaledSize(QtCore.QSize(SETTINGS.PLUGINS_ICON_HEIGHT*2,
                                                 int(round(SETTINGS.PLUGINS_ICON_HEIGHT*2*ratio))))
            elif pixmap_width == pixmap_height:
                logging.info('gif has square format')
                movie.setScaledSize(QtCore.QSize(SETTINGS.PLUGINS_ICON_HEIGHT*2,
                                                 SETTINGS.PLUGINS_ICON_HEIGHT*2))
            elif pixmap_width < pixmap_height:
                logging.info('gif has portrait format')
                ratio = pixmap_width/float(pixmap_height)
                movie.setScaledSize(QtCore.QSize(int(round(SETTINGS.PLUGINS_ICON_HEIGHT*2*ratio)),
                                                 SETTINGS.PLUGINS_ICON_HEIGHT*2))

            self.widget_title.preview_icon.setToolTip('right click to play gif')
            self.widget_title.preview_icon.setMovie(movie)
            self.widget_title.preview_icon.connect(self.widget_title.preview_icon,
                                                   QtCore.SIGNAL('right_mouse_button_pressed'),
                                                   self.change_movie_state)

            movie.start()
            movie.setPaused(SETTINGS.DISABLE_GIF_AUTOSTART)

        else:
            if pixmap_width > pixmap_height:
                logging.info('thumbnail has landscape format')
                img_pixmap = img_pixmap.scaledToWidth(SETTINGS.PLUGINS_ICON_HEIGHT*2, QtCore.Qt.SmoothTransformation)
            elif pixmap_width == pixmap_height:
                logging.info('thumbnail has square format')
                img_pixmap = img_pixmap.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT*2, QtCore.Qt.SmoothTransformation)
            elif pixmap_width < pixmap_height:
                logging.info('thumbnail has portrait format')
                img_pixmap = img_pixmap.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT*2, QtCore.Qt.SmoothTransformation)

            # draw  rounded preview icon
            new_width = img_pixmap.width()
            new_height = img_pixmap.height()

            color = QtGui.QColor(0, 0, 0, 0)

            new_pixmap = QtGui.QPixmap(new_width, new_height)
            new_pixmap.fill(color)

            rect = QtCore.QRect(0, 0, new_width-1, new_height-1)

            brush = QtGui.QBrush(img_pixmap)
            painter = QtGui.QPainter()
            # painter.setRenderHint(painter.HighQualityAntialiasing)
            painter.begin(new_pixmap)
            painter.setBrush(brush)
            painter.drawRoundedRect(rect, SETTINGS.PREVIEW_ROUNDNESS, SETTINGS.PREVIEW_ROUNDNESS)
            painter.end()

            self.widget_title.preview_icon.setToolTip('this is not a gif animation')
            self.widget_title.preview_icon.setPixmap(new_pixmap)
            self.widget_title.preview_icon.disconnect(self.widget_title.preview_icon,
                                                      QtCore.SIGNAL('right_mouse_button_pressed'),
                                                      self.change_movie_state)

    def change_movie_state(self):
        movie = self.widget_title.preview_icon.movie()
        state = movie.state()
        if state == 0:
            movie.start()
        elif state == 1:
            movie.setPaused(False)
        elif state == 2:
            movie.setPaused(True)

    def set_label(self, text):
        self.widget_title.label_label.setText(text)

    def set_task_icon(self):
        scale = self.compositor.pixmap_no_overlay.size() * SETTINGS.ICON_SCALE
        self.widget_title.label_icon.setPixmap(self.compositor.pixmap_no_overlay.scaled(scale))

    def set_arch_icon(self):
        scale = self.compositor.arch_icon.size() * SETTINGS.ICON_SCALE
        self.widget_title.label_arch_icon.setPixmap(self.compositor.arch_icon.scaled(scale))

    def set_lock_icon(self):
        scale = self.compositor.lock.size() * SETTINGS.ICON_SCALE
        self.widget_title.label_lock_icon.setPixmap(self.compositor.lock.scaled(scale))

    def add_ui_elements(self):
        self.widget_title_proxy.setWidget(self.widget_title)
        self.widget_title_proxy.setParentItem(self)

        self.widget_elements_proxy.setWidget(self.widget_elements)
        self.widget_elements_proxy.setParentItem(self)

    def add_task_menu_items(self):
        combobox = self.widget_elements.combobox_task
        combobox.addItem('-select task-')

        index = 0

        for task in self.get_tasks:
            index += 1
            combobox.addItem(task.task)
            combobox.setItemData(index, task)

        combobox.activated.connect(self.set_task_color)
        combobox.activated.connect(self.set_label_task)

    def add_status_menu_items(self):
        combobox = self.widget_elements.combobox_status
        combobox.addItem('-select status-')

        index = 0

        for status in SETTINGS.NODE_STATES:
            index += 1
            combobox.addItem(status[u'state'])
            combobox.setItemData(index, status[u'color'])

        combobox.activated.connect(self.set_label_status)

    def add_assignee_menu_items(self):
        combobox = self.widget_elements.combobox_assignee
        combobox.addItem('-select assignee-')

        index = 0

        for user in self.get_users:
            index += 1
            combobox.addItem(user.name_full)
            combobox.setItemData(index, user.id)

        combobox.activated.connect(self.set_label_assignee)
        combobox.activated.connect(self.set_combobox_department)
        combobox.activated.connect(self.clear_reports_to)

    def clear_reports_to(self):
        layout_reports_to = self.widget_elements.vlayout_reports_to

        while layout_reports_to.count():
            child = layout_reports_to.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()

    def set_combobox_department(self):

        combobox_department = self.widget_elements.combobox_department

        combobox_department.clear()

        combobox_department.addItem('-select department-')

        if self.current_combobox_assignee_index == 0:
            return

        else:
            index = 0

            combobox_assignee = self.widget_elements.combobox_assignee

            data = combobox_assignee.itemData(self.current_combobox_assignee_index)

            user_id = data.toPyObject()
            for user in self.get_users:
                if user.id == user_id:
                    reports_to_list = user.department_reports_to

            for reports_to in reports_to_list:
                index += 1
                combobox_department.addItem(reports_to[u'department'])
                combobox_department.setItemData(index, reports_to[u'reports_to_users'])

            combobox_department.activated.connect(self.set_label_report_to)

    def set_label_report_to(self):
        combobox_department = self.widget_elements.combobox_department
        layout_reports_to = self.widget_elements.vlayout_reports_to

        self.clear_reports_to()

        while layout_reports_to.count():
            child = layout_reports_to.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()

        if self.current_combobox_deparment_index == 0:
            widget = QtGui.QLabel('-none-')
            layout_reports_to.addWidget(widget)

        else:
            data = combobox_department.itemData(self.current_combobox_deparment_index)

            reports_to_id_list = data.toPyObject()

            for reports_to_id in reports_to_id_list:
                widget = QtGui.QLabel(reports_to_id)

                layout_reports_to.addWidget(widget)

        layout_reports_to.addStretch()

        self.resize()

    def add_supervisor_menu_items(self):
        combobox = self.widget_elements.combobox_supervisor
        combobox.addItem('-select supervisor-')

        supervisors = ['Mark', 'Peter', 'Frank', 'David']

        for status in supervisors:
            combobox.addItem(status)

    def boundingRect(self):
        return self.rect

    def hoverEnterEvent(self, event):
        logging.info('hoverEnterEvent on NodeUI ({0})'.format(self))
        self.hovered = True

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        logging.info('hoverLeaveEvent on NodeUI ({0})'.format(self))
        self.hovered = False

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def set_ui_widgets_position(self):
        # title widget
        self.widget_title_proxy.setPos(0, 0)

        # elements widget
        self.widget_elements_proxy.setPos(0, self.widget_title_proxy.boundingRect().height())

    def paint(self, painter, option, widget):

        # print self.uuid, 'connections =', len(self.connections)

        painter.setRenderHint(painter.Antialiasing)

        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(0)

        hover_color = QtGui.QColor(255, 160, 0)

        if option.state & QtGui.QStyle.State_Selected:
            self.setZValue(1)
            pen.setWidth(3)
            pen.setColor(hover_color)
            self.gradient.setColorAt(0, self.task_color_item)
            self.gradient.setColorAt(1, self.task_color_item)

        elif option.state & QtGui.QStyle.State_MouseOver or self.hovered:
            pen.setWidth(2)
            self.setZValue(3)

            pen.setColor(hover_color)
            self.gradient.setColorAt(0, self.task_color_item)
            self.gradient.setColorAt(1, self.task_color_item.darker(160))

        else:
            pen.setWidth(0)
            self.setZValue(0)
            self.gradient.setColorAt(0, self.task_color_item)
            self.gradient.setColorAt(1, self.task_color_item.darker(160))

        painter.setBrush(self.gradient)

        painter.setPen(pen)

        painter.drawRoundedRect(self.rect, SETTINGS.NODE_ROUNDNESS, SETTINGS.NODE_ROUNDNESS)

    def arrange_outputs(self):
        for output_item in self.outputs:
            if self.widget_elements.widget_comboboxes.isVisible():
                position = QtCore.QPointF(self.boundingRect().width(),
                                          (self.outputs.index(output_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+self.widget_title.height())
            else:
                position = QtCore.QPointF(self.boundingRect().width(),
                                          (self.outputs.index(output_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+SETTINGS.OUTPUT_OFFSET)
            output_item.setPos(position)

    def arrange_inputs(self):
        for input_item in self.inputs:
            if self.widget_elements.widget_comboboxes.isVisible():
                position = QtCore.QPointF(0,
                                          (self.inputs.index(input_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+self.widget_title.height())
            else:
                position = QtCore.QPointF(0,
                                          (self.inputs.index(input_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+SETTINGS.OUTPUT_OFFSET)
            input_item.setPos(position)

    def resize(self):
        logging.info('node.resize() ({0})'.format(self))
        self.arrange_outputs()
        self.rect.setWidth(self.rect.width())
        self.rect.setHeight(self.rect.height())
        self.reset_proxy_sizes()
        self.resize_height()
        self.resize_width()
        self.arrange_outputs()
        self.arrange_inputs()
        self.drop_area.setRect(self.boundingRect())

    def resize_width(self):
        output_list_text_width = [0]
        input_list_text_width = [0]

        for i in self.input_list:
            input_list_text_width.append(int(i.childrenBoundingRect().width()))

        for i in self.output_list:
            output_list_text_width.append(int(i.childrenBoundingRect().width()))

        if self.widget_elements.widget_comboboxes.isVisible():
            self.rect.setWidth(max([
                                   max([self.widget_title_proxy.boundingRect().width(),
                                        self.widget_elements_proxy.boundingRect().width()]),
                                   (max(output_list_text_width) + 80) + (max(input_list_text_width))]))

        else:
            self.rect.setWidth(self.widget_title_proxy.boundingRect().width())
            # self.rect.setWidth(max([4*SETTINGS.PLUGINS_ICON_HEIGHT *
            #                        SETTINGS.ICON_SCALE +
            #                        max([self.label.boundingRect().width(),
            #                             self.widget_title_proxy.boundingRect().width()]),
            #                        (max(output_list_text_width) + 80) + (max(input_list_text_width))]))

    def resize_height(self):
        # print self.widget_elements.widget_comboboxes.isVisible()
        if self.widget_elements.widget_comboboxes.isVisible():
            self.rect.setHeight(max([self.widget_title_proxy.boundingRect().height() + self.widget_elements_proxy.boundingRect().height(),
                                     ((3*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE),
                                     SETTINGS.OUTPUT_OFFSET + max(len(self.outputs), len(self.inputs))*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING) + self.widget_title_proxy.boundingRect().height()]))

        else:
            # print self.label.boundingRect().height() + self.widget_title_proxy.boundingRect().height()
            # print (3*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE
            # print SETTINGS.OUTPUT_OFFSET + len(self.outputs)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING)

            self.rect.setHeight(max([self.widget_title_proxy.boundingRect().height(),
                                     (3*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE,
                                     SETTINGS.OUTPUT_OFFSET + max(len(self.outputs), len(self.inputs))*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING)]))

        self.gradient = QtGui.QLinearGradient(self.rect.topLeft(), self.rect.bottomLeft())

    @property
    def current_combobox_task_index(self):
        """returns the combobox_task index. False if task is not set"""
        combobox = self.widget_elements.combobox_task
        if combobox.currentIndex() == 0:
            return False
        else:
            return combobox.currentIndex()

    @property
    def current_combobox_task_color(self):
        """returns the current task color. False if task is not set."""
        try:
            combobox = self.widget_elements.combobox_task
            index = self.current_combobox_task_index
            if index:
                return combobox.itemData(index).toPyObject().color
            else:
                raise AttributeError
        except AttributeError:
            return False

    @property
    def current_combobox_task(self):
        """returns the current task color. empty string if task is not set."""
        combobox = self.widget_elements.combobox_task
        try:
            index = self.current_combobox_task_index
            if index:
                return combobox.itemData(index).toPyObject().abbreviation
            else:
                raise AttributeError
        except AttributeError:
            return ''

    @property
    def current_combobox_assignee_index(self):
        """returns the combobox_assignee index. False if task is not set"""
        combobox = self.widget_elements.combobox_assignee
        if combobox.currentIndex() == 0:
            return False
        else:
            return combobox.currentIndex()

    @property
    def current_combobox_deparment_index(self):
        """returns the deparment index. False if assignee is not set"""
        combobox = self.widget_elements.combobox_department
        if combobox.currentIndex() == 0:
            return False
        else:
            return combobox.currentIndex()

    @property
    def current_combobox_assignee(self):
        """returns the current assignee. empty string if task is not set."""
        combobox = self.widget_elements.combobox_assignee
        try:
            index = self.current_combobox_assignee_index
            if index:
                return combobox.currentText()
            else:
                raise AttributeError
        except AttributeError:
            return ''

    @property
    def current_combobox_status_index(self):
        """returns the combobox_status index. False if task is not set"""
        combobox = self.widget_elements.combobox_status
        if combobox.currentIndex() == 0:
            return False
        else:
            return combobox.currentIndex()

    @property
    def current_combobox_status(self):
        """returns the current assignee. empty string if task is not set."""
        combobox = self.widget_elements.combobox_status
        try:
            index = self.current_combobox_status_index
            if index:
                return combobox.currentText()
            else:
                raise AttributeError
        except AttributeError:
            return ''

    def set_task_color(self):
        logging.info('node.set_task_color() ({0})'.format(self))
        task_color = self.task_type or self.current_combobox_task_color or self.task_color_default
        self.task_color_item.setNamedColor(task_color)

    # @staticmethod
    # def _create_pushbutton(ui, text, icon, flat, focus_policy, tool_tip):
    #     ui.setText(text)
    #     ui.setIcon(icon)
    #     ui.setFlat(flat)
    #     ui.setFocusPolicy(focus_policy)
    #     ui.setToolTip(tool_tip)
    #
    # self._create_pushbutton(self.ui.pushButtonClearSearchProjects,
    #                         '',
    #                         cancel_icon,
    #                         True,
    #                         QtCore.Qt.NoFocus,
    #                         'clear filter')

    def set_label_task(self):
        logging.info('node.set_label_task() ({0})'.format(self))

        text = self.current_combobox_task
        label = self.widget_title.label_task
        label.setText(self.current_combobox_task)
        if text == '':
            label.setVisible(False)
        else:
            label.setVisible(True)

        self.resize()

    def set_label_assignee(self):
        logging.info('node.set_label_assignee() ({0})'.format(self))

        text = self.current_combobox_assignee
        label = self.widget_title.label_assignee
        label.setText(text)
        if text == '':
            label.setVisible(False)
        else:
            label.setVisible(True)

        self.resize()

    def set_label_status(self):
        logging.info('node.set_label_status() ({0})'.format(self))

        combobox = self.widget_elements.combobox_status

        text = self.current_combobox_status
        label = self.widget_title.label_status
        label.setText(text)
        palette = QtGui.QPalette()
        if text == '':
            label.setVisible(False)
        else:
            data = combobox.itemData(self.current_combobox_status_index)

            color_value = data.toPyObject()
            color = QtGui.QColor(0, 0, 0, 255)
            color.setNamedColor(color_value)

            palette.setColor(QtGui.QPalette.Base, color)
            label.setPalette(palette)
            label.setVisible(True)

        self.resize()

    def delete_node(self):
        logging.info('node.delete_node() ({0})'.format(self))

        temp_list_copy_inputs = list(self.inputs)
        temp_list_copy_outputs = list(self.outputs)

        for input_item in temp_list_copy_inputs:
            input_item.remove_input()

        for output_item in temp_list_copy_outputs:
            output_item.remove_output()

        del temp_list_copy_inputs
        del temp_list_copy_outputs

        self.scene_object.node_items.remove(self)

        self.scene_object.removeItem(self)

        print 'items left in scene:'
        for i in self.scene_object.items():
            print type(i)

    def keyPressEvent(self, event):
        logging.info('node.keyPressEvent() ({0})'.format(self))
        if event.key() == QtCore.Qt.Key_Backspace:
            self.delete_node()

    # def mouseDoubleClickEvent(self, event):
    #     self.scene_object.view_object.set_container_scene()

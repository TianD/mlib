__author__ = 'Nathan'

import logging
import __main__

from functools import partial

from ...lib import qt
from ...lib.qt import QtGui, QtCore
import maya.cmds as cmds

log = logging.getLogger(__name__)
QWIDGETSIZE_MAX = 16777215

class ShelfButton(QtGui.QToolButton):
	def __init__(self, parent=None):
		super(ShelfButton, self).__init__(parent)
		self.setAutoRaise(True)
		#self.setStyleSheet('QToolButton{margin: 0px 0px 0px 0px; border:none;}')

	def mouseMoveEvent(self, event):
		#print 'Mouse Move'
		if event.buttons() == QtCore.Qt.LeftButton:
			if not self.rect().contains(event.pos()):
				#self.hide()
				#self.parent().layout().removeWidget(self)
				drag = QtGui.QDrag(self)
				data = QtCore.QMimeData()
				data.setText(self.text())
				data.setImageData(self.icon().pixmap(32, 32, self.icon().Normal, self.icon().On))
				drag.setMimeData(data)
				drag.setPixmap(QtGui.QPixmap.grabWidget(self))
				#drag.setPixmap(self.icon().pixmap(32, 32, self.icon().Normal, self.icon().On))
				drag.setHotSpot(QtCore.QPoint(22, 22))

				shelfButtons = set(cmds.lsUI(typ='shelfButton'))
				dropAction = drag.exec_(QtCore.Qt.MoveAction|QtCore.Qt.CopyAction, QtCore.Qt.CopyAction)
				new_buttons = list(set(cmds.lsUI(typ='shelfButton')).difference(shelfButtons))

				if len(new_buttons) == 1:
					button = new_buttons.pop()
					print 'Dropped button!', button

				else:
					print 'Dropped', dropAction
					#print dropAction
					#print drag.target()
					#print drag.target().objectName()

		super(ShelfButton, self).mouseMoveEvent(event)


	@classmethod
	def createFromMaya(cls, data, control, controlType):
		btn = cls()
		if controlType == 'shelfButton':
			command = cmds.shelfButton(control, q=True, c=True)
			sType = cmds.shelfButton(control, q=True, sourceType=True)
			normal =  cmds.shelfButton(control, q=True, image=True)
			over = cmds.shelfButton(control, q=True, highlightImage=True)
			pressed = cmds.shelfButton(control, q=True, selectionImage=True)

			btn.setText(command)
		elif controlType == 'cmdScrollFieldExecuter':
			command = data.text()
			sType = cmds.cmdScrollFieldExecuter(control, q=True, sourceType=True)

		else:
			log.warn('Unsuported drag and drop source: %s - %s'%(controlType, control))


		return cls()


class TrashButton(QtGui.QToolButton):
	def __init__(self, parent=None):
		super(TrashButton, self).__init__(parent)
		self.setStyleSheet('QToolButton{margin: -2px -2px -2px -2px; border:none;}')
		self.setIconSize(QtCore.QSize(32, 32))
		self.setIcon(QtGui.QIcon(':/smallTrash.png'))
		self.setAutoRaise(True)
		self.setAcceptDrops(True)
		self.setObjectName('shelfTrashBtn')

	def dragEnterEvent(self, event):
		event.setDropAction(QtCore.Qt.MoveAction)
		event.accept()

	def dragMoveEvent(self, event):
		event.setDropAction(QtCore.Qt.MoveAction)
		event.accept()




def makeIcon(path, size=(64, 64)):
	pixmap_normal = QtGui.QPixmap(path).scaled(size[0], size[1], QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
	pixmap_over = pixmap_normal.copy()
	painter = QtGui.QPainter(pixmap_over)

	alpha = QtGui.QPixmap(pixmap_over.size())
	alpha.fill(QtGui.QColor(100, 100, 100))
	pixmap_dode = pixmap_normal.copy()
	pixmap_dode.setAlphaChannel(alpha)

	painter.setCompositionMode(painter.CompositionMode_ColorDodge)
	painter.drawPixmap(0, 0, pixmap_dode)

	painter.end()
	icon = QtGui.QIcon()
	icon.addPixmap(pixmap_normal, icon.Normal, icon.On)
	icon.addPixmap(pixmap_over, icon.Active, icon.On)
	return icon
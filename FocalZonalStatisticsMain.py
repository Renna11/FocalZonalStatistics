# coding=utf-8
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import FocalZonalStatistics
from PyQt5  import QtCore
from PyQt5  import QtGui
from PyQt5  import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QMenu, QAction

import subprocess
import multiprocessing as mp
from FZStatistics.KDFZProcess import *

class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = FocalZonalStatistics.Ui_Dialog()
        self.ui.setupUi(self)
        self.initUI()

    def initUI(self):
        cur_dir = os.getcwd()
        self.last_dir = cur_dir
        self.config_file_path = cur_dir + r"\config.ini"

        sel_pixmap = QtGui.QPixmap("icons/open.png")
        sel_icon = QtGui.QIcon(sel_pixmap)
        sel_icon.addPixmap(sel_pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)

        save_pixmap = QtGui.QPixmap("icons/save.png")
        save_icon = QtGui.QIcon(save_pixmap)
        save_icon.addPixmap(save_pixmap, QtGui.QIcon.Normal, QtGui.QIcon.Off)

        wnd_type_list = ["RECTANGLE", "CIRCLE", "ELLIPSE"]

        stats_type_list = ["MEAN", "PERCENTILE", "STD", "MAXIMUM", "MINIMUM", "SUM",
                           "MEDIAN","VARIETY", "RANGE", "MAJORITY", "MINORITY",
                           "CELLS COUNT", "COEFFICIENT OF VARIATION"]

        # <editor-fold desc="Focal">

        # <editor-fold desc="Rasters Setting">
        self.ui.editFocalValRas.setReadOnly(True)

        self.ui.btnFocalSelValRas.setIcon(sel_icon)
        self.ui.btnFocalSaveRstRas.setIcon(save_icon)
        self.ui.btnFocalSelValRas.setIconSize(QtCore.QSize(30, 30))
        self.ui.btnFocalSaveRstRas.setIconSize(QtCore.QSize(30, 30))

        self.ui.btnFocalSelValRas.clicked.connect(self.SelectFocalValueRaster)
        self.ui.btnFocalSaveRstRas.clicked.connect(self.SaveFocalResultRaster)
        # </editor-fold>

        # <editor-fold desc="Neighbourhood Setting">

        self.ui.cbFocalWndType.addItems(wnd_type_list)
        self.ui.cbFocalWndType.currentIndexChanged.connect(self.SetFocalNbhWndPara)
        self.ui.cbFocalWndType.setCurrentIndex(0)

        self.ui.labelFocalNbhSet1.setVisible(True)
        self.ui.editFocalNbhSet1.setVisible(True)
        self.ui.labelFocalNbhSet2.setVisible(True)
        self.ui.editFocalNbhSet2.setVisible(True)
        self.ui.labelFocalNbhSet3.setVisible(False)
        self.ui.editFocalNbhSet3.setVisible(False)

        self.ui.labelFocalNbhSet1.setText("Half Length")
        self.ui.editFocalNbhSet1.setText("50")
        self.ui.labelFocalNbhSet2.setText("Half Width")
        self.ui.editFocalNbhSet2.setText("50")

        self.ui.rbFocalCell.setChecked(True)

        # </editor-fold>

        # <editor-fold desc="Statistics Setting">
        self.ui.cbFocalStatsType.addItems(stats_type_list)
        self.ui.cbFocalStatsType.currentIndexChanged.connect(self.SetFocalStatsPara)
        self.ui.cbFocalStatsType.setCurrentIndex(0)
        self.ui.labelFocalPercentile.setVisible(False)
        self.ui.editFocalPercentile.setVisible(False)
        # </editor-fold>

        # <editor-fold desc="Advanced Setting">
        self.ui.editFocalDataChunk.setText("1,1")
        self.ui.editFocalProcNum.setText("16")
        self.ui.editFocalThreshold.setText("1")
        self.ui.cbFocalIgnoreNodata.setChecked(True)
        # </editor-fold>

        # </editor-fold>

        # <editor-fold desc="Zonal">

        # <editor-fold desc="Rasters Setting">
        self.ui.editZonalValRas.setReadOnly(True)
        self.ui.editZonalZoneRas.setReadOnly(True)

        self.ui.btnZonalSelValRas.setIcon(sel_icon)
        self.ui.btnZonalSelZoneRas.setIcon(sel_icon)
        self.ui.btnZonalSaveRstRas.setIcon(save_icon)

        self.ui.btnZonalSelValRas.setIconSize(QtCore.QSize(30, 30))
        self.ui.btnZonalSelZoneRas.setIconSize(QtCore.QSize(30, 30))
        self.ui.btnZonalSaveRstRas.setIconSize(QtCore.QSize(30, 30))

        self.ui.btnZonalSelValRas.clicked.connect(self.SelectZonalValueRaster)
        self.ui.btnZonalSelZoneRas.clicked.connect(self.SelectZonalZoneRaster)
        self.ui.btnZonalSaveRstRas.clicked.connect(self.SaveZonalResultRaster)
        # </editor-fold>

        # <editor-fold desc="Statistics Setting">
        self.ui.cbZonalStatsType.addItems(stats_type_list)
        self.ui.cbZonalStatsType.currentIndexChanged.connect(self.SetZonalStatsPara)
        self.ui.cbZonalStatsType.setCurrentIndex(0)
        self.ui.labelZonalPercentile.setVisible(False)
        self.ui.editZonalPercentile.setVisible(False)
        # </editor-fold>

        # <editor-fold desc="Advanced Setting">
        self.ui.editZonalThreshold.setText("1")
        self.ui.cbZonalIgnoreNodata.setChecked(True)
        # </editor-fold>

        # </editor-fold>

        # <editor-fold desc="Focal Zonal">

        # <editor-fold desc="Rasters Setting">
        self.ui.editFZMixedValRas.setReadOnly(True)
        self.ui.editFZMixedZoneRas.setReadOnly(True)

        self.ui.btnFZMixedSelValRas.setIcon(sel_icon)
        self.ui.btnFZMixedSelZoneRas.setIcon(sel_icon)
        self.ui.btnFZMixedSaveRstRas.setIcon(save_icon)

        self.ui.btnFZMixedSelValRas.setIconSize(QtCore.QSize(30, 30))
        self.ui.btnFZMixedSelZoneRas.setIconSize(QtCore.QSize(30, 30))
        self.ui.btnFZMixedSaveRstRas.setIconSize(QtCore.QSize(30, 30))

        self.ui.btnFZMixedSelValRas.clicked.connect(self.SelectFZMixedValueRaster)
        self.ui.btnFZMixedSelZoneRas.clicked.connect(self.SelectFZMixedZoneRaster)
        self.ui.btnFZMixedSaveRstRas.clicked.connect(self.SaveFZMixedResultRaster)
        # </editor-fold>

        # <editor-fold desc="Neighbourhood Setting">
        self.ui.cbFZMixedWndType.addItems(wnd_type_list)
        self.ui.cbFZMixedWndType.currentIndexChanged.connect(self.SetFZMixedNbhWndPara)
        self.ui.cbFZMixedWndType.setCurrentIndex(0)

        self.ui.labelFZMixedNbhSet1.setVisible(True)
        self.ui.editFZMixedNbhSet1.setVisible(True)
        self.ui.labelFZMixedNbhSet2.setVisible(True)
        self.ui.editFZMixedNbhSet2.setVisible(True)
        self.ui.labelFZMixedNbhSet3.setVisible(False)
        self.ui.editFZMixedNbhSet3.setVisible(False)

        self.ui.labelFZMixedNbhSet1.setText("Half Length")
        self.ui.editFZMixedNbhSet1.setText("50")
        self.ui.labelFZMixedNbhSet2.setText("Half Width")
        self.ui.editFZMixedNbhSet2.setText("50")

        self.ui.rbtnFZMixedCell.setChecked(True)

        # </editor-fold>

        # <editor-fold desc="Statistics Setting">
        self.ui.cbFZMixedStatsType.addItems(stats_type_list)
        self.ui.cbFZMixedStatsType.currentIndexChanged.connect(self.SetFZMixedStatsPara)
        self.ui.cbFZMixedStatsType.setCurrentIndex(0)
        self.ui.labelFZMixedPercentile.setVisible(False)
        self.ui.editFZMixedPercentile.setVisible(False)
        # </editor-fold>

        # <editor-fold desc="Advanced Setting">
        self.ui.editFZMixedDataChunk.setText("1,1")
        self.ui.editFZMixedProcNum.setText("16")
        self.ui.editFZMixedThreshold.setText("1")
        self.ui.cbFZIgnoreNodata.setChecked(True)
        # </editor-fold>

        # </editor-fold>

        # <editor-fold desc="Processing Message">
        # self.ui.tbMsg.setReadOnly(True)
        # </editor-fold>

        # <editor-fold desc="Dialog">
        self.setFixedSize(self.width(),self.height())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.ui.btnAddToConfigFile.clicked.connect(self.AddToConfigFile)

        menu = QMenu(self)
        action1 = QAction("Add to Config File", menu)
        menu.addAction(action1)
        action1.triggered.connect(self.AddToConfigFile)
        action2 = QAction("Open Config File", menu)
        menu.addAction(action2)
        action2.triggered.connect(self.OpenConfigFile)

        self.ui.btnAddToConfigFilePop.setMenu(menu)
        self.ui.btnAddToConfigFilePop.setStyleSheet("""
            QPushButton {
                text-align: right;
                padding-right: -8px;
            }
            QPushButton::menu-indicator {
                image: none;
            }
        """)

        self.ui.btnRun.clicked.connect(self.Run)

        menu = QMenu(self)
        action1 = QAction("Run", menu)
        menu.addAction(action1)
        action1.triggered.connect(self.Run)
        action2 = QAction("Run Config File", menu)
        menu.addAction(action2)
        action2.triggered.connect(self.RunConfigFile)

        self.ui.btnRunPop.setMenu(menu)
        self.ui.btnRunPop.setStyleSheet("""
            QPushButton {
                text-align: right;
                padding-right: -8px;
            }
            QPushButton::menu-indicator {
                image: none;
            }
        """)

        self.ui.btnQuit.clicked.connect(self.Quit)

        # </editor-fold>


    def printf(self, msg):
        self.ui.tbMsg.append(msg)
        self.cursot = self.ui.tbMsg.textCursor()
        self.ui.tbMsg.moveCursor(self.cursot.End)
        QtWidgets.QApplication.processEvents()


    # <editor-fold desc="Focal function">

    def SetFocalNbhWndPara(self, index):
        if index == 0:
            self.ui.labelFocalNbhSet1.setVisible(True)
            self.ui.editFocalNbhSet1.setVisible(True)
            self.ui.labelFocalNbhSet2.setVisible(True)
            self.ui.editFocalNbhSet2.setVisible(True)
            self.ui.labelFocalNbhSet3.setVisible(False)
            self.ui.editFocalNbhSet3.setVisible(False)

            self.ui.labelFocalNbhSet1.setText("Half Length")
            self.ui.editFocalNbhSet1.setText("50")
            self.ui.labelFocalNbhSet2.setText("Half Width")
            self.ui.editFocalNbhSet2.setText("50")
        elif index == 1:
            self.ui.labelFocalNbhSet1.setVisible(True)
            self.ui.editFocalNbhSet1.setVisible(True)
            self.ui.labelFocalNbhSet2.setVisible(False)
            self.ui.editFocalNbhSet2.setVisible(False)
            self.ui.labelFocalNbhSet3.setVisible(False)
            self.ui.editFocalNbhSet3.setVisible(False)

            self.ui.labelFocalNbhSet1.setText("Radius")
            self.ui.editFocalNbhSet1.setText("50")
        elif index == 2:
            self.ui.labelFocalNbhSet1.setVisible(True)
            self.ui.editFocalNbhSet1.setVisible(True)
            self.ui.labelFocalNbhSet2.setVisible(True)
            self.ui.editFocalNbhSet2.setVisible(True)
            self.ui.labelFocalNbhSet3.setVisible(True)
            self.ui.editFocalNbhSet3.setVisible(True)

            self.ui.labelFocalNbhSet1.setText("Semi-major Axis")
            self.ui.editFocalNbhSet1.setText("100")
            self.ui.labelFocalNbhSet2.setText("Ratio")
            self.ui.editFocalNbhSet2.setText("0.5")
            self.ui.labelFocalNbhSet3.setText("Angle (°)")
            self.ui.editFocalNbhSet3.setText("0")

    def SetFocalStatsPara(self, index):
        if index != 1:
            self.ui.labelFocalPercentile.setVisible(False)
            self.ui.editFocalPercentile.setVisible(False)
        else:
            self.ui.labelFocalPercentile.setVisible(True)
            self.ui.editFocalPercentile.setVisible(True)
            self.ui.editFocalPercentile.setText("98")

    def SelectFocalValueRaster(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Select Raster",
                                                         self.last_dir, "Raster Datasets (*.tif)")
        if fileName != "":
            self.ui.editFocalValRas.setText(fileName)
            self.last_dir = fileName

    def SaveFocalResultRaster(self):
        fileName, filetype = QFileDialog.getSaveFileName(self, "Save Raster",
                                                         self.last_dir, "Raster Datasets (*.tif)")
        if fileName != "":
            self.ui.editFocalRstRas.setText(fileName)
            self.last_dir = fileName

    # </editor-fold>

    # <editor-fold desc="Zonal function">
    def SelectZonalValueRaster(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Select Raster",
                                                         self.last_dir, "Raster Datasets (*.tif)")
        if fileName != "":
            self.ui.editZonalValRas.setText(fileName)
            self.last_dir = fileName

    def SelectZonalZoneRaster(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Select Raster",
                                                         self.last_dir, "Raster Datasets (*.tif)")
        if fileName != "":
            self.ui.editZonalZoneRas.setText(fileName)
            self.last_dir = fileName

    def SaveZonalResultRaster(self):
        fileName, filetype = QFileDialog.getSaveFileName(self, "Save Raster",
                                                         self.last_dir, "Raster Datasets (*.tif)")
        if fileName != "":
            self.ui.editZonalRstRas.setText(fileName)
            self.last_dir = fileName

    def SetZonalStatsPara(self, index):
        if index != 1:
            self.ui.labelZonalPercentile.setVisible(False)
            self.ui.editZonalPercentile.setVisible(False)
        else:
            self.ui.labelZonalPercentile.setVisible(True)
            self.ui.editZonalPercentile.setVisible(True)
            self.ui.editZonalPercentile.setText("98")
    # </editor-fold>

    # <editor-fold desc="Focal Zonal function">
    def SelectFZMixedValueRaster(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Select Raster",
                                                         self.last_dir, "Raster Datasets (*.tif)")
        if fileName != "":
            self.ui.editFZMixedValRas.setText(fileName)
            self.last_dir = fileName

    def SelectFZMixedZoneRaster(self):
        fileName, filetype = QFileDialog.getOpenFileName(self, "Select Raster",
                                                         self.last_dir, "Raster Datasets (*.tif)")
        if fileName != "":
            self.ui.editFZMixedZoneRas.setText(fileName)
            self.last_dir = fileName

    def SaveFZMixedResultRaster(self):
        fileName, filetype = QFileDialog.getSaveFileName(self, "Save Raster",
                                                         self.last_dir, "Raster Datasets (*.tif)")
        if fileName != "":
            self.ui.editFZMixedRstRas.setText(fileName)
            self.last_dir = fileName

    def SetFZMixedStatsPara(self, index):
        if index != 1:
            self.ui.labelFZMixedPercentile.setVisible(False)
            self.ui.editFZMixedPercentile.setVisible(False)
        else:
            self.ui.labelFZMixedPercentile.setVisible(True)
            self.ui.editFZMixedPercentile.setVisible(True)
            self.ui.editFZMixedPercentile.setText("98")

    def SetFZMixedNbhWndPara(self, index):
        if index == 0:
            self.ui.labelFZMixedNbhSet1.setVisible(True)
            self.ui.editFZMixedNbhSet1.setVisible(True)
            self.ui.labelFZMixedNbhSet2.setVisible(True)
            self.ui.editFZMixedNbhSet2.setVisible(True)
            self.ui.labelFZMixedNbhSet3.setVisible(False)
            self.ui.editFZMixedNbhSet3.setVisible(False)

            self.ui.labelFZMixedNbhSet1.setText("Half Length")
            self.ui.editFZMixedNbhSet1.setText("50")
            self.ui.labelFZMixedNbhSet2.setText("Half Width")
            self.ui.editFZMixedNbhSet2.setText("50")
        elif index == 1:
            self.ui.labelFZMixedNbhSet1.setVisible(True)
            self.ui.editFZMixedNbhSet1.setVisible(True)
            self.ui.labelFZMixedNbhSet2.setVisible(False)
            self.ui.editFZMixedNbhSet2.setVisible(False)
            self.ui.labelFZMixedNbhSet3.setVisible(False)
            self.ui.editFZMixedNbhSet3.setVisible(False)

            self.ui.labelFZMixedNbhSet1.setText("Radius")
            self.ui.editFZMixedNbhSet1.setText("50")
        elif index == 2:
            self.ui.labelFZMixedNbhSet1.setVisible(True)
            self.ui.editFZMixedNbhSet1.setVisible(True)
            self.ui.labelFZMixedNbhSet2.setVisible(True)
            self.ui.editFZMixedNbhSet2.setVisible(True)
            self.ui.labelFZMixedNbhSet3.setVisible(True)
            self.ui.editFZMixedNbhSet3.setVisible(True)

            self.ui.labelFZMixedNbhSet1.setText("Semi-major Axis")
            self.ui.editFZMixedNbhSet1.setText("100")
            self.ui.labelFZMixedNbhSet2.setText("Ratio")
            self.ui.editFZMixedNbhSet2.setText("0.5")
            self.ui.labelFZMixedNbhSet3.setText("Angle (°)")
            self.ui.editFZMixedNbhSet3.setText("0")
    # </editor-fold>


    # <editor-fold desc="Get Setting">

    def GetRasterSettings(self, tab_index):
        error_msg = ""
        success_msg = ""

        value_file_name_ui = ""
        zone_file_name_ui = ""
        result_file_name_ui = ""

        if tab_index == 0:
            value_file_name_ui = self.ui.editFocalValRas.text().strip()
            result_file_name_ui = self.ui.editFocalRstRas.text().strip()
        elif tab_index == 1:
            value_file_name_ui = self.ui.editZonalValRas.text().strip()
            zone_file_name_ui = self.ui.editZonalZoneRas.text().strip()
            result_file_name_ui = self.ui.editZonalRstRas.text().strip()
        elif tab_index == 2:
            value_file_name_ui = self.ui.editFZMixedValRas.text().strip()
            zone_file_name_ui = self.ui.editFZMixedZoneRas.text().strip()
            result_file_name_ui = self.ui.editFZMixedRstRas.text().strip()

        value_file_name = None
        zone_file_name = None
        result_file_name = None

        file_exist, message = validate_path(value_file_name_ui)
        if file_exist:
            value_file_name = value_file_name_ui
            success_msg += f"Value Raster: {value_file_name}\n"
        else:
            error_msg += f"Value Raster: {message}"

        if tab_index in [1, 2]:
            file_exist, message = validate_path(zone_file_name_ui)
            if file_exist:
                zone_file_name = zone_file_name_ui
                success_msg += f"Zone Raster: {zone_file_name}\n"
            else:
                error_msg += f"Zone Raster: {message}"

        result_dir = os.path.dirname(result_file_name_ui)
        dir_exist, message = validate_path(result_dir, True)
        if dir_exist:
            result_file_name = result_file_name_ui
            success_msg += f"Result Raster: {result_file_name}\n"
        else:
            error_msg += f"Result Raster: {message}"

        return value_file_name, zone_file_name, result_file_name, error_msg, success_msg

    def GetNeighbourhoodSettings(self, tab_index):
        error_msg = ""
        success_msg = ""

        unit = None
        wnd_type = None
        half_length, half_width = None, None
        radius = None
        semi_majr_length, ratio, angle = None, None, None

        if tab_index in [0, 2]:
            if tab_index == 0:
                if self.ui.rbFocalCell.isChecked():
                    unit_ui = self.ui.rbFocalCell.text()
                else:
                    unit_ui = self.ui.rbFocalMap.text()
                unit = unit_ui
                success_msg += f"Unit: {unit}\n"

                wnd_type_index = self.ui.cbFocalWndType.currentIndex()
                wnd_type = self.ui.cbFocalWndType.currentText()
                success_msg += f"Neighbourhood Window: {wnd_type}\n"

                expected_type = "int"
                if unit == "Map":
                    expected_type = "float"

                if wnd_type_index == 0:
                    half_length_ui = self.ui.editFocalNbhSet1.text()
                    half_width_ui = self.ui.editFocalNbhSet2.text()

                    valid, message = check_variable("Half Length", half_length_ui, expected_type)
                    if valid:
                        half_length = message
                        success_msg += f"Half Length: {half_length}\n"
                    else:
                        error_msg += message

                    valid, message = check_variable("Half Width", half_width_ui, expected_type)
                    if valid:
                        half_width = message
                        success_msg += f"Half Width: {half_width}\n"
                    else:
                        error_msg += message

                elif wnd_type_index == 1:
                    radius_ui = self.ui.editFocalNbhSet1.text()

                    valid, message = check_variable("Radius", radius_ui, expected_type)
                    if valid:
                        radius = message
                        success_msg += f"Radius: {radius}\n"
                    else:
                        error_msg += message

                elif wnd_type_index == 2:

                    semi_majr_length_ui = self.ui.editFocalNbhSet1.text()
                    ratio_ui = self.ui.editFocalNbhSet2.text()
                    angle_ui = self.ui.editFocalNbhSet3.text()

                    valid, message = check_variable("Semi-major length", semi_majr_length_ui, expected_type)
                    if valid:
                        semi_majr_length = message
                        success_msg += f"Semi-major length: {semi_majr_length}\n"
                    else:
                        error_msg += message

                    valid, message = check_variable("Ratio", ratio_ui, "float")
                    if valid:
                        ratio = message
                        success_msg += f"Ratio: {ratio}\n"
                    else:
                        error_msg += message

                    valid, message = check_variable("Angle", angle_ui, "float", True)
                    if valid:
                        angle = message
                        success_msg += f"Angle: {angle}\n"
                    else:
                        error_msg += message

            elif tab_index == 2:
                if self.ui.rbtnFZMixedCell.isChecked():
                    unit_ui = self.ui.rbtnFZMixedCell.text()
                else:
                    unit_ui = self.ui.rbtnFZMixedMap.text()
                unit = unit_ui
                success_msg += f"Unit: {unit}\n"

                wnd_type_index = self.ui.cbFZMixedWndType.currentIndex()
                wnd_type = self.ui.cbFZMixedWndType.currentText()
                success_msg += f"Neighbourhood Window: {wnd_type}\n"

                expected_type = "int"
                if unit == "Map":
                    expected_type = "float"

                if wnd_type_index == 0:
                    half_length_ui = self.ui.editFZMixedNbhSet1.text()
                    half_width_ui = self.ui.editFZMixedNbhSet2.text()

                    valid, message = check_variable("Half Length", half_length_ui, expected_type)
                    if valid:
                        half_length = message
                        success_msg += f"Half Length: {half_length}\n"
                    else:
                        error_msg += message

                    valid, message = check_variable("Half Width", half_width_ui, expected_type)
                    if valid:
                        half_width = message
                        success_msg += f"Half Width: {half_width}\n"
                    else:
                        error_msg += message

                elif wnd_type_index == 1:
                    radius_ui = self.ui.editFZMixedNbhSet1.text()

                    valid, message = check_variable("Radius", radius_ui, expected_type)
                    if valid:
                        radius = message
                        success_msg += f"Radius: {radius}\n"
                    else:
                        error_msg += message

                elif wnd_type_index == 2:
                    semi_majr_length_ui = self.ui.editFZMixedNbhSet1.text()
                    ratio_ui = self.ui.editFZMixedNbhSet2.text()
                    angle_ui = self.ui.editFZMixedNbhSet3.text()

                    valid, message = check_variable("Semi-major length", semi_majr_length_ui, expected_type)
                    if valid:
                        semi_majr_length = message
                        success_msg += f"Semi-major length: {semi_majr_length}\n"
                    else:
                        error_msg += message

                    valid, message = check_variable("Ratio", ratio_ui, "float")
                    if valid:
                        ratio = message
                        success_msg += f"Ratio: {ratio}\n"
                    else:
                        error_msg += message

                    valid, message = check_variable("Angle", angle_ui, "float", True)
                    if valid:
                        angle = message
                        success_msg += f"Angle: {angle}\n"
                    else:
                        error_msg += message

        return unit, wnd_type, half_length, half_width, radius, semi_majr_length, ratio, angle, error_msg, success_msg

    def GetStatisticsSettings(self, tab_index):
        error_msg = ""
        success_msg = ""

        if tab_index == 0:
            stats_type_ui = self.ui.cbFocalStatsType.currentText()
        elif tab_index == 1:
            stats_type_ui = self.ui.cbZonalStatsType.currentText()
        else:
            stats_type_ui = self.ui.cbFZMixedStatsType.currentText()
        stats_type = stats_type_ui
        success_msg += f"Statistics Type: {stats_type}\n"

        percentile = None
        if stats_type_ui == "PERCENTILE":
            if tab_index == 0:
                percentile_ui = self.ui.editFocalPercentile.text()
            elif tab_index == 1:
                percentile_ui = self.ui.editZonalPercentile.text()
            else:
                percentile_ui = self.ui.editFZMixedPercentile.text()

            valid, message = check_percentile(percentile_ui)
            if valid:
                percentile = message
                success_msg += f"Percentile: {percentile}\n"
            else:
                error_msg += message

        return stats_type, percentile, error_msg, success_msg

    def GetAdvancedSettings(self, tab_index):
        error_msg = ""
        success_msg = ""

        data_chunk_ui = ""
        proc_nums_ui = ""
        threshold_ui = ""
        ign_nodata_ui = True
        if tab_index == 0:
            data_chunk_ui = self.ui.editFocalDataChunk.text()
            proc_nums_ui = self.ui.editFocalProcNum.text()
            threshold_ui = self.ui.editFocalThreshold.text()
            ign_nodata_ui = self.ui.cbFocalIgnoreNodata.isChecked()
        elif tab_index == 1:
            threshold_ui = self.ui.editZonalThreshold.text()
            ign_nodata_ui = self.ui.cbZonalIgnoreNodata.isChecked()
        elif tab_index == 2:
            data_chunk_ui = self.ui.editFZMixedDataChunk.text()
            proc_nums_ui = self.ui.editFZMixedProcNum.text()
            threshold_ui = self.ui.editFZMixedThreshold.text()
            ign_nodata_ui = self.ui.cbFZIgnoreNodata.isChecked()

        columns = None
        rows = None
        proc_nums = None
        threshold = None
        is_ign_nodata = ign_nodata_ui

        if tab_index in [0, 2]:
            try:
                columns_str, rows_str = data_chunk_ui.split(",")

                valid, message = check_variable("Columns", columns_str.strip(), "int")
                if valid:
                    columns = message
                    success_msg += f"Columns: {columns}\n"
                else:
                    error_msg += message

                valid, message = check_variable("Rows", rows_str.strip(), "int")
                if valid:
                    rows = message
                    success_msg += f"Rows: {rows}\n"
                else:
                    error_msg += message

            except ValueError:
                error_msg += "Data Chunk: Invalid format\n"


            valid, message = check_variable("Process Number", proc_nums_ui, "int")
            if valid:
                proc_nums = message
                success_msg += f"Process Number: {proc_nums}\n"
            else:
                error_msg += message


        valid, message = check_variable("Threshold", threshold_ui, "int")
        if valid:
            threshold = message
            success_msg += f"Threshold: {threshold}\n"
        else:
            error_msg += message

        return columns, rows, proc_nums, threshold, is_ign_nodata, error_msg, success_msg

    # </editor-fold>


    def ConstructObject(self):
        tab_index = self.ui.tabWidget.currentIndex()
        error_msg = ""
        success_msg = ""

        # <editor-fold desc="Rasters Setting">
        value_file_name, zone_file_name, result_file_name, error_msg_raster, msg_raster = \
            self.GetRasterSettings(tab_index)
        error_msg += error_msg_raster
        success_msg += msg_raster
        # </editor-fold>

        # <editor-fold desc="Neighbourhood Setting">
        unit, wnd_type, half_length, half_width, radius, semi_majr_length, ratio, angle, \
            error_msg_nbh, msg_nbh = self.GetNeighbourhoodSettings(tab_index)
        error_msg += error_msg_nbh
        success_msg += msg_nbh
        # </editor-fold>

        # <editor-fold desc="Statistics Setting">
        stats_type, percentile, error_msg_stats, msg_stats = self.GetStatisticsSettings(tab_index)
        error_msg += error_msg_stats
        success_msg += msg_stats
        # </editor-fold>

        # <editor-fold desc="Advanced Setting">
        div_columns, div_rows, proc_nums, threshold, is_ign_nodata, error_msg_adv, msg_adv = \
            self.GetAdvancedSettings(tab_index)
        error_msg += error_msg_adv
        success_msg += msg_adv
        # </editor-fold>

        stats_method = self.ui.tabWidget.tabText(tab_index)

        if success_msg != "":
            self.printf(success_msg)

        object = None
        if not error_msg:
            object = KDFZObject(value_file_name, zone_file_name, result_file_name,
                                unit,
                                wnd_type,
                                half_length, half_width,
                                radius,
                                semi_majr_length, ratio, angle,
                                stats_type, percentile,
                                div_columns, div_rows, proc_nums, threshold, is_ign_nodata,
                                stats_method)
        else:
            self.printf(error_msg)

        return object



    def AddToConfigFile(self):
        object = self.ConstructObject()
        if object != None:
            write_config(self.config_file_path, object)
            self.printf(f"Object has been appended to {self.config_file_path}\n")

    def OpenConfigFile(self):
        subprocess.run(["notepad", self.config_file_path], shell=True, check=True)

    def RunConfigFile(self):
        run_config(self.config_file_path)

    def Run(self):
        object = self.ConstructObject()
        if object != None:
            process_object(object)

    def Quit(self):
        sys.exit()


if __name__ == '__main__':
    mp.freeze_support()
    myapp = QApplication(sys.argv)
    myDlg = MainDialog()
    myDlg.show()
    sys.exit(myapp.exec_())
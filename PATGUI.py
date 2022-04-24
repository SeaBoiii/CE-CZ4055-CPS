import logging
import sys
from time import time, sleep
from multiprocessing import Pool, cpu_count, freeze_support

import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QRunnable, Qt, QThreadPool
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
                             QMainWindow, QMenu, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QSpinBox, QComboBox,
                             QWidget)

from PAT import getByteKey, print_key

logging.basicConfig(format="%(message)s", level=logging.INFO)


class LoadingProcess(QRunnable):
    def __init__(self, runBtn, plotBtn):
        super().__init__()
        self.runBtn = runBtn
        self.plotBtn = plotBtn

    def run(self):
        btnText = 'Loading'
        count = 0

        global done

        while not done:
            count += 1
            self.runBtn.setText(btnText + ' ' + ('.' * count))

            if count >= 5:
                count = 0

            sleep(1)

        self.runBtn.setText('Analyse')
        self.runBtn.setEnabled(True)
        self.plotBtn.setEnabled(True)


class Runnable(QRunnable):
    def __init__(self, data, no_of_traces, plot_graph, lbl, excludeCtrl, timeElapsedLbl):
        super().__init__()
        self.data = data
        self.no_of_traces = no_of_traces
        self.plot_graph = plot_graph
        self.lbl = lbl
        self.excludeCtrl = excludeCtrl
        self.timeElapsedLbl = timeElapsedLbl

    def run(self):
        '''
        set up parameters required by the task
        '''
        n_processors = cpu_count() - 1
        actual_key_byte = 16
        # 32 to 127 if self.excludeCtrl
        no_of_possible_values_of_key_byte = 95 if self.excludeCtrl else 256
        no_of_power_trace = 2500

        data_arr = self.data[0].to_numpy()
        power_model_matrix = [[]] * no_of_possible_values_of_key_byte
        actual_power_model_matrix = self.data.iloc[:, 2:2502].to_numpy()
        actual_power_model_matrix = np.transpose(
            actual_power_model_matrix[0: self.no_of_traces])

        key_bytes = []
        for i in range(0, actual_key_byte*2, 2):
            process = []
            process.append(i)
            process.append(data_arr)
            process.append(no_of_possible_values_of_key_byte)
            process.append(self.no_of_traces)
            process.append(no_of_power_trace)
            process.append(power_model_matrix)
            process.append(actual_power_model_matrix)
            process.append(self.plot_graph)
            process.append(self.excludeCtrl)
            process.append(True)
            key_bytes.append(process)

        start = time()
        with Pool(n_processors) as pool:
            x = pool.map(getByteKey, key_bytes)

        global raw_key
        global x_index
        global best_correlation_values
        global x1_0
        global best_pos

        raw_key = [i[0] for i in x]
        x_index = [i[1] for i in x]
        best_correlation_values = [i[2] for i in x]
        x1_0 = [i[3] for i in x]
        best_pos = [i[4] for i in x]

        keys = print_key(raw_key, False)
        end = time()

        global hex_key
        global actual_key

        hex_key = str(keys[0])
        actual_key = str(keys[1])

        self.lbl[0].setText(str(keys[0]))
        self.lbl[1].setText(str(keys[1]))
        self.timeElapsedLbl.setText(str(round(end - start, 2)) + ' (s)')

        global done

        done = True


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.excludeCtrl = True

    def setupUi(self):
        self.setWindowTitle("Power Analysis Tool")
        self.setWindowIcon(QIcon('logo.png'))
        self.resize(700, 200)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        self.openAction = QAction(self)
        self.openAction.setText("&Open...")
        self.openAction.triggered.connect(self.openFile)
        self.exitAction = QAction(self)
        self.exitAction.setText("&Exit")
        self.exitAction.triggered.connect(lambda: self.close())

        menuBar = self.menuBar()
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.exitAction)

        self.traceFileLbl = QLabel(
            "File > Open and select a trace file", centralWidget)
        self.traceFileLbl.setFixedHeight(20)

        self.cipherCombo = QComboBox(centralWidget)
        self.cipherCombo.setFixedHeight(20)
        cipher_list = ["AES128"]
        for item in cipher_list:
            self.cipherCombo.addItem(item)

        self.traceCount = QSpinBox(centralWidget)
        self.traceCount.setFixedHeight(20)
        self.traceCount.setRange(2, 100)
        self.traceCount.setValue(100)

        self.bytePosCount = QSpinBox(centralWidget)
        self.bytePosCount.setFixedHeight(20)
        self.bytePosCount.setRange(0, 15)
        self.bytePosCount.setValue(0)

        self.excludeCtrlCB = QCheckBox("Exclude ASCII control characters")
        self.excludeCtrlCB.setChecked(True)
        self.excludeCtrlCB.stateChanged.connect(
            lambda: self.excludeCtrlToggle())

        self.hexKeyLbl = QLabel("", centralWidget)
        self.hexKeyLbl.setFixedHeight(20)

        self.decodedKeyLbl = QLabel("", centralWidget)
        self.decodedKeyLbl.setFixedHeight(20)

        self.timeElapsedLbl = QLabel("", centralWidget)
        self.timeElapsedLbl.setFixedHeight(20)

        self.runBtn = QPushButton("Analyse", centralWidget)
        self.runBtn.setEnabled(False)
        self.runBtn.clicked.connect(self.runTasks)

        self.plotBtn = QPushButton("Show Graph Analysis", centralWidget)
        self.plotBtn.setEnabled(False)
        self.plotBtn.clicked.connect(self.plot_graph)

        self.madeByLbl = QLabel(
            "Made by: \nTeam Snakes (Aleem, Ethel, Fatin, Samuel)", centralWidget)

        self.projLbl = QLabel(
            "NTU CZ4055 Lab Project", centralWidget)
        self.projLbl.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        mainLayout = QVBoxLayout()

        row1Layout = QHBoxLayout()
        row1Layout.addWidget(QLabel("Trace file:"))
        row1Layout.addWidget(self.traceFileLbl)

        row2Layout = QHBoxLayout()
        row2Layout.addWidget(QLabel('Cipher:'))
        row2Layout.addWidget(self.cipherCombo)

        row3Layout = QHBoxLayout()
        row3Layout.addWidget(QLabel('No of traces:'))
        row3Layout.addWidget(self.traceCount)

        row5Layout = QHBoxLayout()
        row5Layout.addWidget(QLabel('Hex Key:'))
        row5Layout.addWidget(self.hexKeyLbl)

        row6Layout = QHBoxLayout()
        row6Layout.addWidget(QLabel('Decoded Key:'))
        row6Layout.addWidget(self.decodedKeyLbl)

        row7Layout = QHBoxLayout()
        row7Layout.addWidget(QLabel('Time Elapsed:'))
        row7Layout.addWidget(self.timeElapsedLbl)

        row8Layout = QHBoxLayout()
        row8Layout.addWidget(QLabel('Byte Position: (0 - 15)'))
        row8Layout.addWidget(self.bytePosCount)
        row8Layout.addWidget(self.plotBtn)

        row9Layout = QHBoxLayout()
        row9Layout.addWidget(self.madeByLbl)
        row9Layout.addWidget(self.projLbl)

        mainLayout.addLayout(row1Layout)
        mainLayout.addLayout(row2Layout)
        mainLayout.addLayout(row3Layout)
        mainLayout.addWidget(self.excludeCtrlCB, 0, Qt.AlignRight)
        mainLayout.addWidget(self.runBtn)
        mainLayout.addLayout(row5Layout)
        mainLayout.addLayout(row6Layout)
        mainLayout.addLayout(row7Layout)
        mainLayout.addLayout(row8Layout)
        mainLayout.addLayout(row9Layout)

        centralWidget.setLayout(mainLayout)

    def runTasks(self):
        global done
        done = False
        self.runBtn.setEnabled(False)
        self.hexKeyLbl.setText("")
        self.decodedKeyLbl.setText("")
        self.timeElapsedLbl.setText("")
        pool = QThreadPool.globalInstance()
        runnable = Runnable(self.data, self.traceCount.value(), False,
                            (self.hexKeyLbl, self.decodedKeyLbl), self.excludeCtrl, self.timeElapsedLbl)
        loadingProcess = LoadingProcess(self.runBtn, self.plotBtn)
        pool.start(runnable)
        pool.start(loadingProcess)

    def plot_graph(self):
        if 'raw_key' in globals():
            global raw_key
            global hex_key
            global actual_key
            global x_index
            global best_correlation_values
            global x1_0
            global best_pos

            position = self.bytePosCount.value()
            split_hex_key = [hex_key[i:i+2] for i in range(0, len(hex_key), 2)]

            plot.figure()
            plot.title(
                f"Correct Key Byte : {raw_key[position]}/{split_hex_key[position]}({actual_key[position]})")
            plot.xlabel('Value of key byte')
            plot.ylabel('Correlation Value')
            plot.plot([i + (32 if self.excludeCtrl else 0)
                      for i in x_index[position]], best_correlation_values[position])
            plot.plot(x1_0[position] + (32 if self.excludeCtrl else 0), best_correlation_values[position]
                      [best_pos[position][0][0]], 'r*')
            plot.show()

    def openFile(self):
        self.fname = QFileDialog.getOpenFileName(
            self, "Open trace file", "", "csv(*.csv)")
        if self.fname[0] != '':
            self.data = pd.read_csv(self.fname[0], header=None)
            self.traceFileLbl.setText(self.fname[0])
            self.runBtn.setEnabled(True)
        else:
            self.data = None
            self.traceFileLbl.setText("")
            self.runBtn.setEnabled(False)

    def excludeCtrlToggle(self):
        self.excludeCtrl = not self.excludeCtrl


if __name__ == "__main__":
    freeze_support()
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import ui_main_1 as ui_main
import heat_machine as hm

class Ui_MainWindow_tagged(ui_main.Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

    def tag_all(self):
        self.Graph_PushButton.clicked.connect(self.handle_graph)

    def handle_graph(self):
        points  = self.get_graph_info()
        fr_coef = int(self.FreedomCoef_LineEdit.text())
        d = hm.Draw(points, fr_coef)
        self.update_info(d.comp)
        d.show()

    def get_graph_info(self):
        points = []
        text = self.PointInput_plainTextEdit.toPlainText()
        for i in text.split('\n'):
            if i:
                t = i.split()
                dp = float(t[0])
                dv = float(t[1])
                t1 = t[2]
                points.append((dp, dv, t1))
        return points

    def update_info(self, com):
        _translate = QtCore.QCoreApplication.translate

        com.remember_calculations()

        self.HeaterHeat_Label.setText(_translate("MainWindow", str(round(com.heater_heat, 2))))
        self.CoolerHeat_Label.setText(_translate("MainWindow", str(round(-com.cooler_heat, 2))))
        self.GasWork_Label.setText(_translate("MainWindow", str(round(com.all_work, 2))))
        self.Coef_Label.setText(_translate("MainWindow", str(round(com.coef*100, 3))))

        info_text = ''

        for i in range(len(com.work)):
            info_text += f'A({(i+1)}-{(i+1)%len(com.work)+1}) = {round(com.work[i], 2)}\n'
        
        info_text += '\n'
        for i in range(len(com.heat)):
            info_text += f'Q({(i+1)}-{(i+1)%len(com.heat)+1}) = {round(com.heat[i], 2)}\n'
        
        info_text += '\n'
        for i in range(len(com.energy)):
            info_text += f'dU({(i+1)}-{(i+1)%len(com.energy)+1}) = {round(com.energy[i], 2)}\n'

        self.ProcessInfo_plainTextEdit.setPlainText(info_text)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_tagged()
    ui.setupUi(MainWindow)
    ui.tag_all()
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
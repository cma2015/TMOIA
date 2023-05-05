# GUI for TMOIA
import sys, os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5.QtCore import QThread, pyqtSignal
#from numpy import unique
#from qt_material import apply_stylesheet
from utils_gui import*
from main import*


class thread_train(QThread):
    #trigger = pyqtSignal(str)
    finished = pyqtSignal()
    def __init__(self, percTst:float, path_saveModel:str, path_trait:str, dict_omics:dict, regr_or_clas:int, classNum:int):
        super().__init__()
        self.percTst = percTst
        self.path_saveModel = path_saveModel
        self.path_trait = path_trait
        self.dict_omics = dict_omics
        self.regr_or_clas = regr_or_clas
        self.classNum = classNum
    def run(self):
        build_model(self.percTst, self.path_saveModel, self.path_trait, self.dict_omics, self.regr_or_clas, self.classNum)
        self.finished.emit()

class thread_pred(QThread):
    #trigger = pyqtSignal(str)
    finished = pyqtSignal()
    def __init__(self, path_save_result:str, path_model:str, dict_omics:dict):
        super().__init__()
        self.path_save_result = path_save_result
        self.path_model = path_model
        self.dict_omics = dict_omics
    def run(self):
        prediction(self.path_save_result, self.path_model, self.dict_omics)
        self.finished.emit()


class mywindow(QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        file_ui = 'tmoia.ui'
        self.ui = uic.loadUi(resource_path(file_ui))

        # Main buttons
        self.ui.pushButton_abort.clicked.connect(self.app_exit)
        self.ui.pushButton_submit.clicked.connect(self.app_submit)
        self.ui.pushButton_reset.clicked.connect(self.app_reset)

        # Tab 1
        ## Click buttons to input and output
        self.ui.toolButton_fopen_1_1.clicked.connect(self.choose_file_trait)
        self.ui.toolButton_fopen_1_2.clicked.connect(self.choose_file_1_om1)
        self.ui.toolButton_fopen_1_3.clicked.connect(self.choose_file_1_om2)
        self.ui.toolButton_fopen_1_4.clicked.connect(self.choose_file_1_om3)
        self.ui.toolButton_fopen_1_5.clicked.connect(self.choose_file_1_om4)
        self.ui.toolButton_fout_1.clicked.connect(self.choose_path_save_model)
        ## slider
        self.ui.horizontalSlider.valueChanged.connect(self.handle_perc_trntst)
        self.ui.lineEdit_trnPerc.textChanged.connect(self.set_slider_percTrn)
        self.ui.lineEdit_tstPerc.textChanged.connect(self.set_slider_percTst)
        ## combobox
        if self.ui.comboBox_modelType.currentIndex() == 0:
            self.ui.lineEdit_classNum.setVisible(False)
        self.ui.comboBox_modelType.currentIndexChanged.connect(self.popUpClassNumber)
        self.ui.lineEdit_classNum.textChanged.connect(self.set_classNum)

        # Tab 2
        ## Click buttons to input and output
        self.ui.toolButton_fopenModel.clicked.connect(self.choose_model)
        self.ui.toolButton_fopen_2_1.clicked.connect(self.choose_file_2_om1)
        self.ui.toolButton_fopen_2_2.clicked.connect(self.choose_file_2_om2)
        self.ui.toolButton_fopen_2_3.clicked.connect(self.choose_file_2_om3)
        self.ui.toolButton_fopen_2_4.clicked.connect(self.choose_file_2_om4)
        self.ui.toolButton_fout_2.clicked.connect(self.choose_file_pred_trait)
        
        # Async
        #self.thread_train = thread_train()
        #self.thread_pred = thread_pred()

        self.ui.show()


    def choose_file_trait(self):
        dialog = QFileDialog(caption="Choose a File of Trait(s)", filter="Trait (*.csv)")
        #dialog.setFileMode(QFileDialog.AnyFile)
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_label.setText(filenames[0])
    def choose_file_1_om1(self):
        dialog = QFileDialog(caption="Choose a Omic File", filter="Omic File (*.csv)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_om_1_1.setText(filenames[0])
    def choose_file_1_om2(self):
        dialog = QFileDialog(caption="Choose a Omic File", filter="Omic File (*.csv)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_om_1_2.setText(filenames[0])
    def choose_file_1_om3(self):
        dialog = QFileDialog(caption="Choose a Omic File", filter="Omic File (*.csv)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_om_1_3.setText(filenames[0])
    def choose_file_1_om4(self):
        dialog = QFileDialog(caption="Choose a Omic File", filter="Omic File (*.csv)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_om_1_4.setText(filenames[0])
    def choose_path_save_model(self):
        dialog = QFileDialog(caption="Save Your Model", filter="Model (*.pth)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_output_1.setText(filenames[0])
        if not self.ui.lineEdit_output_1.text().endswith(".pth"):
            self.ui.lineEdit_output_1.setText(self.ui.lineEdit_output_1.text() + ".pth")
    
    def handle_perc_trntst(self, value):
        self.ui.lineEdit_trnPerc.setText(str(value))
        self.ui.lineEdit_tstPerc.setText(str(100 - value))
    def set_slider_percTrn(self):
        valueT = self.ui.lineEdit_trnPerc.text()
        valueT = "".join([ele for ele in valueT if ele.isdigit()])
        if len(valueT) > 2:
            valueT = "70"
        if len(valueT) < 1:
            valueT = "30"
        self.ui.lineEdit_trnPerc.setText(valueT)
        self.ui.horizontalSlider.setValue(int(valueT))
    def set_slider_percTst(self):
        valueT = self.ui.lineEdit_tstPerc.text()
        valueT = "".join([ele for ele in valueT if ele.isdigit()])
        if len(valueT) > 2:
            valueT = "70"
        if len(valueT) < 1:
            valueT = "30"
        self.ui.lineEdit_tstPerc.setText(valueT)
        self.ui.horizontalSlider.setValue(100 - int(valueT))
    def popUpClassNumber(self):
        if self.ui.comboBox_modelType.currentIndex() == 1:#=classification
            self.ui.lineEdit_classNum.setVisible(True)
            self.ui.textBrowser.append("Please input the number of categories.")
        else:
            self.ui.lineEdit_classNum.setVisible(False)
    def set_classNum(self):
        value_cn = self.ui.lineEdit_classNum.text()
        value_cn = "".join([ele for ele in value_cn if ele.isdigit()])
        self.ui.lineEdit_classNum.setText(value_cn)

    
    def choose_model(self):
        dialog = QFileDialog(caption="Choose a Trained Model", filter="Model (*.pth)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_pathModel.setText(filenames[0])
    def choose_file_2_om1(self):
        dialog = QFileDialog(caption="Choose a Omic File", filter="Omic File (*.csv)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_om_2_1.setText(filenames[0])
    def choose_file_2_om2(self):
        dialog = QFileDialog(caption="Choose a Omic File", filter="Omic File (*.csv)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_om_2_2.setText(filenames[0])
    def choose_file_2_om3(self):
        dialog = QFileDialog(caption="Choose a Omic File", filter="Omic File (*.csv)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_om_2_3.setText(filenames[0])
    def choose_file_2_om4(self):
        dialog = QFileDialog(caption="Choose a Omic File", filter="Omic File (*.csv)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_om_2_4.setText(filenames[0])
    def choose_file_pred_trait(self):
        dialog = QFileDialog(caption="Save Predicted Trait(s)", filter="Trait (*.csv)")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            self.ui.lineEdit_output_2.setText(filenames[0])
        if not self.ui.lineEdit_output_2.text().endswith(".csv"):
            self.ui.lineEdit_output_2.setText(self.ui.lineEdit_output_2.text() + ".csv")


    def set_button_disable(self):
        self.ui.pushButton_submit.setDisabled(True)
        self.ui.pushButton_reset.setDisabled(True)
        self.ui.comboBox_modelType.setDisabled(True)
        self.ui.horizontalSlider.setDisabled(True)
        self.ui.lineEdit_trnPerc.setDisabled(True)
        self.ui.lineEdit_tstPerc.setDisabled(True)
    def set_button_able(self):
        self.ui.pushButton_submit.setDisabled(False)
        self.ui.pushButton_reset.setDisabled(False)
        self.ui.comboBox_modelType.setDisabled(False)
        self.ui.horizontalSlider.setDisabled(False)
        self.ui.lineEdit_trnPerc.setDisabled(False)
        self.ui.lineEdit_tstPerc.setDisabled(False)

    def do_after_trn(self):
        self.ui.textBrowser.append("Model has been saved to " + self.ui.lineEdit_output_1.text())
        self.set_button_able()
        print("Done.\n")
    def do_after_prd(self):
        self.ui.textBrowser.append("Prediction Result has been saved to " + self.ui.lineEdit_output_2.text())
        self.set_button_able()
        print("Done.\n")
    

    def start_train(self):
        # Read inputs
        ## lineEdit
        #percTrn = int(self.ui.lineEdit_trnPerc.text()) / 100
        percTst = int(self.ui.lineEdit_tstPerc.text()) / 100
        path_trait = self.ui.lineEdit_label.text()
        path_omic_1 = self.ui.lineEdit_om_1_1.text()
        path_omic_2 = self.ui.lineEdit_om_1_2.text()
        path_omic_3 = self.ui.lineEdit_om_1_3.text()
        path_omic_4 = self.ui.lineEdit_om_1_4.text()
        path_saveModel = self.ui.lineEdit_output_1.text()
        classNum = self.ui.lineEdit_classNum.text()
        ##
        if ( path_omic_1 == '' ) : self.ui.comboBox_omic_1.setCurrentText('')
        if ( path_omic_2 == '' ) : self.ui.comboBox_omic_2.setCurrentText('')
        if ( path_omic_3 == '' ) : self.ui.comboBox_omic_3.setCurrentText('')
        if ( path_omic_4 == '' ) : self.ui.comboBox_omic_4.setCurrentText('')
        ## comboBox
        modelRegrOrClas = self.ui.comboBox_modelType.currentIndex()
        omic_1 = self.ui.comboBox_omic_1.currentText()
        omic_2 = self.ui.comboBox_omic_2.currentText()
        omic_3 = self.ui.comboBox_omic_3.currentText()
        omic_4 = self.ui.comboBox_omic_4.currentText()

        # Detect inputs
        ## Check omics
        dict_omics = check_omics([path_omic_1, path_omic_2, path_omic_3, path_omic_4], [omic_1, omic_2, omic_3, omic_4])
        if dict_omics == False:
            self.ui.textBrowser.append("ERROR: Omics collision.")
            return 0
        else:
            path_omics_list = list(dict_omics.values())
            #name_omics = list(dict_omics)
        ## If files exist
        paths_in = path_omics_list + [path_trait]
        isOK = 1
        for xxpath in paths_in:
            if not os.path.exists(xxpath):
                isOK = 0
        if len(path_saveModel) < 2:
            isOK = 0
        if len(classNum) < 1:
            classNum = 0
        classNum = int(classNum)
        if modelRegrOrClas == 1 and classNum < 2:
            isOK = 0
        if isOK == 0:
            self.ui.textBrowser.append("ERROR: Blank input.")
            return 0
        
        ## If add suffix
        if not path_saveModel.endswith(".pth"):
            path_saveModel = path_saveModel + ".pth"
            self.ui.lineEdit_output_1.setText(path_saveModel)
        ## Can the model be saved?
        if not ifCanBeSaved(path_saveModel):
            self.ui.textBrowser.append("ERROR: The Model cannot be saved to the specified path.")
            return 0
        
        # Run core - TRAIN
        self.ui.textBrowser.append("Imported files: " + str(dict_omics))
        self.ui.textBrowser.append("Training...")
        self.thread_train = thread_train(percTst, path_saveModel, path_trait, dict_omics, modelRegrOrClas, classNum)
        self.set_button_disable()
        self.thread_train.start()
        ## Done
        self.thread_train.finished.connect(self.do_after_trn)
        
    

    def start_predict(self):
        # Read inputs
        ## lineEdit
        path_model = self.ui.lineEdit_pathModel.text()
        path_omic_1 = self.ui.lineEdit_om_2_1.text()
        path_omic_2 = self.ui.lineEdit_om_2_2.text()
        path_omic_3 = self.ui.lineEdit_om_2_3.text()
        path_omic_4 = self.ui.lineEdit_om_2_4.text()
        path_prediction = self.ui.lineEdit_output_2.text()
        ##
        if ( path_omic_1 == '' ) : self.ui.comboBox_omic_2_1.setCurrentText('')
        if ( path_omic_2 == '' ) : self.ui.comboBox_omic_2_2.setCurrentText('')
        if ( path_omic_3 == '' ) : self.ui.comboBox_omic_2_3.setCurrentText('')
        if ( path_omic_4 == '' ) : self.ui.comboBox_omic_2_4.setCurrentText('')
        ## comboBox
        omic_1 = self.ui.comboBox_omic_2_1.currentText()
        omic_2 = self.ui.comboBox_omic_2_2.currentText()
        omic_3 = self.ui.comboBox_omic_2_3.currentText()
        omic_4 = self.ui.comboBox_omic_2_4.currentText()
        ## checkBox
        #isOurModel = self.ui.checkBox.isChecked()

        # Detect inputs
        ## Check omics
        dict_omics = check_omics([path_omic_1, path_omic_2, path_omic_3, path_omic_4], [omic_1, omic_2, omic_3, omic_4])
        if dict_omics == False:
            self.ui.textBrowser.append("ERROR: Omics collision.")
            return 0
        else:
            path_omics_list = list(dict_omics.values())
        ## If files exist
        paths_in = path_omics_list + [path_model]
        isOK = 1
        for xxpath in paths_in:
            if not os.path.exists(xxpath):
                isOK = 0
        if len(path_prediction) < 3:
            isOK = 0
        if isOK == 0:
            self.ui.textBrowser.append("ERROR: Blank input.")
            return 0
        ## If add suffix
        if not path_prediction.endswith(".csv"):
            path_prediction = path_prediction + ".csv"
            self.ui.lineEdit_output_2.setText(path_prediction)
        ## Can the result be saved?
        if not ifCanBeSaved(path_prediction):
            self.ui.textBrowser.append("ERROR: The Prediction Result cannot be saved to the specified path.")
            return 0
        
        # Run core - PREDICT
        self.ui.textBrowser.append("Imported files: " + str(dict_omics))
        self.ui.textBrowser.append("Predicting...")
        self.thread_pred = thread_pred(path_prediction, path_model, dict_omics)
        self.set_button_disable()
        self.thread_pred.start()
        ## Done
        self.thread_pred.finished.connect(self.do_after_prd)
    
    
    def reset_tab1(self):
        self.ui.lineEdit_trnPerc.clear()
        self.ui.lineEdit_tstPerc.clear()
        self.ui.lineEdit_label.clear()
        self.ui.lineEdit_om_1_1.clear()
        self.ui.lineEdit_om_1_2.clear()
        self.ui.lineEdit_om_1_3.clear()
        self.ui.lineEdit_om_1_4.clear()
        self.ui.lineEdit_output_1.clear()
        self.ui.lineEdit_classNum.clear()
        self.ui.comboBox_modelType.setCurrentIndex(0)
        self.ui.comboBox_omic_1.setCurrentIndex(0)
        self.ui.comboBox_omic_2.setCurrentIndex(0)
        self.ui.comboBox_omic_3.setCurrentIndex(0)
        self.ui.comboBox_omic_4.setCurrentIndex(0)
    def reset_tab2(self):
        self.ui.lineEdit_pathModel.clear()
        self.ui.lineEdit_om_2_1.clear()
        self.ui.lineEdit_om_2_2.clear()
        self.ui.lineEdit_om_2_3.clear()
        self.ui.lineEdit_om_2_4.clear()
        self.ui.lineEdit_output_2.clear()
        self.ui.comboBox_omic_2_1.setCurrentIndex(0)
        self.ui.comboBox_omic_2_2.setCurrentIndex(0)
        self.ui.comboBox_omic_2_3.setCurrentIndex(0)
        self.ui.comboBox_omic_2_4.setCurrentIndex(0)
        #self.ui.checkBox.setChecked(False)

    def app_submit(self):
        if self.ui.tabWidget.currentIndex() == 0:
            self.start_train()
        else:
            self.start_predict()
    def app_reset(self):
        self.ui.textBrowser.clear()
        if self.ui.tabWidget.currentIndex() == 0:
            self.reset_tab1()
        else:
            self.reset_tab2()
    def app_exit(self):
        exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    #apply_stylesheet(app, theme='dark_cyan.xml')
    appwindow = mywindow()
    sys.exit(app.exec())


#pyuic5 -o tmoia_ui.py tmoia.ui
#pyuic5.exe -o .\tmoia_ui.py .\tmoia.ui

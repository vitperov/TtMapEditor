from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton
from functools import partial

class ChooseModelDlg(QDialog):
    def __init__(self, objCollection, category, parent=None):
        super(ChooseModelDlg, self).__init__(parent)
        self.setWindowTitle("Choose Model")
        self.selectedModel = None
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        availableObjects = objCollection.getTypesInCategory(category)
        
        for model in availableObjects:
            btn = QPushButton(f"Model {model}")
            btn.clicked.connect(partial(self.onButtonClicked, model))
            layout.addWidget(btn)
    
    def onButtonClicked(self, model):
        self.selectedModel = model
        self.accept()

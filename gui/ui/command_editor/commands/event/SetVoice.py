from PySide6 import QtWidgets, QtGui, QtCore


class SetVoiceUI(QtWidgets.QWidget):
    def __init__(self):
        super(SetVoiceUI, self).__init__()

        self.form_layout = QtWidgets.QFormLayout()
        self.setLayout(self.form_layout)

        self.voice_clip = QtWidgets.QSpinBox()
        self.voice_clip.setMaximum(65536)
        self.form_layout.addRow("Voice Clip", self.voice_clip)

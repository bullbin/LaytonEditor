from gui.ui.event.command.CharacterShakeCommand import CharacterShakeCommandUI
from .CommandEditor import CommandEditor
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore
from gui.SettingsManager import SettingsManager


class CharacterShakeCommand(CommandEditor, CharacterShakeCommandUI):
    def set_command(self, command: GDSCommand, event: Event):
        super(CharacterShakeCommand, self).set_command(command, event)
        settings = SettingsManager()

        for i, char_id in enumerate(self.event.characters):
            if char_id == 0:
                break
            char_name = settings.character_id_to_name[char_id]
            self.character.addItem(f"{char_name}: {char_id}", i)
        self.character.setCurrentIndex(command.params[0])

        self.duration.setValue(command.params[1])

    def save(self):
        self.command.params = [
            self.character.currentData(QtCore.Qt.ItemDataRole.UserRole),
            self.duration.value()
        ]

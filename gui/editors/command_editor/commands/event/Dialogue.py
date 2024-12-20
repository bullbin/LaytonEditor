from gui.ui.command_editor.commands.event.Dialogue import DialogueUI
from ..CommandEditor import CommandEditorEvent
from formats.gds import GDSCommand
from formats.event import Event
from PySide6 import QtCore
from gui.SettingsManager import SettingsManager
from utility.replace_substitutions import replace_substitutions, convert_substitutions


class Dialogue(CommandEditorEvent, DialogueUI):
    def set_command(self, command: GDSCommand, event: Event = None, **kwargs):
        super(Dialogue, self).set_command(command, event=event, **kwargs)
        text_num = command.params[0]
        text = event.get_text(text_num)
        settings = SettingsManager()

        self.character.addItem("Narrator", 0)
        index = 0
        for i, char_id in enumerate(event.characters):
            if char_id == 0:
                break
            char_name = SettingsManager().character_id_to_name.get(char_id, f"Unnamed {char_id}")
            self.character.addItem(f"{char_name}: {char_id}", char_id)
            if char_id == text.params[0]:
                index = i + 1
        self.character.setCurrentIndex(index)

        self.start_anim.setText(text.params[1])
        self.end_anim.setText(text.params[2])
        self.pitch.setValue(text.params[3])

        text = replace_substitutions(text.params[4])
        self.text.setPlainText(text)

    def save(self):
        text_num = self.command.params[0]
        text = self.event.get_text(text_num)
        text.params[0] = self.character.currentData(QtCore.Qt.ItemDataRole.UserRole)
        text.params[1] = self.start_anim.text()
        text.params[2] = self.end_anim.text()
        text.params[3] = self.pitch.value()
        text.params[4] = convert_substitutions(self.text.toPlainText())

from PySide6 import QtWidgets, QtGui, QtCore
from formats.event import Event
from formats.gds import GDS, GDSCommand


class CommandListModel(QtCore.QAbstractListModel):
    def __init__(self):
        super(CommandListModel, self).__init__()
        self._event: [Event] = None

    def set_event(self, event):
        self.layoutAboutToBeChanged.emit()
        self._event = event
        self.layoutChanged.emit()

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        if parent.isValid():
            return 0
        return len(self._event.gds.commands)

    def data(self, index: QtCore.QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        command: GDSCommand = self._event.gds.commands[index.row()]
        if role == QtCore.Qt.ItemDataRole.DisplayRole:
            return self.parse_command(command) + "\n"
        elif role == QtCore.Qt.ItemDataRole.UserRole:
            return command
        return None

    def parse_command(self, command: GDSCommand):
        if command.command in [0x2, 0x3, 0x32, 0x33, 0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:  # fade
            fade_in = command.command in [0x2, 0x32, 0x80, 0x81, 0x88]
            fade_time = None
            fade_screens = 0
            if command.command in [0x2, 0x3, 0x72, 0x80]:
                fade_screens = 2  # both screens
            elif command.command in [0x32, 0x33, 0x7f, 0x81]:
                fade_screens = 0  # btm screen
            elif command.command in [0x87, 0x88]:
                fade_screens = 1  # top screen
            if command.command in [0x72, 0x7f, 0x80, 0x81, 0x87, 0x88]:
                fade_time = command.params[0]  # timed

            screens = {
                0: "Bottom screen",
                1: "Top screen",
                2: "Both screens"
            }[fade_screens]

            duration = "Default frames" if fade_time is None else f"{fade_time} frames"

            return f"Fade {'In' if fade_in else 'Out'}\n" \
                   f"{screens} ({duration})"
        elif command.command in [0x5, 0x8, 0x9, 0xb]:
            mode = {
                0x5: "Place",
                0x8: "Movie",
                0x9: "Event",
                0xb: "Puzzle"
            }[command.command]
            return f"Set Mode ID\n" \
                   f"{mode} to {command.params[0]}"
        elif command.command in [0x6, 0x7]:
            return f"{'Next Mode' if command.command is 0x6 else 'Queue Following Mode'}\n" \
                   f"Mode: {command.params[0]}"
        elif command.command in [0x31, 0x69, 0x6c]:
            if command.command == 0x31:
                line = f"{command.params[0]} Frames"
            elif command.command == 0x69:
                line = f"Tap"
            else:
                line = f"Tap or {command.params[0]} Frames"
            return f"Wait {line}"
        elif command.command in [0x21, 0x22]:
            return f"Load {'Bottom' if command.command == 0x21 else 'Top'} Background\n" \
                   f"{command.params[0]}"
        elif command.command in [0x2a, 0x2b, 0x2c]:
            if command.command in [0x2a, 0x2b]:
                show = command.command == 0x2a
            else:
                show = command.params[1] > 0
            alpha = "" if command.command != 0x2c else ' (alpha)'
            return f"Character {command.params[0]} Visibility\n" \
                   f"{'Show' if show else 'Hide'}{alpha}"
        else:
            return f"Command {hex(command.command)}\n" \
                   f"Parameters: {command.params}"

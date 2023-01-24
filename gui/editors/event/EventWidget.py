import logging

from gui.ui.event.EventWidget import EventWidgetUI
from formats.event import Event
from formats_parsed.EventDCC import EventDCC
from formats_parsed.EventScript import EventScript

from previewers.event.EventPlayer import EventPlayer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gui.MainEditor import MainEditor


from .EventPropertiesWidget import EventPropertiesWidget
from PySide6 import QtCore
from gui.editor_categories.Events import EventCategory, EventNode


class EventEditor(EventWidgetUI):
    def __init__(self, main_editor):
        super(EventEditor, self).__init__()
        self.event = None
        self.event_node: QtCore.QModelIndex = None
        self.main_editor: MainEditor = main_editor

    def get_event_properties_widget(self):
        return EventPropertiesWidget(self)

    def set_event(self, ev: Event, ev_index: QtCore.QModelIndex):
        self.event = ev
        self.event_node = ev_index
        self.character_widget.set_event(ev)
        dcc_text = EventDCC(ev)
        serialized = dcc_text.serialize(include_character=False)
        self.text_editor.setPlainText(serialized)

    def preview_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = EventDCC(self.event).parse(text, include_character=False)
        if is_ok:
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        else:
            logging.error(f"Error compiling DCC: {error}")

    def save_dcc_btn_click(self):
        text = self.text_editor.toPlainText()
        is_ok, error = EventDCC(self.event).parse(text, include_character=False)
        if is_ok:
            self.event.save_to_rom()
            event_node: EventNode = self.event_node.internalPointer()
            category: EventCategory = event_node.category
            category.load_event_names()
            self.main_editor.tree_model.dataChanged.emit(self.event_node, self.event_node)
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
        else:
            logging.error(f"Error compiling DCC: {error}")

    def preview_ev_script_btn_click(self):
        text = self.text_editor.toPlainText()
        try:
            ev_script = EventScript(text, self.event)
            ev_script.parse()
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
            self.character_widget.set_event(self.event)
        except Exception as e:
            logging.error(f"Error compiling EventScript: {e}")

    def save_ev_script_btn_click(self):
        text = self.text_editor.toPlainText()
        try:
            ev_script = EventScript(text, self.event)
            ev_script.parse()
            self.event.save_to_rom()
            self.main_editor.pg_previewer.start_renderer(EventPlayer(self.event))
            self.character_widget.set_event(self.event)
        except Exception as e:
            logging.error(f"Error compiling EventScript: {e}")

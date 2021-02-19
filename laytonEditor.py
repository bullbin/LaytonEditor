import sys

import wx

from gui import MainEditor

print(f"Layton Editor running in python version {sys.version}")


class LaytonEditor(wx.App):
    editor: MainEditor

    def OnInit(self):
        self.editor = MainEditor(None)
        self.editor.Show(True)
        return True


def main():
    app = LaytonEditor(None)
    app.editor.open_rom("../Base File.nds")
    app.MainLoop()


if __name__ == '__main__':
    main()

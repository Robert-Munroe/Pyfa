import wx

import eos.db
import gui.mainFrame
from gui import globalEvents as GE
from gui.fitCommands.calc.cart.add import CalcAddCartCommand
from gui.fitCommands.helpers import CargoInfo, InternalCommandHistory
from service.market import Market


class GuiAddCartCommand(wx.Command):

    def __init__(self, fitID, itemID, amount):
        wx.Command.__init__(self, True, 'Add Cart')
        self.internalHistory = InternalCommandHistory()
        self.fitID = fitID
        self.itemID = itemID
        self.amount = amount

    def Do(self):
        cmd = CalcAddCartCommand(fitID=self.fitID, cartInfo=CargoInfo(itemID=self.itemID, amount=self.amount))
        success = self.internalHistory.submit(cmd)
        Market.getInstance().storeRecentlyUsed(self.itemID)
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

    def Undo(self):
        success = self.internalHistory.undoAll()
        eos.db.commit()
        wx.PostEvent(gui.mainFrame.MainFrame.getInstance(), GE.FitChanged(fitIDs=(self.fitID,)))
        return success

from openpilot.common.params import Params
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.widgets import Widget
from openpilot.system.ui.widgets.list_view import toggle_item
from openpilot.system.ui.widgets.scroller_tici import Scroller
from openpilot.system.ui.widgets.confirm_dialog import ConfirmDialog
from openpilot.system.ui.lib.application import gui_app
from openpilot.system.ui.lib.multilang import tr, tr_noop
from openpilot.system.ui.widgets import DialogResult
from bleak import BleakScanner


class CustomLayout(Widget):
  def __init__(self):
    super().__init__()
    self._params = Params()
    self._is_release = self._params.get_bool("IsReleaseBranch")

    # Build items and keep references for callbacks/state updates
    self._scan_button = button_item(
      lambda: tr("Scan Bluetooth"),
      description=lambda: tr("SCAN"),
      callback=self._on_scan,
    )

    def _on_scan(self):
      try:
        devices = await BleakScanner.discover(timeout=4.0)
        for device in devices:
          # Do whatever
        return devices
      except Exception as e:
        print("Bluetooth scan failed: {e}")
        return []

    self._scroller = Scroller([
      self._scan_button,
    ], line_separator=True, spacing=0)

  def _render(self, rect):
    self._scroller.render(rect)

  def show_event(self):
    super().show_event()
    self._scroller.show_event()
    self._update_toggles()

  def _update_toggles(self):
    ui_state.update_params()

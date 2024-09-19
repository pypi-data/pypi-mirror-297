from typing import cast

from glue_qt.app import GlueApplication
from glue_vispy_viewers.volume.qt.volume_viewer import VispyVolumeViewer
from qtpy.QtGui import QDoubleValidator, QIntValidator
from qtpy.QtWidgets import QCheckBox, QLabel, QLineEdit

from glue_ar.common.tests.test_base_dialog import BaseExportDialogTest, DummyState
from glue_ar.common.scatter_export_options import ARVispyScatterExportOptions
from glue_ar.qt.export_dialog import QtARExportDialog
from glue_ar.qt.tests.utils import combobox_options


class TestQtExportDialog(BaseExportDialogTest):

    app: GlueApplication
    dialog: QtARExportDialog

    def setup_method(self, method):
        self.app = GlueApplication()
        self._setup_data()

        # We use a volume viewer because it can support both volume and scatter layers
        self.viewer: VispyVolumeViewer = cast(VispyVolumeViewer,
                                              self.app.new_data_viewer(VispyVolumeViewer, data=self.volume_data))
        self.viewer.add_data(self.scatter_data)

        self.dialog = QtARExportDialog(parent=self.viewer, viewer=self.viewer)
        self.dialog.show()

    def teardown_method(self, method):
        self.dialog.close()

    def test_default_ui(self):
        ui = self.dialog.ui
        assert ui.button_cancel.isVisible()
        assert ui.button_ok.isVisible()
        assert ui.combosel_compression.isVisible()
        assert ui.label_compression_message.isVisible()

        compression_options = combobox_options(ui.combosel_compression)
        assert compression_options == ["None", "Draco", "Meshoptimizer"]

    def test_filetype_change(self):
        state = self.dialog.state
        ui = self.dialog.ui

        state.filetype = "USDC"
        assert not ui.combosel_compression.isVisible()
        assert not ui.label_compression_message.isVisible()

        state.filetype = "USDA"
        assert not ui.combosel_compression.isVisible()
        assert not ui.label_compression_message.isVisible()

        state.filetype = "glTF"
        assert ui.combosel_compression.isVisible()
        assert ui.label_compression_message.isVisible()

        state.filetype = "USDA"
        assert not ui.combosel_compression.isVisible()
        assert not ui.label_compression_message.isVisible()

        state.filetype = "glB"
        assert ui.combosel_compression.isVisible()
        assert ui.label_compression_message.isVisible()

        state.filetype = "glTF"
        assert ui.combosel_compression.isVisible()
        assert ui.label_compression_message.isVisible()

    def test_widgets_for_property(self):
        state = DummyState()

        int_widgets = self.dialog._widgets_for_property(state, "cb_int", "Int CB")
        assert len(int_widgets) == 2
        label, edit = int_widgets
        assert isinstance(label, QLabel)
        assert label.text() == "Int CB:"
        assert isinstance(edit, QLineEdit)
        assert isinstance(edit.validator(), QIntValidator)
        assert edit.text() == "0"

        float_widgets = self.dialog._widgets_for_property(state, "cb_float", "Float CB")
        assert len(float_widgets) == 2
        label, edit = float_widgets
        assert isinstance(label, QLabel)
        assert label.text() == "Float CB:"
        assert isinstance(edit, QLineEdit)
        assert isinstance(edit.validator(), QDoubleValidator)
        assert edit.text() == "1.7"

        bool_widgets = self.dialog._widgets_for_property(state, "cb_bool", "Bool CB")
        assert len(bool_widgets) == 1
        box = bool_widgets[0]
        assert isinstance(box, QCheckBox)
        assert box.text() == "Bool CB"
        assert not box.isChecked()

    def test_update_layer_ui(self):
        state = DummyState()
        self.dialog._update_layer_ui(state)
        assert self.dialog.ui.layer_layout.rowCount() == 3

        state = ARVispyScatterExportOptions()
        self.dialog._update_layer_ui(state)
        assert self.dialog.ui.layer_layout.rowCount() == 2

    def test_clear_layout(self):
        self.dialog._clear_layer_layout()
        assert self.dialog.ui.layer_layout.isEmpty()
        assert self.dialog._layer_connections == []

    def test_layer_change_ui(self):
        state = self.dialog.state
        ui = self.dialog.ui

        state.layer = "Scatter Data"
        assert ui.combosel_method.currentText() == state.method
        assert combobox_options(ui.combosel_method) == ["Scatter"]
        assert not ui.label_method.isVisible()
        assert not ui.combosel_method.isVisible()

        state.layer = "Volume Data"
        assert set(combobox_options(ui.combosel_method)) == {"Isosurface", "Voxel"}
        assert ui.combosel_method.currentText() == state.method
        assert ui.label_method.isVisible()
        assert ui.combosel_method.isVisible()

        state.layer = "Scatter Data"
        assert ui.combosel_method.currentText() == state.method
        assert combobox_options(ui.combosel_method) == ["Scatter"]
        assert not ui.label_method.isVisible()
        assert not ui.combosel_method.isVisible()

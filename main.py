import threading
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from jnius import autoclass

Context = autoclass('android.content.Context')
UsbManager = autoclass('android.hardware.usb.UsbManager')
PythonActivity = autoclass('org.kivy.android.PythonActivity')


class Interface(FloatLayout):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self.add_widget(self.spinner)
        self.usb_manager = None
        self.setup_usb_manager()

    def setup_usb_manager(self):
        activity = PythonActivity.mActivity
        self.usb_manager = activity.getSystemService(Context.USB_SERVICE)

    def update_usb_devices(self):
        device_list = self.usb_manager.getDeviceList().values()
        device_names = [device.getDeviceName() for device in device_list]
        if device_names:
            self.ids.usb_spinner.values = device_names
        else:
            self.ids.usb_spinner.values = ('No USB Device Detected',)


class ProjectApp(App):
    def build(self):
        return Interface()


ProjectApp().run()

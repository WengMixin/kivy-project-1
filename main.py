from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass

Context = autoclass('android.content.Context')
UsbManager = autoclass('android.hardware.usb.UsbManager')
UsbDevice = autoclass('android.hardware.usb.UsbDevice')


class SerialApp(App):
    def build(self):
        usb_manager = UsbManager.getSystemService(Context.USB_SERVICE)
        usb_device_list = usb_manager.getDeviceList()
        label_text = 'Connected USB Devices:\n' + \
            '\n'.join(usb_device_list.keys())
        self.root.ids.usb_label.text = label_text


if __name__ == '__main__':
    SerialApp().run()

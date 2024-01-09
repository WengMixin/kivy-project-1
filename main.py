import threading
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from pyudev import Context, Monitor, MonitorObserver


class Interface(FloatLayout):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self.spinner = Spinner(
            text='USB Devices',
            values=('No USB Device Detected',),
            size_hint=(None, None),
            size=(100, 44),
            pos_hint={'center_x': .5, 'center_y': .5})
        self.add_widget(self.spinner)

    def update_usb_devices(self, action, device):
        if device.device_type == 'usb_device':
            if action == 'add':
                print("USB Device Connected.")
                self.ids.label.text = "USB Device Detected."
                # Update the spinner values
                self.ids.usb_spinner.values = (device.device_node,)
            elif action == 'remove':
                print("USB Device Disconnected.")
                self.ids.label.text = "USB Device Disconnected."
                self.ids.usb_spinner.values = ('No USB Device Detected',)

     def display_error(self, error):
        self.ids.label.text = "Error: " + str(error)

    def safe_update_usb_devices(self, action, device):
        try:
            self.update_usb_devices(action, device)
        except Exception as e:
            error = traceback.format_exc()
            print(error)  # 打印错误到控制台
            self.display_error(error)  # 显示错误信息到 UI

    def display_information(self):
        data = self.ids.textInput.text
        self.ids.label.text = data


class ProjectApp(App):
    def build(self):
        interface = Interface()
        # Set up USB monitoring in a separate thread
        context = Context()
        monitor = Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb')
        observer = MonitorObserver(
            monitor, callback=interface.safe_update_usb_devices)  # 使用包装后的方法
        usb_thread = threading.Thread(target=observer.start)
        usb_thread.daemon = True
        usb_thread.start()
        return interface


ProjectApp().run()

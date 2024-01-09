import traceback
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from jnius import autoclass, JavaException

# Android 类的引用
Context = autoclass('android.content.Context')
UsbManager = autoclass('android.hardware.usb.UsbManager')
PythonActivity = autoclass('org.kivy.android.PythonActivity')


class Interface(FloatLayout):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)
        self.usb_manager = None
        self.setup_usb_manager()

    def setup_usb_manager(self):
        try:
            activity = PythonActivity.mActivity
            self.usb_manager = activity.getSystemService(Context.USB_SERVICE)
            self.update_usb_devices()  # 更新 USB 设备列表
        except JavaException as je:
            print("set-up-Java Exception: ", je)
            print("set-up-Java Exception Traceback: ",
                  traceback.format_exc())
            # 在这里处理 Java 层面的异常
        except Exception as e:
            print("setup-Exception: ", e)
            print("setup-Exception Traceback: ", traceback.format_exc())
            # 在这里处理 Python 层面的异常

    def update_usb_devices(self):
        try:
            device_list = self.usb_manager.getDeviceList().values()
            device_names = [device.getDeviceName() for device in device_list]
            if device_names:
                self.ids.usb_spinner.values = device_names
            else:
                self.ids.usb_spinner.values = ('No USB Device Detected',)
        except JavaException as je:
            print("Update_Java Exception: ", je)
            print("Update_Java Exception Traceback: ", traceback.format_exc())
            # 在这里处理 Java 层面的异常
        except Exception as e:
            print("Update_func_Exception: ", e)
            print("Update_func_Exception Traceback: ", traceback.format_exc())
            # 在这里处理 Python 层面的异常


class ProjectApp(App):
    def build(self):
        return Interface()


ProjectApp().run()

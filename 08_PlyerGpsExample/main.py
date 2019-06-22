from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import Clock, mainthread

from android.permissions import request_permission, Permission, check_permission

kv = '''
BoxLayout:
    orientation: 'vertical'

    Label:
        text: app.gps_location

    Label:
        text: app.gps_status

    BoxLayout:
        size_hint_y: None
        height: '48dp'
        padding: '4dp'

        ToggleButton:
            text: 'Start' if self.state == 'normal' else 'Stop'
            on_state:
                app.start(1000, 0) if self.state == 'down' else \
                app.stop()
'''


class GpsTest(App):

    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')

    def build(self):
        try:
            if not check_permission('android.permission.ACCESS_FINE_LOCATION'):
                print('Permission Fine Location Access: %s' % str(check_permission('android.permission.ACCESS_FINE_LOCATION')))
                request_permission('android.permission.ACCESS_FINE_LOCATION')
            else:
                print('Fine Location Access Permission OK')

            if not check_permission(Permission.ACCESS_COARSE_LOCATION):
                print('Permission Coarse Location Access: %s' % str(check_permission(Permission.ACCESS_COARSE_LOCATION)))
                request_permission(Permission.ACCESS_COARSE_LOCATION)
            else:
                print('Coarse Location Access Permission OK')

            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            print('GPS is not implemented for your platform')
            self.gps_status = 'GPS is not implemented for your platform'

        return Builder.load_string(kv)

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(1000, 0)
        pass


if __name__ == '__main__':
    GpsTest().run()

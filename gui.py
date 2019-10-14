from microsmycentral import MicrosMycentral
from preferences import Preferences
import rumps, json, requests


class PreferencePane(rumps.Window):

    def __init__(self):
        super(PreferencePane, self).__init__(title="Preferences", cancel=True)
        self.message = "You can modify the below configuration using JSON."
        self.default_text = str(json.dumps(Preferences().config,
                                           sort_keys=True,
                                           indent=4,
                                           separators=(',', ': ')
                                           ))


class About(rumps.Window):

    def __init__(self):
        super(About, self).__init__(title="About")
        self.default_text = str("Version: 1.0.3\nAuthor: Christian D. Tuen")


class Password(rumps.Window):

    def __init__(self):
        super(Password, self).__init__(title="Password", cancel=True, dimensions=(295, 20))
        self.default_text = str("*****************")


class StatusBarApp(rumps.App):

    def __init__(self):
        super(StatusBarApp, self).__init__("-- kr")
        try:
            self.preferences = Preferences()
            self.mmc = MicrosMycentral()
        except requests.exceptions.ReadTimeout:
            rumps.alert("Not able to connect to lunch portal, please check the application preferences.")
        except Exception, e:
            rumps.alert(str(e.message))

    @rumps.clicked("Preferences")
    def prefs(self, _):
        response = PreferencePane().run()
        requirements = ['email', 'interval']
        if response.clicked == 1:
            try:
                user_configuration = json.loads(str(response.text))
                if not all(requirement in user_configuration for requirement in requirements):
                    raise ValueError('You are missing required properties in the JSON configuration.')
                self.preferences.configuration = user_configuration
                self.preferences.write_config()
                self.refresh(_)
            except Exception, e:
                rumps.alert(str(e.message))

    @rumps.clicked("Password")
    def password(self, _):
        response = Password().run()
        if response.clicked == 1:
            self.preferences.password = str(response.text)
            self.refresh(_)

    @rumps.clicked("Refresh")
    def refresh(self, _):
        self.preferences = Preferences()
        self.mmc = MicrosMycentral()
        self.balance_updater(_)

    @rumps.clicked("About")
    def about(self, _):
        About().run()

    @rumps.timer(Preferences().interval)
    def balance_updater(self, _):
        self.mmc.initiate_session()
        self.mmc.post_credentials(self.preferences.username, self.preferences.password)
        usage = self.mmc.get_current_balance()
        if usage == -1:
            usage = "--"
        new_title = "{0:.2f}".format(usage)
        if self.preferences.show_currency:
            new_title += " kr"
        self.title = new_title


if __name__ == "__main__":
    StatusBarApp().run()

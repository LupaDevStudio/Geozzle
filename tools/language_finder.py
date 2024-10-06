from kivy.utils import platform


if platform == "android":
    from android import autoclass
    LanguageFinder = autoclass('org.org.kivyreview.LanguageFinder')

    def find_device_language(*_):
        language = LanguageFinder.get_device_language()
        print(language)
        return language
else:

    def find_device_language(*_):
        print("Language finder is only available on Android devices.")
        return "en"

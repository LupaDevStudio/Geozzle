from kivy.utils import platform


if platform == "android":
    from android import PythonJavaClass, autoclass, java_method, mActivity

    context = mActivity.getApplicationContext()
    LanguageFinder = autoclass('org.org.language_finder.LanguageFinder')

    def find_device_language(*_):
        language_finder = LanguageFinder()
        language_finder.get_device_language()
        language = language_finder.language
        print(language)
        return language
else:

    def find_device_language(*_):
        print("Language finder is only available on Android devices.")
        return "en"

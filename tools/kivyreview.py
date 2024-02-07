from kivy.utils import platform


if platform == "android":
    from android import PythonJavaClass, autoclass, java_method, mActivity
    from android.runnable import run_on_ui_thread

    context = mActivity.getApplicationContext()
    YourReviewHandler = autoclass('org.org.kivyreview.ReviewHandler')
    PythonActivity = autoclass('org.kivy.android.PythonActivity')

    def request_review(*_):
        activity = PythonActivity.mActivity
        review_handler = YourReviewHandler(activity)
        review_handler.requestReview()
else:
    def request_review(*_):
        print("In app review is only possible on android devices.")

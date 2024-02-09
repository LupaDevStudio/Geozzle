package org.org.kivyreview;

import android.app.Activity;
import com.google.android.play.core.review.ReviewInfo;
import com.google.android.play.core.review.ReviewManager;
import com.google.android.play.core.tasks.Task;

public class ReviewHandler {

    private Activity mActivity;
    private ReviewManager mReviewManager;

    public ReviewHandler(Activity activity) {
        mActivity = activity;
        mReviewManager = com.google.android.play.core.review.ReviewManagerFactory.create(mActivity);
    }

    public void requestReview() {
        Task<ReviewInfo> request = mReviewManager.requestReviewFlow();
        request.addOnCompleteListener(task -> {
            if (task.isSuccessful()) {
                ReviewInfo reviewInfo = task.getResult();
                launchReviewFlow(reviewInfo);
            } else {
                // Handle error when requesting review flow
                // For example, show a fallback review prompt
                showFallbackReviewPrompt();
            }
        });
    }

    private void launchReviewFlow(ReviewInfo reviewInfo) {
        Task<Void> flow = mReviewManager.launchReviewFlow(mActivity, reviewInfo);
        flow.addOnCompleteListener(task -> {
            // Review flow launched, handle success or failure here
            // For example, log completion or show a thank you message
        });
    }

    private void showFallbackReviewPrompt() {
        // Fallback mechanism to ask for user feedback or redirect to the Play Store for
        // review
        // You can implement a custom dialog or redirect the user to the app's Play
        // Store page
    }
}
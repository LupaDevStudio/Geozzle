package org.org.language_finder;

import android.content.res.Resources;
import androidx.core.os.ConfigurationCompat;
import androidx.core.os.LocaleListCompat;

public class LanguageFinder {

    private String language;

    private void get_device_language() {
        LocaleListCompat locales = ConfigurationCompat.getLocales(Resources.getSystem().getConfiguration());
        if (!locales.isEmpty()) {
            language = locales.get(0).getLanguage();  // Getting the first locale's language
        }
    }
}

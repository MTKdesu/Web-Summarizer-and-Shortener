package com.bluewind.shorturl.common.util;

import java.util.regex.Pattern;


 //URL校验

public class UrlUtils {
    private static final Pattern URL_REG = Pattern.compile("^(((ht|f)tps?):\\/\\/)?[\\w-]+(\\.[\\w-]+)+([\\w.,@?^=%&:/~+#-]*[\\w@?^=%&/~+#-])?$");

    public static boolean checkURL(String url) {
        return URL_REG.matcher(url).matches();
    }
}

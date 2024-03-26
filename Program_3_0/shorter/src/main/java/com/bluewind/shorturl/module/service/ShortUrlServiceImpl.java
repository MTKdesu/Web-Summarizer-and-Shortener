package com.bluewind.shorturl.module.service;

import com.bluewind.shorturl.common.util.HashUtils;
import com.bluewind.shorturl.module.dao.ShortUrlDaoImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

/**
 * @reference https://juejin.cn/post/6844904090602848270?share_token=4ba00e67-783a-496a-9b49-fe5cb9b1a4c9
 **/
@Service
public class ShortUrlServiceImpl {
    @Autowired
    private ShortUrlDaoImpl shortUrlDao;



    public  String  getOriginalUrlByShortUrl(String shortURL) {

        List<Map<String, Object>> result = shortUrlDao.queryListByshortURL(shortURL);
        String originalURL = "";
        if (result != null && !result.isEmpty()) {
            originalURL = result.get(0).get("lurl") == null ? null : (String) result.get(0).get("lurl");
            return originalURL;
        } else {
            return null;
        }
    }



   // 生成的短链

    public String saveUrlMap(String originalURL) {
        String tempURL = originalURL;
        String shortURL = HashUtils.hashToBase62(tempURL);

        shortUrlDao.insertOne(shortURL, originalURL);


        return shortURL;


    }

}
package com.bluewind.shorturl.module.controller;

import com.bluewind.shorturl.common.base.Result;
import com.bluewind.shorturl.common.util.UrlUtils;
import com.bluewind.shorturl.module.service.ShortUrlServiceImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.net.InetAddress;
import java.net.UnknownHostException;

@RestController
public class ShortUrlApiController {

    @Autowired
    private ShortUrlServiceImpl shortUrlServiceImpl;

    @Autowired
    private Environment env;
    //curl -X POST http://localhost:8076/api/generate -d "originalUrl=https://translate.google.com/?sl=en&tl=zh-CN&op=translate"
    // 新增一个API端点用于生成短链接
    @PostMapping("/api/generate")
    public Result generateShortUrlApi(@RequestParam String originalUrl) throws UnknownHostException {
        if (UrlUtils.checkURL(originalUrl)) {
            String shortURL = shortUrlServiceImpl.saveUrlMap(originalUrl);
            String host = "http://" + InetAddress.getLocalHost().getHostAddress() + ":"
                    + env.getProperty("server.port")
                    + "/";
                // 这里直接返回Result对象，Spring Boot会自动将其序列化为JSON
            return Result.ok("请求成功", host + shortURL);
        } else {
            return Result.error("请输入正确的网址链接，注意以http://或https://开头");
        }
    }

    // 你可以继续添加其他API端点...
}

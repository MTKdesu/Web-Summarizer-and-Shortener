package com.bluewind.shorturl.module.controller;

import com.bluewind.shorturl.common.base.Result;
import com.bluewind.shorturl.common.util.UrlUtils;
import com.bluewind.shorturl.module.service.ShortUrlServiceImpl;
import com.jfinal.plugin.activerecord.Db;
import com.jfinal.plugin.activerecord.Record;
import com.jfinal.plugin.activerecord.SqlPara;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.List;


@Controller
public class ShortUrlController {

    @Autowired
    private ShortUrlServiceImpl shortUrlServiceImpl;

    @Autowired
    private Environment env;


    @GetMapping("/")
    public String index() {
        return "index";
    }


    @GetMapping("/notFound")
    public String notFound() {
        return "not_found";
    }


    @GetMapping("/expirePage")
    public String expirePage() {
        return "expire_page";
    }

    @PostMapping("/generate")
    @ResponseBody
    public Result generateShortURL(@RequestParam String originalUrl,
                                   @RequestParam(required = false, defaultValue = "sevenday", value = "validityPeriod") String validityPeriod) throws UnknownHostException {
        if (UrlUtils.checkURL(originalUrl)) {
            String shortURL = shortUrlServiceImpl.saveUrlMap(originalUrl);
            String host = "http://" + InetAddress.getLocalHost().getHostAddress() + ":"
                    + env.getProperty("server.port")
                    + "/";
            return Result.ok("请求成功", host + shortURL);
        }
        return Result.error("请输入正确的网址链接，注意以http://或https://开头");
    }


    @GetMapping("/{shortURL}")
    public String redirect(@PathVariable String shortURL) {
        // 根据断链，获取原始url
        String originalURL = shortUrlServiceImpl.getOriginalUrlByShortUrl(shortURL);
        if (originalURL != null && !originalURL.isEmpty()) {
                    return "redirect:" + originalURL;
                }
        else {
            // 没有对应的原始链接，则直接返回404页
            return "redirect:/notFound";
        }
    }


    @GetMapping("/activeRecordTest")
    @ResponseBody
    public Object activeRecordTest() {
        SqlPara sqlPara = Db.getSqlPara("user.getAllList", new HashMap());
        List<Record> applyList2 = Db.find(sqlPara);
        return  Result.ok("测试成功", applyList2);
    }

}

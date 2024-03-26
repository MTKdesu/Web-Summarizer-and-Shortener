package com.bluewind.shorturl.module.dao;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Map;

@Repository
public class ShortUrlDaoImpl {

    @Autowired
    private JdbcTemplate jdbcTemplate;


    public List<Map<String, Object>> queryListByshortURL(String shortURL) {
        String sql = "select lurl from url_map where surl = ?";
        List<Map<String, Object>> result = jdbcTemplate.queryForList(sql, shortURL);
        return result;
    }

    //使用ignore确保了当输入相同的长网址后，不会因为数据库里已经存在当前网址而报错
    public int insertOne(String shortURL, String originalURL) {
        String sql = "INSERT IGNORE INTO url_map (surl, lurl) VALUES (?, ?)";
        return jdbcTemplate.update(sql, shortURL, originalURL);
    }
}

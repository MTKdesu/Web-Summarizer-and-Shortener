package com.bluewind.shorturl.module.controller;

import com.bluewind.shorturl.common.base.Result;
import com.bluewind.shorturl.summarize.WebPageSummarizer;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class SummarizerController {

    @Autowired
    private WebPageSummarizer webPageSummarizer;

    @Value("${openai.api.key}")
    private String apiKey;

    @GetMapping("/summarize")
    public String summarize() {
        return "summarize"; // 返回初始HTML表单页面
    }

    @PostMapping("/summary")
    public String summarizeWebPage(@RequestParam("url") String url,
                                   @RequestParam("level") int summarizationLevel, Model model) {
        try {
            String webPageContent = WebPageSummarizer.fetchWebPageContent(url);
            String summary = WebPageSummarizer.summarizeTextWithOpenAI(webPageContent, apiKey, summarizationLevel);
            model.addAttribute("summary", summary);
            return "summary"; // 返回包含概括内容的视图名称
        } catch (Exception e) {
            model.addAttribute("error", "概括失败，请重试。");
            return "error"; // 返回错误页面的视图名称
        }
    }
}

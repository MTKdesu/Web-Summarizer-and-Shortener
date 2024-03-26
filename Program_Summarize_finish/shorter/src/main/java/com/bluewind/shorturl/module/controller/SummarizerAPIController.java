package com.bluewind.shorturl.module.controller;

import com.bluewind.shorturl.common.base.Result;
import com.bluewind.shorturl.summarize.WebPageSummarizer;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.io.IOException;

@RestController
@RequestMapping("/api")
public class SummarizerAPIController {
//这个controller实现了别人访问咱们的api中summarize的功能
    @Value("${openai.api.key}")
    private String apiKey;

    //curl "http://localhost:8076/api/summarize?url=https://www.cosc.brocku.ca/~efoxwell/3P97/URL&summarizationLevel=100"

    @GetMapping("/summarize")
    public Result summarizeWebPage(@RequestParam String url, @RequestParam(defaultValue = "100") int summarizationLevel) {
        try {
            String webPageContent = WebPageSummarizer.fetchWebPageContent(url);
            String summary = WebPageSummarizer.summarizeTextWithOpenAI(webPageContent, apiKey, summarizationLevel);
            return Result.ok("Summarization succeeded", summary);
        } catch (IOException | InterruptedException e) {
            return Result.error("Summarization failed");
        }
    }
}

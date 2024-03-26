package com.bluewind.shorturl.summarize;


import java.io.IOException;

public class WebPageSummarizerTest {

    public static void main(String[] args) {
        // 替换以下字符串为你的OpenAI API密钥
        String apiKey = "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";
        // 设置想要概括的网页地址
        String webPageUrl = "https://www.cosc.brocku.ca/~efoxwell/3P97/";
        // 设置输出的长度（token为单位）
        int summarizationLevel=60;
        try {
            // 抓取网页内容
            String content = WebPageSummarizer.fetchWebPageContent(webPageUrl);
            // 使用OpenAI概括文本
            String summary = WebPageSummarizer.summarizeTextWithOpenAI(content, apiKey,summarizationLevel);

            // 打印概括
            System.out.println("Summary: " + summary);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
    }
}

package com.bluewind.shorturl.summarize;

import org.json.JSONObject;
import org.springframework.stereotype.Service;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.io.IOException;

@Service

public class WebPageSummarizer {

    private static final HttpClient httpClient = HttpClient.newHttpClient();

    public static String fetchWebPageContent(String webPageUrl) throws IOException, InterruptedException {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(webPageUrl))
                .GET()
                .build();

        HttpResponse<String> response = httpClient.send(request, BodyHandlers.ofString());

        return response.body();
    }

    public static String summarizeTextWithOpenAI(String text, String apiKey,int summarizationLevel) throws IOException, InterruptedException {
        // 使用JSONObject构建请求体，自动处理特殊字符
        JSONObject json = new JSONObject();
        json.put("prompt", "Summarize this: " + text);
        json.put("max_tokens",summarizationLevel );//定义缩放程度
        json.put("temperature", 0.7);
        json.put("model", "gpt-3.5-turbo-instruct");

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.openai.com/v1/completions"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + apiKey)
                .POST(HttpRequest.BodyPublishers.ofString(json.toString()))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        return response.body();
    }
}

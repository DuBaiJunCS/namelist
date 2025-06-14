/*
 * Copyright (C) 2025 ankio(ankio@ankio.net)
 * Licensed under the Apache License, Version 3.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *         http://www.apache.org/licenses/LICENSE-3.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *   limitations under the License.
 */

package net.ankio.auto.request;


import okhttp3.*;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class GetAnonymousSession {

    public static Map<String, String> getAnonymousSession() {
        String url = "https://ncnjv3qw5wjd.feishu.cn/share/base/view/shrcn0T0NcS3UyFsOAMJqZ9GoeS";

        final Map<String, String> cookieStore = new HashMap<>();

        CookieJar cookieJar = new CookieJar() {
            @Override
            public void saveFromResponse(HttpUrl url, List<Cookie> cookies) {
                for (Cookie cookie : cookies) {
                    cookieStore.put(cookie.name(), cookie.value());
                }
            }

            @Override
            public List<Cookie> loadForRequest(HttpUrl url) {
                return List.of(); // 不需要发送 Cookie
            }
        };

        OkHttpClient client = new OkHttpClient.Builder()
                .cookieJar(cookieJar)
                .followRedirects(true)
                .build();

        Request request = new Request.Builder()
                .url(url)
                .header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0")
                .header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
                .header("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2")
                .header("DNT", "1")
                .header("Sec-GPC", "1")
                .header("Connection", "keep-alive")
                .header("Upgrade-Insecure-Requests", "1")
                .header("Sec-Fetch-Dest", "document")
                .header("Sec-Fetch-Mode", "navigate")
                .header("Sec-Fetch-Site", "none")
                .header("Sec-Fetch-User", "?1")
                .header("Priority", "u=0, i")
                .header("Pragma", "no-cache")
                .header("Cache-Control", "no-cache")
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                System.out.println("请求失败: " + response.code());
                return Map.of();
            }
            return cookieStore;
        } catch (IOException e) {
            System.out.println("请求失败: " + e);
            return Map.of();
        }
    }

    public static void main(String[] args) {
        Map<String, String> cookies = getAnonymousSession();
        System.out.println(cookies);
    }
}


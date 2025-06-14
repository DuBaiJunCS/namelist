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

import com.google.gson.*;
import okhttp3.*;

import java.io.IOException;
import java.util.*;

public class FetchRecords {

    public static List<Map.Entry<String, String>> fetchRecordsSync(Map<String, String> customCookies) {
        List<Map.Entry<String, String>> resultList = new ArrayList<>();

        OkHttpClient client = new OkHttpClient.Builder()
                .cookieJar(new CookieJar() {
                    @Override
                    public void saveFromResponse(HttpUrl url, List<Cookie> cookies) {}

                    @Override
                    public List<Cookie> loadForRequest(HttpUrl url) {
                        List<Cookie> list = new ArrayList<>();
                        for (Map.Entry<String, String> entry : customCookies.entrySet()) {
                            list.add(new Cookie.Builder()
                                    .name(entry.getKey())
                                    .value(entry.getValue())
                                    .domain("cits7vio8b.feishu.cn")
                                    .build());
                        }
                        return list;
                    }
                })
                .build();

        HttpUrl url = new HttpUrl.Builder()
                .scheme("https")
                .host("cits7vio8b.feishu.cn")
                .addPathSegments("space/api/bitable/external/view/share/records_and_meta")
                .addQueryParameter("shareToken", "shrcn0T0NcS3UyFsOAMJqZ9GoeS")
                .build();

        Request request = new Request.Builder()
                .url(url)
                .headers(new Headers.Builder()
                        .add("authority", "cits7vio8b.feishu.cn")
                        .add("accept", "application/json, text/plain, */*")
                        .add("accept-language", "zh-CN,zh;q=0.9")
                        .add("f-version", "docs-6-3-1748932565147")
                        .add("referer", "https://cits7vio8b.feishu.cn/share/base/view/shrcn0T0NcS3UyFsOAMJqZ9GoeS")
                        .add("sec-ch-ua", "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"")
                        .add("sec-ch-ua-mobile", "?0")
                        .add("sec-ch-ua-platform", "\"Windows\"")
                        .add("sec-fetch-dest", "empty")
                        .add("sec-fetch-mode", "cors")
                        .add("sec-fetch-site", "same-origin")
                        .add("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
                        .build())
                .get()
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                System.out.println("响应失败: " + response.code());
                return resultList;
            }

            String bodyStr = response.body() != null ? response.body().string() : "";
            JsonObject root = JsonParser.parseString(bodyStr).getAsJsonObject();

            if (root.get("code").getAsInt() != 0) {
                System.out.println("响应失败，code不为0");
                return resultList;
            }

            JsonObject data = root.getAsJsonObject("data");
            String snapshotStr = data.get("snapshot").getAsString();
            JsonObject snapshotJson = JsonParser.parseString(snapshotStr).getAsJsonObject();

            JsonObject fieldMap = snapshotJson.has("fieldMap") ? snapshotJson.getAsJsonObject("fieldMap") : new JsonObject();
            String name1FieldName = "fldQa0uO5U";
            String name2FieldName = "fldpe0gtNe";

            for (Map.Entry<String, JsonElement> entry : fieldMap.entrySet()) {
                JsonObject fieldItem = entry.getValue().getAsJsonObject();
                String name = fieldItem.has("name") ? fieldItem.get("name").getAsString() : null;
                if ("name1".equals(name)) {
                    name1FieldName = entry.getKey();
                } else if ("name2".equals(name)) {
                    name2FieldName = entry.getKey();
                }
            }

            JsonObject viewShareEntity = snapshotJson.getAsJsonObject("viewShareEntity");
            JsonObject recordMap = viewShareEntity.getAsJsonObject("recordMap");

            for (Map.Entry<String, JsonElement> recordEntry : recordMap.entrySet()) {
                JsonObject recordObj = recordEntry.getValue().getAsJsonObject();
                if (recordObj == null) continue;

                JsonObject name1Item = recordObj.has(name1FieldName) ? recordObj.getAsJsonObject(name1FieldName) : null;
                JsonObject name2Item = recordObj.has(name2FieldName) ? recordObj.getAsJsonObject(name2FieldName) : null;

                if (name1Item == null || name2Item == null) continue;

                JsonElement name1Value = name1Item.get("value");
                JsonElement name2Value = name2Item.get("value");

                if (name1Value == null || name1Value.isJsonNull() || name2Value == null || name2Value.isJsonNull())
                    continue;

                JsonArray name1Array = name1Value.isJsonArray() ? name1Value.getAsJsonArray() : null;
                JsonArray name2Array = name2Value.isJsonArray() ? name2Value.getAsJsonArray() : null;

                if (name1Array != null && name2Array != null && name1Array.size() > 0 && name2Array.size() > 0) {
                    String mac = name1Array.get(0).getAsJsonObject().get("text").getAsString();
                    String accode = name2Array.get(0).getAsJsonObject().get("text").getAsString();

                    if (!mac.isBlank() && !accode.isBlank()) {
                        resultList.add(new AbstractMap.SimpleEntry<>(mac, accode));
                    }
                }
            }

        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("解析JSON失败: " + e.getMessage());
        }

        return resultList;
    }

    public static void main(String[] args) {
        Map<String, String> cookies = GetAnonymousSession.getAnonymousSession();
        List<Map.Entry<String, String>> records = fetchRecordsSync(cookies);
        for (Map.Entry<String, String> entry : records) {
            System.out.println(entry.getKey() + " " + entry.getValue());
        }
    }
}

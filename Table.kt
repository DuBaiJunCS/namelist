package net.ankio.auto.request

import okhttp3.*
import java.io.IOException

fun getAnonymousSession(): Map<String, String> {
    val url = "https://ncnjv3qw5wjd.feishu.cn/share/base/view/shrcn0T0NcS3UyFsOAMJqZ9GoeS"
//    var sessionValueByCookie="";

    val cookieJar = object : CookieJar {
         val cookieStore = mutableMapOf<String, String>()

        override fun saveFromResponse(url: HttpUrl, cookies: List<Cookie>) {
            for (cookie in cookies) {
                cookieStore[cookie.name]=cookie.value
            }
        }

        override fun loadForRequest(url: HttpUrl): List<Cookie> {
            return  emptyList()
        }
    }

    val client = OkHttpClient.Builder()
        .cookieJar(cookieJar)   // 自动管理 Cookie
        .followRedirects(true)  // 默认就是 true，可以显式写出
        .build()

    val request = Request.Builder()
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
        .build()

    return try {
        client.newCall(request).execute().use { response ->
            if (!response.isSuccessful) {
                println("请求失败: ${response.code}")
                return emptyMap()
            }
            cookieJar.cookieStore
        }
    } catch (e: IOException) {
        println("请求失败: $e")
        emptyMap()
    }
}

// 简单测试
fun main() {
    var c=getAnonymousSession()
    println(c)
}

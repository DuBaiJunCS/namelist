import com.google.gson.JsonObject
import com.google.gson.JsonParser
import net.ankio.auto.request.getAnonymousSession
import okhttp3.*

fun fetchRecordsSync(customCookies: Map<String, String>): List<Pair<String, String>> {
    val client = OkHttpClient.Builder()
        .cookieJar(object : CookieJar {
            override fun saveFromResponse(url: HttpUrl, cookies: List<Cookie>) {}
            override fun loadForRequest(url: HttpUrl): List<Cookie> {
                return customCookies.map { (name, value) ->
                    Cookie.Builder()
                        .name(name)
                        .value(value)
                        .domain("cits7vio8b.feishu.cn")
                        .build()
                }
            }
        })
        .build()

    val urlBuilder = HttpUrl.Builder()
        .scheme("https")
        .host("cits7vio8b.feishu.cn")
        .addPathSegments("space/api/bitable/external/view/share/records_and_meta")
        .addQueryParameter("shareToken", "shrcn0T0NcS3UyFsOAMJqZ9GoeS")

    val request = Request.Builder()
        .url(urlBuilder.build())
        .headers(
            Headers.Builder()
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
                .build()
        )
        .get()
        .build()

    val resultList = mutableListOf<Pair<String, String>>() // 保存 mac 和 accode

    client.newCall(request).execute().use { response ->
        if (!response.isSuccessful) {
            println("响应失败: ${response.code}")
            return@use
        }

        val bodyStr = response.body?.string() ?: ""
        try {
            val root = JsonParser.parseString(bodyStr).asJsonObject

            if (root.get("code")?.asInt != 0) {
                println("响应失败，code不为0")
                return@use
            }

            val data = root.getAsJsonObject("data")
            val snapshotStr = data.get("snapshot")?.asString ?: return@use
            val snapshotJson = JsonParser.parseString(snapshotStr).asJsonObject

            val fieldMap = snapshotJson.getAsJsonObject("fieldMap") ?: JsonObject()
            var name1FieldName = "fldQa0uO5U"
            var name2FieldName = "fldpe0gtNe"

            for ((key, value) in fieldMap.entrySet()) {
                val fieldItem = value.asJsonObject
                val name = fieldItem.get("name")?.asString
                if (name == "name1") name1FieldName = key
                if (name == "name2") name2FieldName = key
            }

            val viewShareEntity = snapshotJson.getAsJsonObject("viewShareEntity") ?: return@use
            val recordMap = viewShareEntity.getAsJsonObject("recordMap") ?: return@use

            for ((_, recordItem) in recordMap.entrySet()) {
                val recordObj = recordItem.asJsonObject
                if (recordObj==null){
                    continue
                }
                val name1Item: JsonObject? = recordObj.getAsJsonObject(name1FieldName) ?: continue
                var  name1Value= name1Item?.get("value") ?: continue
                if (name1Value.isJsonNull){
                    continue
                }

                val name2Item: JsonObject? = recordObj.getAsJsonObject(name2FieldName) ?: continue
                var  name2Value = name2Item?.get("value") ?: continue

                if (name2Value.isJsonNull){
                    continue
                }

                val name1Array = name1Value.takeIf { it.isJsonArray }?.asJsonArray
                val name2Array = name2Value.takeIf { it.isJsonArray }?.asJsonArray

                if (name1Array != null && name1Array.size() > 0 &&
                    name2Array != null && name2Array.size() > 0) {

                    val mac = name1Array[0].asJsonObject.get("text")?.asString ?: ""
                    val accode = name2Array[0].asJsonObject.get("text")?.asString ?: ""

                    if (mac.isNotBlank() && accode.isNotBlank()) {
                        resultList.add(mac to accode)
                    }
                }
            }

        } catch (e: Exception) {
            e.printStackTrace()
            println("解析JSON失败: $e")
            println(bodyStr)
            return@use
        }
    }

    return resultList
}

fun main() {
    val customCookies = getAnonymousSession()
    val records = fetchRecordsSync(customCookies)
    for ((mac, code) in records) {
        println("$mac $code")
    }
}

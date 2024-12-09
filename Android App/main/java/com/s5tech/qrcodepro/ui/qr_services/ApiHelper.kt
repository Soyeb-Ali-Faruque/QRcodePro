import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import okhttp3.*
import org.json.JSONObject
import java.io.IOException
import java.util.concurrent.TimeUnit
import android.util.Base64
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody

class ApiHelper {

    fun sendApiRequest(map: Map<String, String>): Bitmap? {

        var qrCodeBitmap: Bitmap? = null

        val client = OkHttpClient.Builder()
            .connectTimeout(15, TimeUnit.SECONDS)
            .readTimeout(15, TimeUnit.SECONDS)
            .build()

        // Create JSON request body
        val jsonBody = JSONObject()
        for ((key, value) in map) {
            jsonBody.put(key, value)
        }

        val requestBody = jsonBody.toString()
            .toRequestBody("application/json; charset=utf-8".toMediaType())

        val request = Request.Builder()
            .url("https://soyebalifaruque.pythonanywhere.com/qrcodepro/api/generate-qr/")
            .post(requestBody)
            .build()



        client.newCall(request).execute().use { response ->
            if (response.isSuccessful) {
                response.body?.let { responseBody ->
                    val responseString = responseBody.string()
                    val jsonResponse = JSONObject(responseString)
                    if (jsonResponse.getString("status") == "success") {
                        val qrCodeBase64 = jsonResponse.getString("qr_code")
                        // Decode the Base64 string into a Bitmap
                        val decodedBytes = Base64.decode(qrCodeBase64, Base64.DEFAULT)
                        qrCodeBitmap = BitmapFactory.decodeByteArray(decodedBytes, 0, decodedBytes.size)                    }
                }
            }
        }

        return qrCodeBitmap
    }
}

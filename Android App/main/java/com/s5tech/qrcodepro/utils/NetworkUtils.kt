package com.s5tech.qrcodepro.utils

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build

// Step 1: Create a singleton object
object NetworkUtils {

    // Step 2: Define the function to check internet connectivity
    fun isInternetAvailable(context: Context): Boolean {
        // Step 3: Get the ConnectivityManager from the system services
        val connectivityManager = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager

        // Step 4: Check for internet connectivity based on API levels
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            // Step 5: For Android Marshmallow and above, use NetworkCapabilities
            val network = connectivityManager.activeNetwork ?: return false
            val activeNetwork = connectivityManager.getNetworkCapabilities(network) ?: return false

            // Step 6: Check if the network has valid transport types
            return when {
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> true
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> true
                activeNetwork.hasTransport(NetworkCapabilities.TRANSPORT_ETHERNET) -> true
                else -> false
            }
        } else {
            // Step 7: For older devices, use the deprecated activeNetworkInfo
            @Suppress("DEPRECATION")
            val networkInfo = connectivityManager.activeNetworkInfo
            @Suppress("DEPRECATION")
            return networkInfo != null && networkInfo.isConnected
        }
    }
}

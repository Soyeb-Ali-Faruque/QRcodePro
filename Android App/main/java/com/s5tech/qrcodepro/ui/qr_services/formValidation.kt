package com.s5tech.qrcodepro.ui.qr_services

import android.util.Log
import android.util.Patterns
import com.google.i18n.phonenumbers.PhoneNumberUtil
import com.google.i18n.phonenumbers.Phonenumber

class FormValidation {

    private val phoneUtil: PhoneNumberUtil = PhoneNumberUtil.getInstance()

    /**
     * Validates a phone number using Google's libphonenumber library.
     *
     * @param countryCode The country code in "+91" format.
     * @param phoneNumber The phone number as a string.
     * @return `true` if the phone number is valid, `false` otherwise.
     */
    fun isValidPhoneNumber(countryCode: String, phoneNumber: String): Boolean {
        return try {
            val regionCode = getRegionCodeForCountryCode(countryCode)
            val parsedNumber = phoneUtil.parse(phoneNumber, regionCode)
            phoneUtil.isValidNumber(parsedNumber)
        } catch (e: Exception) {
            Log.e("FormValidation", "Error validating phone number: ${e.message}")
            false
        }
    }

    /**
     * Converts a country code (e.g., "+91") to a region code (e.g., "IN").
     *
     * @param countryCode The country code in "+91" format.
     * @return The region code as a string.
     */
    private fun getRegionCodeForCountryCode(countryCode: String): String {
        return try {
            val numericCountryCode = countryCode.replace("+", "").toInt()
            phoneUtil.getRegionCodeForCountryCode(numericCountryCode)
        } catch (e: Exception) {
            Log.e("FormValidation", "Error converting country code: ${e.message}")
            ""
        }
    }


//email validation
    fun isValidEmail(email: String): Boolean {
        // Use a regex pattern for email validation
        val emailPattern = "[a-zA-Z0-9._-]+@[a-z]+\\.+[a-z]+"
        return email.matches(emailPattern.toRegex())
    }


    //URl validation
    fun isValidUrl(url: String): Boolean {
        // Check if the URL matches the WEB_URL pattern
        return Patterns.WEB_URL.matcher(url).matches()
    }
}

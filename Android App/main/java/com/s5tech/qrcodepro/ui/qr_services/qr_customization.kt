package com.s5tech.qrcodepro.ui.qr_services

import android.content.Context
import android.net.Uri
import android.util.Base64
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.ActivityResultLauncher
import androidx.activity.result.contract.ActivityResultContracts
import androidx.fragment.app.Fragment
import com.afollestad.materialdialogs.MaterialDialog
import com.afollestad.materialdialogs.color.colorChooser
import java.io.ByteArrayOutputStream
import java.io.InputStream

class qr_customization {

    private var encodedImage: String? = null
    private lateinit var pickImageLauncher: ActivityResultLauncher<String>



    /**
     * Opens a color picker dialog, updates the TextView with the selected color,
     * and provides the hex value via a callback.
     */
    fun openColorPickerDialog(
        context: Context,
        title: String,
        initialColor: Int,
        textView: TextView,
        onHexColorSelected: (String) -> Unit
    ) {
        MaterialDialog(context).show {
            title(text = title)
            colorChooser(
                colors = intArrayOf(
                    0xFF000000.toInt(), // Black
                    0xFFFFFF00.toInt(), // Yellow
                    0xFF00FF00.toInt(), // Green
                    0xFFFF0000.toInt()  // Red
                ),
                initialSelection = initialColor,
                showAlphaSelector = true,
                allowCustomArgb = true
            ) { _, selectedColor ->
                // Convert the selected color to hex
                val selectedHexColor = String.format("#%06X", (0xFFFFFF and selectedColor))

                // Update the TextView with the selected color and hex value
                textView.setTextColor(selectedColor)
                textView.text = "$title: $selectedHexColor"

                // Return the hex color via callback
                onHexColorSelected(selectedHexColor)
            }
        }
    }


    // Method to initialize the image picker launcher
    fun initializeImagePicker(fragment: Fragment, onImagePicked: (String?) -> Unit) {
        pickImageLauncher =
            fragment.registerForActivityResult(ActivityResultContracts.GetContent()) { uri: Uri? ->
                if (uri != null) {
                    try {
                        // Convert image to Base64
                        val encodedImage = encodeImageToBase64(fragment.requireContext(), uri)
                        if (encodedImage != null) {

                            onImagePicked(encodedImage) // Return the encoded image through the callback
                        }
                    } catch (e: Exception) {
                        Toast.makeText(
                            fragment.requireContext(),
                            "Error processing image: ${e.localizedMessage}",
                            Toast.LENGTH_SHORT
                        ).show()
                    }
                } else {
                    Toast.makeText(
                        fragment.requireContext(),
                        "No image selected",
                        Toast.LENGTH_SHORT
                    )
                        .show()
                }
            }
    }
    // Method to launch the image picker
    fun launchImagePicker() {
        pickImageLauncher.launch("image/*")
    }
    // Function to encode the image to Base64
    private fun encodeImageToBase64(context: Context, uri: Uri): String? {
        try {
            val inputStream: InputStream? = context.contentResolver.openInputStream(uri)
            val byteArrayOutputStream = ByteArrayOutputStream()

            // Read the image content into a byte array
            val buffer = ByteArray(1024)
            var bytesRead: Int
            while (inputStream?.read(buffer).also { bytesRead = it ?: -1 } != -1) {
                byteArrayOutputStream.write(buffer, 0, bytesRead)
            }

            // Convert the byte array to Base64
            val byteArray = byteArrayOutputStream.toByteArray()
            return Base64.encodeToString(byteArray, Base64.DEFAULT)
        } catch (e: Exception) {
            return null
        }
    }

}

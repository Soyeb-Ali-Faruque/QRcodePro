package com.s5tech.qrcodepro.ui.qr_services


import android.Manifest
import android.content.ContentValues
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Bundle
import android.provider.MediaStore
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.graphics.drawable.toBitmap
import com.s5tech.qrcodepro.R
import java.io.OutputStream

// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [download_qrFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class download_qrFragment : Fragment() {
    // TODO: Rename and change types of parameters
    private var param1: String? = null
    private var param2: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        arguments?.let {
            param1 = it.getString(ARG_PARAM1)
            param2 = it.getString(ARG_PARAM2)
        }
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        val view= inflater.inflate(R.layout.fragment_download_qr, container, false)

        // Get views
        val qrView: ImageView = view.findViewById(R.id.qrView)
        val downloadButton: Button = view.findViewById(R.id.downloadQR)

        // Get decoded QR code string from arguments
        val byteArray = arguments?.getByteArray("qrCodeResult")

        if (byteArray != null) {
            // Convert byte array to Bitmap
            val qrBitmap = BitmapFactory.decodeByteArray(byteArray, 0, byteArray.size)
            if (qrBitmap != null) {
                qrView.setImageBitmap(qrBitmap)
            } else {
                Toast.makeText(requireContext(), "Failed to load QR Code", Toast.LENGTH_SHORT).show()
            }
        } else {
            Toast.makeText(requireContext(), "QR Code data is empty", Toast.LENGTH_SHORT).show()
        }

        // Handle download button click (placeholder logic)
        downloadButton.setOnClickListener {
            // Check for permissions and request if necessary
            if (ContextCompat.checkSelfPermission(requireContext(), Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(requireActivity(), arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE), 100)
            } else {
                saveImage(qrView.drawable.toBitmap())
            }
        }

        return view
    }
    private fun saveImage(bitmap: Bitmap) {
        try {
            // Get the external storage directory for the app
            val contentResolver = requireContext().contentResolver

            val contentValues = ContentValues().apply {
                put(MediaStore.Images.Media.DISPLAY_NAME, "qr_code_${System.currentTimeMillis()}.png")
                put(MediaStore.Images.Media.MIME_TYPE, "image/png")
                put(MediaStore.Images.Media.RELATIVE_PATH, "Pictures/QRcodePro") // Specify the folder where it will be saved
            }

            // Insert the new image into MediaStore
            val imageUri = contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)

            // Open an output stream to write the bitmap data
            val outputStream: OutputStream? = imageUri?.let { contentResolver.openOutputStream(it) }
            outputStream?.use {
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, it)
            }

            // Notify the gallery to update
            requireContext().sendBroadcast(Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE, imageUri))

            Toast.makeText(requireContext(), "QR Code saved!", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            Log.e("DownloadQR", "Error saving image", e)
            Toast.makeText(requireContext(), "Failed to save QR Code", Toast.LENGTH_SHORT).show()
        }
    }













    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment download_qrFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            download_qrFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}
package com.s5tech.qrcodepro.ui.qr_services

import ApiHelper
import android.content.Context
import android.graphics.Bitmap
import android.graphics.Color
import android.net.Uri
import android.os.Bundle
import android.util.Base64
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import com.s5tech.qrcodepro.R
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import androidx.navigation.fragment.findNavController
import java.io.ByteArrayOutputStream
import com.afollestad.materialdialogs.MaterialDialog
import com.afollestad.materialdialogs.color.colorChooser
import com.airbnb.lottie.LottieAnimationView
import com.s5tech.qrcodepro.MainActivity
import com.s5tech.qrcodepro.utils.NetworkUtils
import java.io.InputStream


// TODO: Rename parameter arguments, choose names that match
// the fragment initialization parameters, e.g. ARG_ITEM_NUMBER
private const val ARG_PARAM1 = "param1"
private const val ARG_PARAM2 = "param2"

/**
 * A simple [Fragment] subclass.
 * Use the [qr_textFragment.newInstance] factory method to
 * create an instance of this fragment.
 */
class qr_textFragment : Fragment(){
    // TODO: Rename and change types of parameters
    private var param1: String? = null
    private var param2: String? = null

    private var encodedImage: String? = null
    private  var customization: qr_customization = qr_customization()
    private lateinit var animationView: LottieAnimationView



    override fun onAttach(context: Context) {
        super.onAttach(context)
        // Ensure MainActivity is available
        if (context is MainActivity) {
            animationView = context.findViewById(R.id.animationView)
        }
    }





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
        val view=  inflater.inflate(R.layout.fragment_qr_text, container, false)


        val textInput: EditText = view.findViewById(R.id.textInput)
        val customizeTextView: TextView = view.findViewById(R.id.customizeTextView)
        val customizationOptions: LinearLayout = view.findViewById(R.id.customizationOptions)
        val fillColorTextView: TextView = view.findViewById(R.id.fillColorTextView)
        val backgroundColorTextView: TextView = view.findViewById(R.id.backgroundColorTextView)
        val uploadLogoTextView: TextView = view.findViewById(R.id.uploadLogoTextView)
        val generateQRButton: Button = view.findViewById(R.id.generateQR)



        // data
        var text: String = ""
        var fillColor: String = "#000000" // Set initial value (black)
        var backgroundColor: String = "#FFFFFF" // Set initial value (white)

        //control visibility of customization qr code
        customizeTextView.setOnClickListener {
            if (customizationOptions.visibility == View.GONE) {
                customizationOptions.visibility = View.VISIBLE
                customizeTextView.text = "Hide customization options"
            }else{
                customizationOptions.visibility = View.GONE
                customizeTextView.text = "Customize your QR"
            }
        }
        //handling color picking event for qr and its background color
        fillColorTextView.setOnClickListener {
            customization.openColorPickerDialog(
                context = requireContext(),
                title = "Fill Color",
                initialColor = 0x000000,
                textView = fillColorTextView
            ) { hexColor ->
                fillColor=hexColor
                // Check if the updated backgroundColor is white and update the text color accordingly
                if (fillColor.equals("#FFFFFF", ignoreCase = true)) {
                    fillColorTextView.setTextColor(0xFF000000.toInt()) // Set text color to black
                }
            }

        }
        backgroundColorTextView.setOnClickListener {
            customization.openColorPickerDialog(
                context = requireContext(),
                title = "Background Color",
                initialColor = 0xFFFFFF, // Default color: White
                textView = backgroundColorTextView
            ) { hexColor ->
                backgroundColor = hexColor // Store the selected hex value
                if (backgroundColor.equals("#FFFFFF", ignoreCase = true)) {
                    backgroundColorTextView.setTextColor(0xFF000000.toInt()) // Set text color to black
                }
            }

        }


        // Initialize the image picker
        customization.initializeImagePicker(this) { encodedImageResult ->
            encodedImage = encodedImageResult
            if (encodedImage != null) {
                Toast.makeText(requireContext(), "Image uploaded successfully ", Toast.LENGTH_SHORT).show()
                uploadLogoTextView.text = "Upload logo (logo uploaded successfully)"
            }
        }
        // Set the onClickListener for the upload logo button
        uploadLogoTextView.setOnClickListener {
            // Launch the image picker
            customization.launchImagePicker()

        }


        generateQRButton.setOnClickListener {
            (activity as MainActivity).showLoadingAnimation()
            text=textInput.text.toString()
            if(text.isEmpty()){
                (activity as MainActivity).hideLoadingAnimation()

                textInput.error = "This field cannot be empty"

            }else if(!NetworkUtils.isInternetAvailable(requireContext())){
                (activity as MainActivity).hideLoadingAnimation()
                Toast.makeText(
                    requireContext(),
                    "check internet connectivity!",
                    Toast.LENGTH_LONG
                ).show()

            }
            else {

                // Create request data
                val requestData = mutableMapOf(
                    "type" to "text",
                    "text_content" to text,
                    "fill_color" to fillColor,
                    "background_color" to backgroundColor
                )
// Add "logo" key if encodedImage is not null or empty
                encodedImage?.let {
                    requestData["logo"] = it

                    // Add "logo_shape" if logo is provided
                    requestData["logo_shape"] =
                        "circle" // You can change this value based on your condition if needed
                }

                // Show the animation before an API call

                // Call API in a coroutine
                GlobalScope.launch(Dispatchers.IO) {
                    val apiHelper = ApiHelper()
                    val qrCodeResult = apiHelper.sendApiRequest(requestData)

                    withContext(Dispatchers.Main) {
                        (activity as MainActivity).hideLoadingAnimation()

                        if (qrCodeResult != null) {
                            Toast.makeText(
                                requireContext(),
                                "QR Code generated successfully!",
                                Toast.LENGTH_SHORT
                            ).show()
                            // Handle successful response (e.g., display QR code in ImageView)
                            // Navigate to another fragment with qrCodeResult
                            val bundle = Bundle().apply {
                                val byteArrayOutputStream = ByteArrayOutputStream()
                                qrCodeResult.compress(
                                    Bitmap.CompressFormat.PNG,
                                    100,
                                    byteArrayOutputStream
                                )
                                val byteArray = byteArrayOutputStream.toByteArray()
                                putByteArray("qrCodeResult", byteArray)
                            }
                            findNavController().navigate(R.id.nav_downloadQR, bundle)
                        } else {
                            Toast.makeText(
                                requireContext(),
                                "Failed to generate QR Code",
                                Toast.LENGTH_SHORT
                            ).show()
                        }
                    }
                }
            }
        }

        return view

    }

























    companion object {
        /**
         * Use this factory method to create a new instance of
         * this fragment using the provided parameters.
         *
         * @param param1 Parameter 1.
         * @param param2 Parameter 2.
         * @return A new instance of fragment qr_textFragment.
         */
        // TODO: Rename and change types and number of parameters
        @JvmStatic
        fun newInstance(param1: String, param2: String) =
            qr_textFragment().apply {
                arguments = Bundle().apply {
                    putString(ARG_PARAM1, param1)
                    putString(ARG_PARAM2, param2)
                }
            }
    }
}
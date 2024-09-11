const encodingCodeSamples = {
    java: `
import java.util.Base64;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;

public class Base64ImageExample {
    public static void main(String[] args) throws IOException {
        byte[] fileContent = Files.readAllBytes(Paths.get("image.jpg"));
        String encodedString = Base64.getEncoder().encodeToString(fileContent);
        System.out.println("Encoded Image: " + encodedString);
    }
}
    `,
    python: `
import base64

with open("image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    print("Encoded Image:", encoded_string)
    `,
    kotlin: `
import java.util.Base64
import java.nio.file.Files
import java.nio.file.Paths

fun main() {
    val fileContent = Files.readAllBytes(Paths.get("image.jpg"))
    val encodedString = Base64.getEncoder().encodeToString(fileContent)
    println("Encoded Image: $encodedString")
}
    `,
    go: `
package main

import (
    "encoding/base64"
    "fmt"
    "io/ioutil"
)

func main() {
    data, err := ioutil.ReadFile("image.jpg")
    if err != nil {
        panic(err)
    }
    encodedString := base64.StdEncoding.EncodeToString(data)
    fmt.Println("Encoded Image:", encodedString)
}
    `,
    csharp: `
using System;
using System.IO;

public class Base64ImageExample
{
    public static void Main(string[] args) {
        byte[] imageBytes = File.ReadAllBytes("image.jpg");
        string base64String = Convert.ToBase64String(imageBytes);
        Console.WriteLine("Encoded Image: " + base64String);
    }
}
    `,
    ruby:`
    require 'base64'

image_data = File.open('image.jpg', 'rb').read
encoded_string = Base64.encode64(image_data)
puts "Encoded Image: #{encoded_string}"
   
`,
javaScript:`const fs = require('fs');

fs.readFile('image.jpg', (err, data) => {
    if (err) throw err;
    const encodedString = Buffer.from(data).toString('base64');
    console.log('Encoded Image:', encodedString);
});
`,
php:`
<?php
$imageData = file_get_contents('image.jpg');
$encodedString = base64_encode($imageData);
echo "Encoded Image: " . $encodedString;
?>
`,
swift:`
import Foundation
import UIKit

func encodeImageToBase64(imagePath: String) {
    if let image = UIImage(contentsOfFile: imagePath),
       let imageData = image.jpegData(compressionQuality: 1.0) {
        let encodedString = imageData.base64EncodedString()
        print("Encoded Image: \(encodedString)")
    } else {
        print("Failed to load image or convert to data.")
    }
}

// Example usage
encodeImageToBase64(imagePath: "path/to/image.jpg")
`

};

const decodingCodeSamples = {
    java: `
import java.util.Base64;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.IOException;
import java.nio.file.StandardOpenOption;

public class Base64ImageDecoder {
    public static void main(String[] args) throws IOException {
        String encodedString = "Base64EncodedImageString";
        byte[] decodedBytes = Base64.getDecoder().decode(encodedString);
        Files.write(Paths.get("decodedImage.jpg"), decodedBytes, StandardOpenOption.CREATE);
    }
}
    `,
    python: `
import base64

encoded_string = "Base64EncodedImageString"
image_data = base64.b64decode(encoded_string)
with open("decodedImage.jpg", "wb") as image_file:
    image_file.write(image_data)
    `,
    kotlin: `
import java.util.Base64
import java.nio.file.Files
import java.nio.file.Paths
import java.nio.file.StandardOpenOption

fun main() {
    val encodedString = "Base64EncodedImageString"
    val decodedBytes = Base64.getDecoder().decode(encodedString)
    Files.write(Paths.get("decodedImage.jpg"), decodedBytes, StandardOpenOption.CREATE)
}
    `,
    go: `
package main

import (
    "encoding/base64"
    "fmt"
    "io/ioutil"
)

func main() {
    encodedString := "Base64EncodedImageString"
    decodedBytes, _ := base64.StdEncoding.DecodeString(encodedString)
    ioutil.WriteFile("decodedImage.jpg", decodedBytes, 0644)
}
    `,
    csharp: `
using System;
using System.IO;

public class Base64ImageDecoder
{
    public static void Main(string[] args) {
        string encodedString = "Base64EncodedImageString";
        byte[] decodedBytes = Convert.FromBase64String(encodedString);
        File.WriteAllBytes("decodedImage.jpg", decodedBytes);
        Console.WriteLine("Decoded Image saved as 'decodedImage.jpg'");
    }
}
    `,

    ruby:`
    require 'base64'

encoded_string = "Base64EncodedImageString"
decoded_data = Base64.decode64(encoded_string)
File.open('decodedImage.jpg', 'wb') { |file| file.write(decoded_data) }
puts "Decoded Image saved as 'decodedImage.jpg'"
`,
javaScript:`
const fs = require('fs');

const encodedString = "Base64EncodedImageString";
const decodedData = Buffer.from(encodedString, 'base64');
fs.writeFile('decodedImage.jpg', decodedData, (err) => {
    if (err) throw err;
    console.log('Decoded Image saved as \'decodedImage.jpg\'');
});
`,

    php:`
    <?php
$encodedString = "Base64EncodedImageString";
$decodedData = base64_decode($encodedString);
file_put_contents('decodedImage.jpg', $decodedData);
echo "Decoded Image saved as 'decodedImage.jpg'";
?>
`,
swift:`
import Foundation
import UIKit

func decodeBase64ToImage(encodedString: String, outputPath: String) {
    if let decodedData = Data(base64Encoded: encodedString),
       let image = UIImage(data: decodedData) {
        if let imageData = image.jpegData(compressionQuality: 1.0) {
            do {
                try imageData.write(to: URL(fileURLWithPath: outputPath))
                print("Decoded Image saved as '\(outputPath)'")
            } catch {
                print("Error saving decoded image: \(error)")
            }
        }
    } else {
        print("Failed to decode base64 string or convert to image.")
    }
}

// Example usage
decodeBase64ToImage(encodedString: "Base64EncodedImageString", outputPath: "path/to/decodedImage.jpg")
`
};

// Update encoding code block based on selected language
function changeEncodingLanguage() {
    const selectedLanguage = document.getElementById('language-encoding').value;
    document.getElementById('encoding-code-block').textContent = encodingCodeSamples[selectedLanguage].trim();
}

// Update decoding code block based on selected language
function changeDecodingLanguage() {
    const selectedLanguage = document.getElementById('language-decoding').value;
    document.getElementById('decoding-code-block').textContent = decodingCodeSamples[selectedLanguage].trim();
}

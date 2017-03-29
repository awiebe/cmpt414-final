var myImage = 'OCR.jpg';

function myFunction() {
	Tesseract.recognize(myImage)
.then(function(result){
    console.log(result)
})
}
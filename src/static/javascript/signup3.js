let counter = 1;
//keeps track of what images have already been selected
let chosenImages = new Array(9);
for (let i = 0; i < chosenImages.length; i++) {
    chosenImages[i] = 0;
}

//for all images
Array.from(document.getElementsByClassName("signup3-buttons")).forEach(function(element) {
    element.addEventListener('click', image); //if clicked, call image()
});

function image() {
    if(chosenImages[this.getAttribute('data-section')] == 1){  //prevents selecting same image
        alert('You have already chosen this image. Click RESET at the top right if you would like to start over.');
    } else if(counter > 4){ //only 4 images can be clicked
        alert('You can only select 4 images.');
    } else {
        document.getElementById('password').value += this.getAttribute('data-number'); //apend images data-number to password
        chosenImages[this.getAttribute('data-section')] = 1; //keep track that this image was selected
        const number = document.createElement("div");
        number.className = "number";
        number.textContent = counter;
        this.parentNode.insertBefore(number, this);
        counter++;
    }
}

//Reset Functionality
document.getElementById("reset").addEventListener('click', reset);
function reset(){
    console.log("in");
    document.getElementById('password').value = "";
    const numbers = document.querySelectorAll(".number");
    numbers.forEach(function(number) {
        number.parentNode.removeChild(number);
    });
    counter = 1;
    for (let i = 0; i < chosenImages.length; i++) {
        chosenImages[i] = 0;
    }
}

//Settings Functionality
document.getElementById("settings").addEventListener('click', settings);
function settings() {
    var settingsWindow = document.getElementById("settings-window");
    if (settingsWindow.style.display === "block") {
        settingsWindow.style.display = "none";
    } else {
        settingsWindow.style.display = "block";
    }
}

// Determines which mode was activated/deactivated 
function handleModes(text) {
    if(text) {
        var textModeCheckbox = document.getElementById("text-mode");
        textMode(textModeCheckbox.checked);
    } else {
        var colorBlindModeCheckbox = document.getElementById("colorblind-mode");
        colorBlindMode(colorBlindModeCheckbox.checked);
    }
}

function textMode(enabled){
    if(enabled) {
        //grab names for Text Mode
        Array.from(document.getElementsByClassName("signup3-buttons")).forEach(function(element) {
            //pulls and converts src to picture name
            const filePath = element.getAttribute(`src`);

            const imageType = document.createElement("div");
            imageType.className = "iname";
            imageType.textContent = filePath.split('/').pop().slice(0, -4);
            element.parentNode.insertBefore(imageType, element.nextSibling);
        });

        console.log("Text mode enabled");
    } else {
        const inames = document.querySelectorAll('.iname');
        inames.forEach(function(iname) {
            iname.remove();
        });
        console.log("Text mode disabled");
    }
}

function colorBlindMode(enabled) {
    const signupWhite = document.getElementById("signup3-white");
  
    if (enabled) {
        // Apply colorblind filter to each signup3-buttons element
        Array.from(document.getElementsByClassName("signup3-buttons")).forEach(function (element) {
            element.style.filter = "brightness(150%) saturate(80%) hue-rotate(-30deg)";
        });
  
        // Set light gray background color for #signup3-white element
        signupWhite.style.backgroundColor = "#D3D3D3";
  
        console.log("Colorblind mode enabled");
    } else {
        // Remove colorblind filter from each signup3-buttons element
        Array.from(document.getElementsByClassName("signup3-buttons")).forEach(function (element) {
            element.style.filter = "";
        });
  
        // Restore white background color for #signup3-white element
        signupWhite.style.backgroundColor = "white";
  
        console.log("Colorblind mode disabled");
    }
}
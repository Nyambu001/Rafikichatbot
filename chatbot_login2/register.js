const form = document.getElementById("form");
const username = document.getElementById("username");
const email = document.getElementById("email");
const password = document.getElementById("password");
const password2 = document.getElementById("password2");


//error message to be displayed
//seterror receives a html element and an error message
const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success');//add error class and remove success class if present
    //hence adds the red border
}

//success message to be displayed
const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorDisplay = inputControl.querySelector('.error');

    errorDisplay.innerText = "";
    inputControl.classList.add('success');
    inputControl.classList.remove('error');//add success class and remove error class if present
    //hence adds the green border
}

const isValidEmail = email => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return re.test(String(email).toLowerCase());
}

//define values to be validated
const validateInputs = () => {
    let isValid = true; // Track validation status

    const usernameValue = username.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const password2Value = password2.value.trim();

    if(usernameValue === "") {
        setError(username, 'Username is required');
        isValid = false;
    } else {
        setSuccess(username);
    }

    if(emailValue === "") {
        setError(email, 'Email is required');
        isValid = false;
    } else if (!isValidEmail(emailValue)){
        setError(email, "Provide a valid email address");
        isValid = false;
    } else {
        setSuccess(email);
    }

    if(passwordValue === "") {
        setError(password, 'Password is required');
        isValid = false;
    } else if (passwordValue.length < 8 ) {
        setError(password, "Password must have at least 8 characters.");
        isValid = false;
    } else {
        setSuccess(password);
    }

    if(password2Value === "") {
        setError(password2, 'Please confirm your password');
        isValid = false;
    } else if (password2Value !== passwordValue) {
        setError(password2, "Passwords don't match");
        isValid = false;
    } else {
        setSuccess(password2);
    }

        // If all inputs are valid, allow further actions
    if (isValid) {
        console.log("Validation successful");
        loadRafikiBot(); // Load the Rafiki Bot
    } else {
        console.log("Validation failed");
    }
};

const loadRafikiBot = () => {
    console.log("Loading Rafiki Bot...");
    window.location.href = "../chatbot/index.html";
};

form.addEventListener('submit', (e) => {
    e.preventDefault(); // Prevent default form submission
    validateInputs();   // Run the validation
});
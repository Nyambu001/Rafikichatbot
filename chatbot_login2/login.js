// Select the form and input elements
const form = document.getElementById('form');
const email = document.getElementById('email');
const password = document.getElementById('password');

// Error message display function
// `setError` receives an HTML element and an error message
const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorMessage = inputControl.querySelector('.error');

    errorMessage.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success'); // Adds red border by toggling classes
};

// Success message display function
const setSuccess = (element) => {
    const inputControl = element.parentElement;
    const errorMessage = inputControl.querySelector('.error');

    errorMessage.innerText = ""; // Clears error message
    inputControl.classList.add('success');
    inputControl.classList.remove('error'); // Adds green border by toggling classes
};

// Email validation function
function validateEmail(emailValue) {
    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailValid.test(emailValue);
}

// Add an event listener to the form submission
form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();

    // Validation logic
    let valid = true;

    // Check email field
    if (emailValue === "") {
        setError(email, "Email cannot be empty.");
        valid = false;
    } else if (!validateEmail(emailValue)) {
        setError(email, "Provide a valid email address.");
        valid = false;
    } else {
        setSuccess(email);
    }

    // Check password field
    if (passwordValue === "") {
        setError(password, "Password cannot be empty.");
        valid = false;
    } else {
        setSuccess(password);
    }

    // Simulate login process if fields are valid
    if (valid) {
        if (emailValue === 'xtnnjr@gmail.com' && passwordValue === 'xtn.njr8') {
            alert("Login successful!");
            window.location.href = '../chatbot/index.html'; // Redirect on successful login
        } else {
            setError(email, "Invalid email or password.");
            setError(password, "Invalid email or password.");
        }
    }
});

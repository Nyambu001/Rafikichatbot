// Select the form and input elements
const form = document.getElementById('form');
const email = document.getElementById('email');
const password = document.getElementById('password');

//error message to be displayed
//seterror receives a html element and an error message
const setError = (element, message) => {
    const inputControl = element.parentElement;
    const errorMessage = inputControl.querySelector('.error');

    errorMessage.innerText = message;
    inputControl.classList.add('error');
    inputControl.classList.remove('success');//add error class and remove success class if present
    //hence adds the red border
}

//success message to be displayed
const setSuccess = element => {
    const inputControl = element.parentElement;
    const errorMessage = inputControl.querySelector('.error');

    errorMessage.innerText = "";
    inputControl.classList.add('success');
    inputControl.classList.remove('error');//add success class and remove error class if present
    //hence adds the green border
}

// Add an event listener to the form submission
form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();

    // Validation logic
    let isvalid = true;

    // Check email field
    if (emailValue === "") {
        setError(email, "Please fill in this field.");
        isValid = false;
    } else if (!validateEmail(emailValue)) {
        setError(email, "Provide a valid email address.");
        isValid = false;
    } else {
        setSuccess(email);
    }

    // Check password field
    if (passwordValue === "") {
        setError(password, "Please fill in this field.");
        isValid = false;
    } else {
        setSuccess(password);
    }

    // Simulate login process if fields are valid
    if (isValid) {
        login(emailValue, passwordValue); // Call the login function
    }
});

// Email validation function
function validateEmail(emailValue) {
    const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailValid.test(emailValue);
}

// Function to handle login
async function login(email, password) {
    try {
        const response = await fetch('http://your-django-api-url/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: password
            }),
        });

        const data = await response.json();

        if (response.ok) {
            // Successful login, handle session or redirect
            console.log('Login successful', data);
        } else {
            // Login failed
            console.error('Login failed', data);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Usage
login('your-username', 'your-password');


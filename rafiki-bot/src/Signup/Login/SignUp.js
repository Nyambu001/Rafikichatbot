import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';

const SignUp = () => {
  const [signedUp, setSignedUp] = useState(false);  // Local state for sign-up status
  const [emailError, setEmailError] = useState(''); // Local state for email error
  const { register, handleSubmit, formState: { errors }, getValues } = useForm({
    defaultValues: {
      email: "",
      password: "",
      confirmPassword: ""
    }
  });

  const onSubmit = (data) => {
    // Check if email is already registered in localStorage
    const existingEmails = JSON.parse(localStorage.getItem('emails')) || [];

    if (existingEmails.includes(data.email)) {
      setEmailError('Email is already registered');
      return; // Prevent form submission if email is already taken
    }

    // Save user details in localStorage after successful registration
    existingEmails.push(data.email); // Add the email to the list
    localStorage.setItem('emails', JSON.stringify(existingEmails)); // Store updated emails

    localStorage.setItem('isSignedUp', 'true');
    localStorage.setItem('username', data.username);
    localStorage.setItem('email', data.email);

    setSignedUp(true); // Update state to show the success message
    setEmailError('');  // Clear email error on successful sign-up

    // Redirect or perform any additional actions (for example, navigate to the login page)
  };

  return (
    <div>
      {signedUp ? (
        <Link to="/login" className="text-blue-600">Login</Link> 
      ) : (
        <div className="max-w-sm p-4 mx-auto my-10 bg-white border rounded-lg shadow-lg">
          <h2 className="mb-6 text-2xl text-center">Sign Up</h2>
          {/* Handle form submission */}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" noValidate>
            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
              <input
                id="email"
                type="email"
                className="w-full px-4 py-2 border border-gray-300 rounded"
                placeholder="Enter your email address"
                {...register('email', {
                  required: 'Email is required',
                  pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address',
                  }
                })}
              />
              <p className="text-sm text-red-700">{errors.email?.message}</p>
              <p className="text-sm text-red-700">{emailError}</p> {/* Display email error */}
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
              <input
                id="password"
                type="password"
                className="w-full px-4 py-2 border border-gray-300 rounded"
                placeholder="Enter your password"
                {...register('password', { 
                  required: 'Password is required', 
                  minLength: { value: 6, message: 'Password must be at least 6 characters' },
                })}
              />
              <p className="text-sm text-red-500">{errors.password?.message}</p>
            </div>

            {/* Confirm Password */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">Confirm Password</label>
              <input
                id="confirmPassword"
                type="password"
                className="w-full px-4 py-2 border border-gray-300 rounded"
                placeholder="Confirm your password"
                {...register('confirmPassword', {
                  required: 'Confirm Password is required',
                  validate: value => value === getValues("password") || 'Passwords do not match'
                })}
              />
              <p className="text-sm text-red-500">{errors.confirmPassword?.message}</p>
            </div>

            {/* Sign Up Button */}
            <div className="flex items-center justify-between">
              <button type="submit" className="px-4 py-2 text-white bg-blue-600 rounded-lg">Sign Up</button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}

export default SignUp;

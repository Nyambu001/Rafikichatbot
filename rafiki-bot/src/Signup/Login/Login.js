import React from 'react';
import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';

const Login = ({ onLogin }) => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const navigate = useNavigate();

  const onSubmit = (data) => {
    // Save the login details and update login state
    localStorage.setItem('isLoggedIn', 'true'); // User is now logged in
    localStorage.setItem('email', data.email); // Save email to localStorage

    // Indicate that the user is logged in and navigate to the main page
    onLogin(true);
    navigate('/');  // Redirect to home page (or wherever you want after login)
  };

  return (
    <div className="max-w-sm p-4 mx-auto my-10 bg-white border rounded-lg shadow-lg">
      <h2 className="mb-6 text-2xl text-center">Login</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
          <input
            id="email"
            type="email"
            className="w-full px-4 py-2 border border-gray-300 rounded"
            placeholder="Enter your Gmail"
            {...register('email', { required: 'Email is required' })}
          />
          <p className="text-sm text-red-500">{errors.email?.message}</p>
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
          <input
            id="password"
            type="password"
            className="w-full px-4 py-2 border border-gray-300 rounded"
            placeholder="Enter your password"
            {...register('password', { required: 'Password is required' })}
          />
          <p className="text-sm text-red-500">{errors.password?.message}</p>
        </div>

        <div className="flex items-center justify-between">
          <Link to="/forgot-password" className="text-sm text-blue-600">Forgot Password?</Link>
          <button type="submit" className="px-4 py-2 text-white bg-blue-600 rounded-lg">Login</button>
        </div>
      </form>

      <p className="mt-4 text-center">
        Don't have an account? <Link to="/signup" className="text-blue-600">Sign up</Link>
      </p>
    </div>
  );
};

export default Login;

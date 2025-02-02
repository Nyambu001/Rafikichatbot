// ForgotPassword.js
import React from 'react';
import { useForm } from 'react-hook-form';

const ForgotPassword = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();

  const onSubmit = (data) => {
    // Handle password reset
    alert(`Password reset link sent to ${data.email}`);
  };

  return (
    <div className="max-w-sm p-4 mx-auto my-10 bg-white border rounded-lg shadow-lg">
      <h2 className="mb-6 text-2xl text-center">Forgot Password?</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
          <input
            id="email"
            type="email"
            className="w-full px-4 py-2 border border-gray-300 rounded"
            placeholder="Enter your email"
            {...register('email', { required: 'Email is required' })}
          />
          {errors.email && <p className="text-sm text-red-500">{errors.email.message}</p>}
        </div>

        <div className="flex items-center justify-between">
          <button type="submit" className="px-4 py-2 text-white bg-blue-600 rounded-lg">Reset Password</button>
        </div>
      </form>
    </div>
  );
};

export default ForgotPassword;

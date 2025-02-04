import { useForm } from 'react-hook-form';
import { useState } from 'react';
import { FaEye, FaEyeSlash, FaLock } from 'react-icons/fa';
import {Link} from 'react-router-dom'
const SignUp = () => {
    const { register, handleSubmit, formState: { errors }, reset, getValues } = useForm();
    const [showPassword, setShowPassword] = useState(false); // State to manage password visibility

    const onSubmit = (data) => {
        console.log(data);
        reset(); // Reset the form after successful submission
    };

    return (
        <div className="flex items-center justify-center h-screen">
            <div className="w-full max-w-sm p-8 bg-white rounded-lg shadow-lg">
                <h2 className="mb-6 text-2xl font-bold text-center">Sign Up</h2>
                <form onSubmit={handleSubmit(onSubmit)}>

                    {/* Email */}
                    <div className="mb-6">
                        <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-700">Email</label>
                        <input
                            type="email"
                            id="email"
                            {...register('email', {
                                required: 'Email is required',
                                pattern: {
                                    value: /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/,
                                    message: 'Invalid email format'
                                }
                            })}
                            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        {errors.email && <p className="text-xs text-red-500">{errors.email.message}</p>}
                    </div>

                    {/* Password */}
                    <div className="mb-4">
                        <label className="block mb-2 text-sm font-bold text-gray-700" htmlFor="password">Password</label>
                        <div className="relative">
                            
                            <span className="absolute top-0 mt-2 text-gray-500 left-3">
                                <FaLock />
                            </span>

                            {/* Input field */}
                            <input
                                {...register("password", { required: true, minLength: 5, maxLength: 12 })}
                                className="w-full px-10 py-2 mb-3 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"
                                type={showPassword ? "text" : "password"}
                                id="password"
                                placeholder="Password"
                            />

                            
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute top-0 right-0 mt-3 mr-4"
                            >
                                {showPassword ? <FaEyeSlash /> : <FaEye />}
                            </button>
                        </div>
                        {errors.password && <p className="text-xs italic text-red-500">Password should be between 5 and 12 characters</p>}
                    </div>

                    {/* Confirm Password */}
                    <div className="mb-6">
                        <label htmlFor="confirmPassword" className="block mb-2 text-sm font-medium text-gray-700">
                            Confirm Password
                        </label>
                        <div className="relative">
                            
                            <span className="absolute text-gray-500 -translate-y-1/2 top-1/2 left-3">
                                <FaLock />
                            </span>

                            {/* Input field */}
                            <input
                                {...register("confirmPassword", {
                                    required: "Confirm password is required",
                                    validate: value => value === getValues("password") || "Passwords do not match"
                                })}
                                className="w-full py-2 pl-10 pr-10 leading-tight text-gray-700 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type={showPassword ? "text" : "password"}
                                id="confirmPassword"
                                placeholder="Confirm Password"
                            />

                            
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute -translate-y-1/2 top-1/2 right-3"
                            >
                                {showPassword ? <FaEyeSlash /> : <FaEye />}
                            </button>
                        </div>
                        {errors.confirmPassword && <p className="text-xs text-red-500">{errors.confirmPassword.message}</p>}
                    </div>

                    {/* Sign Up Button */}
                    <button
                        type="submit"
                        className="w-full py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none"
                    >
                        Sign Up
                    </button>

                  {/* Forgot Password & Sign Up Links */}
                  <div className="flex justify-between mt-4 text-sm">
                        <button type="button" className="text-blue-500 hover:underline">Forgot Password?</button>
                        <Link 
                            to="/" 
                            className="text-blue-500 cursor-pointer hover:underline"
                        >
                            Login
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default SignUp;

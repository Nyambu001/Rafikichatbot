import { useForm } from 'react-hook-form';
import { useState } from 'react';
import { FaEye, FaEyeSlash, FaLock } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom'; 

const Login = ({ onLogin }) => {
    const { register, handleSubmit, formState: { errors }, reset } = useForm();
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate(); 

    const onSubmit = (data) => {
        localStorage.setItem('loggedIn', 'true'); 
        onLogin(); 
        navigate('/'); // This will redirect to the home page (Chatbot)
        
        reset(); 
    };

    return (
        <div className="flex items-center justify-center h-screen">
            <div className="w-full max-w-sm p-8 bg-white rounded-lg shadow-lg">
                <h2 className="mb-6 text-2xl font-bold text-center">Login</h2>
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
                    <div className="mb-6">
                        <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-700">Password</label>
                        <div className="relative">
                            <span className="absolute text-gray-500 -translate-y-1/2 top-1/2 left-3">
                                <FaLock />
                            </span>

                            <input
                                {...register("password", { required: "Password is required" })}
                                className="w-full py-2 pl-10 pr-10 leading-tight text-gray-700 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type={showPassword ? "text" : "password"}
                                id="password"
                                placeholder="Password"
                            />

                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute -translate-y-1/2 top-1/2 right-3"
                            >
                                {showPassword ? <FaEyeSlash /> : <FaEye />}
                            </button>
                        </div>
                        {errors.password && <p className="text-xs text-red-500">{errors.password.message}</p>}
                    </div>

                    {/* Login Button */}
                    <button
                        type="submit"
                        className="w-full py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none"
                    >
                        Login
                    </button>

                    {/* Forgot Password & Sign Up Links */}
                    <div className="flex justify-between mt-4 text-sm">
                        <button type="button" className="text-blue-500 hover:underline">Forgot Password?</button>
                        <Link 
                            to="/signup"
                            className="text-blue-500 cursor-pointer hover:underline"
                        >
                            Sign Up
                        </Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;

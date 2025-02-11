import { useForm } from 'react-hook-form';
import { useState } from 'react';
import { FaEye, FaEyeSlash, FaLock, FaUser } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';

const Login = ({ onLogin }) => {
    const { register, handleSubmit, formState: { errors }, reset } = useForm();
    const [showPassword, setShowPassword] = useState(false);
    const [loginError, setLoginError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const onSubmit = async (data) => {
        setLoginError('');
        setIsLoading(true);

        try {
            const response = await fetch('http://127.0.0.1:8000/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: data.username,
                    password: data.password,
                }),
            });

            const result = await response.json();
            if (response.ok) {
                // Store the JWT token
                localStorage.setItem('authToken', result.token);

                // Directly store userId from the response
                const userId = result.user_id;  // Assuming your backend sends user_id directly
                localStorage.setItem('userId', userId);

                onLogin();  // Trigger login success callback
                navigate('/');  // Navigate to the home page
                reset();
            } else {
                setLoginError(result.error || 'Login failed');
            }
        } catch (error) {
            console.error('Error:', error);
            setLoginError('An error occurred. Please try again later.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center h-screen">
            <div className="w-full max-w-sm p-8 bg-white rounded-lg shadow-lg">
                <h2 className="mb-6 text-2xl font-bold text-center">Login</h2>
                <form onSubmit={handleSubmit(onSubmit)}>

                    {/* Username */}
                    <div className="mb-6">
                        <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-700">Username</label>
                        <div className="relative">
                            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                                <FaUser />
                            </span>
                            <input
                                type="text"
                                id="username"
                                {...register('username', { required: 'Username is required' })}
                                className="w-full px-10 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        {errors.username && <p className="text-xs text-red-500">{errors.username.message}</p>}
                    </div>

                    {/* Password */}
                    <div className="mb-6">
                        <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-700">Password</label>
                        <div className="relative">
                            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                                <FaLock />
                            </span>
                            <input
                                {...register("password", { required: "Password is required" })}
                                className="w-full px-10 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                type={showPassword ? "text" : "password"}
                                id="password"
                                placeholder="Password"
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-3 top-1/2 transform -translate-y-1/2"
                            >
                                {showPassword ? <FaEyeSlash /> : <FaEye />}
                            </button>
                        </div>
                        {errors.password && <p className="text-xs text-red-500">{errors.password.message}</p>}
                    </div>

                    {/* Error Message */}
                    {loginError && <p className="text-red-500 text-center">{loginError}</p>}

                    {/* Login Button */}
                    <button
                        type="submit"
                        className="w-full py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none"
                        disabled={isLoading || Object.keys(errors).length > 0} // Disable button if loading or validation errors
                    >
                        {isLoading ? (
                            <span>Loading...</span> // Show loading state text
                        ) : (
                            'Login'
                        )}
                    </button>

                    {/* Forgot Password & Sign Up Links */}
                    <div className="flex justify-between mt-4 text-sm">
                        <button type="button" className="text-blue-500 hover:underline">Forgot Password?</button>
                        <Link to="/signup" className="text-blue-500 cursor-pointer hover:underline">Sign Up</Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Login;

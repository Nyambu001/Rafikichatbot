import { useForm } from 'react-hook-form';
import { useState } from 'react';
import { FaEye, FaEyeSlash, FaLock, FaUser } from 'react-icons/fa';
import { Link } from 'react-router-dom';

const SignUp = () => {
    const { register, handleSubmit, formState: { errors }, reset } = useForm();
    const [showPassword, setShowPassword] = useState(false);
    const [signUpError, setSignUpError] = useState('');

const onSubmit = async (data) => {
   console.log("Form Data:", data);
    setSignUpError('');

    // Fetch the CSRF token
    const getCSRFToken = async () => {
        try {
            const response = await fetch('http://127.0.0.1:8000/get_csrf_token/');
            const data = await response.json();
            return data.csrf_token;
        } catch (error) {
            console.error("Error fetching CSRF token:", error);
            setSignUpError("Could not fetch CSRF token");
            return null;
        }
    };

    const csrfToken = await getCSRFToken();
    if (!csrfToken) {
        console.error("CSRF token is not available.");
        setSignUpError("CSRF token not found.");
        return;
    }

    try {
        const response = await fetch('http://127.0.0.1:8000/register/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                username: data.username,
                password: data.password,
                email: data.email,
            }),
        });

        const result = await response.json();
        if (response.ok) {
            alert('Registration successful!');
            reset();
        } else {
            setSignUpError(result.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Error:', error);
        setSignUpError('An error occurred. Please try again later.');
    }
};


    return (
        <div className="flex items-center justify-center h-screen">
            <div className="w-full max-w-sm p-8 bg-white rounded-lg shadow-lg">
                <h2 className="mb-6 text-2xl font-bold text-center">Sign Up</h2>
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
                                {...register('username', {
                                    required: 'Username is required',
                                    minLength: { value: 3, message: 'Username must be at least 3 characters' },
                                    maxLength: { value: 20, message: 'Username cannot exceed 20 characters' }
                                })}
                                className="w-full px-10 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>
                        {errors.username && <p className="text-xs text-red-500">{errors.username.message}</p>}
                    </div>

                    {/* Email (Optional) */}
                    <div className="mb-6">
                        <label htmlFor="email" className="block mb-2 text-sm font-medium text-gray-700">Email</label>
                        <input
                            type="email"
                            id="email"
                            {...register('email', {
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
                            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                                <FaLock />
                            </span>
                            <input
                                {...register("password", {
                                    required: 'Password is required',
                                    minLength: { value: 5, message: 'Must be at least 5 characters' },
                                    maxLength: { value: 12, message: 'Cannot exceed 12 characters' }
                                })}
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
                    {signUpError && <p className="text-red-500 text-center">{signUpError}</p>}

                    {/* Sign Up Button */}
                    <button type="submit" className="w-full py-2 text-white bg-blue-500 rounded-md hover:bg-blue-600 focus:outline-none">
                        Sign Up
                    </button>

                    {/* Links */}
                    <div className="flex justify-between mt-4 text-sm">
                        <button type="button" className="text-blue-500 hover:underline">Forgot Password?</button>
                        <Link to="/" className="text-blue-500 cursor-pointer hover:underline">Login</Link>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default SignUp;

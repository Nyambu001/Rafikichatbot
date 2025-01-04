import { useForm } from 'react-hook-form';


const SignUp = ({onSignUp}) => {
    const { register, handleSubmit,formState:{errors} } = useForm({
        defaultValues:{
            username:"",
            email:"",
            password:""
        }
    });

    const onSubmit = (data) => {
        onSignUp(true);//lets parent know that a user has been signed up successfully
    }
    
    return (
    <div className="max-w-sm p-4 mx-auto my-10 bg-white border rounded-lg shadow-lg">
      <h2 className="mb-6 text-2xl text-center">Sign Up</h2>
      {/*noValidate ensures the browser does not interfere with the custom validation */}
      <form onSubmit={handleSubmit(onSubmit)} className='space-y-4' noValidate>
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
        <input
        id='email'
        type='email'
        className='w-full px-4 py-2 border border-gray-300 rounded'
        placeholder='Enter your email address...'
        {...register("email",
            {
                required: 'Email is required',
                pattern: {
                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                    message: 'Invalid email address'
                }
            }
            
        )}/>
           <p className="text-sm text-red-700 ">{errors.email?.message}</p>  
        </div>
        {/* password*/}
        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
          <input
            id="password"
            type="password"
            className="w-full px-4 py-2 border border-gray-300 rounded"
            placeholder="Enter your password"
            {...register('password', { 
              required: 'Password is required', 
              minLength: 
              { value: 8, 
                message: 'Password must be at least 6 characters' 
            } 
            })}
          />
      <p className="text-sm text-red-500">{errors.password?.message}</p>
        </div>
        {/* confirm  password*/}
        <div>
          <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">Confirm Password</label>
          <input
            id="confirmPassword"
            type="password"
            className="w-full px-4 py-2 border border-gray-300 rounded"
            placeholder="Confirm your password"
            {...register('confirmPassword', { 
              required: 'Password is required',
              validate: (value, { password }) => value === password || 'Passwords do not match'
            })}
          />
        <p className="text-sm text-red-500">{errors.confirmPassword?.message}</p>
        </div>
            {/*SIGN UP*/}
            <div className="flex items-center justify-between">
          <button type="submit" className="px-4 py-2 text-white bg-blue-600 rounded-lg">Sign Up</button>
        </div>
      </form>
    </div>
  )
}

export default SignUp

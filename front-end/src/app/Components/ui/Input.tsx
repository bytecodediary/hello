import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  type?: string;
  placeholder?: string;
  className?: string;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ type = 'text', placeholder, className, ...rest }, ref) => {
  return (
    <input
      type={type}
      placeholder={placeholder}
      className={`border rounded-md p-2 ${className}`}
      ref={ref}
      {...rest}
    />
  );
});

Input.displayName = "Input";

export default Input;

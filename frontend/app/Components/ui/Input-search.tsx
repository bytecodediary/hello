// src/components/ui/InputSearch.tsx
import React from 'react';
import Input from './Input';

export const InputSearch = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, ...props }, ref) => {
    return (
      <Input
        ref={ref}
        className={`w-full ${className}`}
        {...props}
      />
    );
  }
);

InputSearch.displayName = 'InputSearch';

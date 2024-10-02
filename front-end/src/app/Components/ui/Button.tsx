"use client";

import React from 'react';
import './button.css'; 

interface ButtonProps {
  label: string;
  variant: 'primary' | 'secondary'  ;
  onClick: () => void;
}

const Button: React.FC<ButtonProps> = ({ label, variant, onClick }) => {
  return (
    <button
      className={`button ${variant}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
};

export default Button;


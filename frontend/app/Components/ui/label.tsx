import React from "react";

interface LabelProps {
  htmlFor?: string; // Optional, as it's not always necessary
  children: React.ReactNode; // This can accept any valid React nodes
  className?: string; // Optional
}

export default function Label({
  htmlFor,
  children,
  className = "",
}: LabelProps) {
  return (
    <label
      htmlFor={htmlFor}
      className={`block text-sm font-medium text-gray-700 ${className}`}
    >
      {children}
    </label>
  );
}

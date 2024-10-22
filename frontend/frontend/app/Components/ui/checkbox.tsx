// src/components/ui/checkbox.tsx
import React from 'react';

interface CheckboxProps {
  id: string;
  label: string;
}

export const Checkbox: React.FC<CheckboxProps> = ({ id, label }) => {
  return (
    <label className="flex items-center">
      <input type="checkbox" id={id} className="mr-2" />
      {label}
    </label>
  );
};

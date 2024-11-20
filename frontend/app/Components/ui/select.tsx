import * as React from "react";
import { useState } from "react";

// Select component
export const Select = ({ children }: { children: React.ReactNode }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSelect = () => {
    setIsOpen(!isOpen);
  };

  // Convert children to an array to safely access items
  const childrenArray = React.Children.toArray(children);

  return (
    <div className="relative">
      <div onClick={toggleSelect}>{childrenArray[0]}</div>
      {isOpen && <div className="absolute z-10 bg-white border">{childrenArray[1]}</div>}
    </div>
  );
};

// SelectTrigger component
export const SelectTrigger = ({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) => {
  return <button className={`select-trigger ${className}`}>{children}</button>;
};

// SelectValue component
export const SelectValue = ({ placeholder }: { placeholder: string }) => {
  return <span className="select-value">{placeholder}</span>;
};

// SelectContent component
export const SelectContent = ({ children }: { children: React.ReactNode }) => {
  return <div className="select-content">{children}</div>;
};

// SelectItem component
export const SelectItem = ({
  value,
  children,
  onSelect,
}: {
  value: string;
  children: React.ReactNode;
  onSelect?: (value: string) => void;
}) => {
  const handleClick = () => {
    if (onSelect) {
      onSelect(value);
    }
  };

  return (
    <div
      onClick={handleClick}
      className="p-2 hover:bg-gray-200 cursor-pointer"
    >
      {children}
    </div>
  );
};

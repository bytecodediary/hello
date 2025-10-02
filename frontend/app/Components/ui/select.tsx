import * as React from "react";
import { useMemo, useState } from "react";

type SelectProps = {
  children: React.ReactNode;
  value?: string;
  defaultValue?: string;
  onValueChange?: (value: string) => void;
};

type SelectTriggerProps = {
  children: React.ReactNode;
  className?: string;
  onClick?: () => void;
  selectedValue?: string;
};

type SelectItemProps = {
  value: string;
  children: React.ReactNode;
  onSelect?: (value: string) => void;
};

export const Select: React.FC<SelectProps> = ({ children, value, defaultValue, onValueChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [internalValue, setInternalValue] = useState<string | undefined>(defaultValue);

  const isControlled = value !== undefined;
  const selectedValue = isControlled ? value : internalValue;

  const toggleSelect = () => setIsOpen((prev) => !prev);
  const closeSelect = () => setIsOpen(false);

  const handleSelect = (nextValue: string) => {
    if (!isControlled) {
      setInternalValue(nextValue);
    }
    onValueChange?.(nextValue);
    closeSelect();
  };

  const childrenArray = React.Children.toArray(children) as React.ReactElement[];
  const trigger = childrenArray[0] as React.ReactElement<SelectTriggerProps> | undefined;
  const content = childrenArray[1] as React.ReactElement<SelectContentProps> | undefined;

  const triggerWithProps =
    trigger && React.isValidElement(trigger)
      ? React.cloneElement<SelectTriggerProps>(trigger, {
          onClick: toggleSelect,
          selectedValue,
        })
      : null;

  const contentWithProps =
    isOpen && content && React.isValidElement(content)
      ? React.cloneElement<SelectContentProps>(content, {
          onSelect: handleSelect,
        })
      : null;

  return (
    <div className="relative">
      {triggerWithProps}
      {contentWithProps && (
        <div className="absolute z-10 mt-1 min-w-full border bg-white shadow-md">
          {contentWithProps}
        </div>
      )}
    </div>
  );
};
Select.displayName = "Select";

export const SelectTrigger: React.FC<SelectTriggerProps> = ({
  children,
  className,
  onClick,
  selectedValue,
}) => {
  const enhancedChildren = useMemo(
    () =>
      React.Children.map(children, (child) => {
        if (!React.isValidElement(child)) {
          return child;
        }

        const childElement = child as React.ReactElement;
        const childType = childElement.type as { displayName?: string };
        if (childType.displayName === "SelectValue") {
          return React.cloneElement(childElement, {
            value: selectedValue,
          });
        }
        return childElement;
      }),
    [children, selectedValue]
  );

  return (
    <button
      type="button"
      className={`select-trigger inline-flex items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ${className ?? ""}`}
      onClick={onClick}
    >
      {enhancedChildren}
    </button>
  );
};
SelectTrigger.displayName = "SelectTrigger";

export const SelectValue = ({ placeholder, value }: { placeholder: string; value?: string }) => (
  <span className="select-value text-sm text-muted-foreground">
    {value ?? placeholder}
  </span>
);
SelectValue.displayName = "SelectValue";

type SelectContentProps = {
  children: React.ReactNode;
  onSelect?: (value: string) => void;
};

export const SelectContent: React.FC<SelectContentProps> = ({ children, onSelect }) => {
  const items = React.Children.map(children, (child) => {
    if (!React.isValidElement(child)) {
      return child;
    }

    const childElement = child as React.ReactElement<SelectItemProps>;
    const existingOnSelect = childElement.props.onSelect;

    return React.cloneElement(childElement, {
      onSelect: (nextValue: string) => {
        existingOnSelect?.(nextValue);
        onSelect?.(nextValue);
      },
    });
  });

  return <div className="select-content divide-y divide-muted-foreground/10">{items}</div>;
};
SelectContent.displayName = "SelectContent";

// SelectItem component
export const SelectItem: React.FC<SelectItemProps> = ({
  value,
  children,
  onSelect,
}) => {
  const handleClick = () => {
    onSelect?.(value);
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      className="flex w-full items-center px-3 py-2 text-left text-sm hover:bg-muted"
    >
      {children}
    </button>
  );
};
SelectItem.displayName = "SelectItem";

//Search buttton
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    label: string;
  }
  
  export const ButtonSearch: React.FC<ButtonProps> = ({ label, className, ...props }) => {
    return (
      <button
        className={`px-4 py-2 rounded-md ${className}`}
        {...props}
      >
        {label}
      </button>
    );
  };
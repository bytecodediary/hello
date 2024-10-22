import * as React from "react";
import Link from "next/link"; // Import Link from Next.js
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/app/libs/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-[#bdb0c7] text-[#0e140e] font-bold hover:bg-[#bdb0c7]/90",
        destructive:
          "bg-destructive text-destructive-foreground font-bold hover:bg-destructive/90",
        outline:
          "border border-input bg-background font-bold hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-[#6f9972] text-white font-bold hover:bg-[#6f9972]/80",
        ghost:
          "hover:bg-accent font-bold hover:text-accent-foreground underline-offset-2",
        link: "text-primary underline-offset-4 font-bold hover:underline",
        darker:
          "text-white bg-black rounded-full hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "default",
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  href?: string; // Add href to handle navigation
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, href, ...props }, ref) => {
    const Comp = asChild ? Slot : href ? "a" : "button"; // Render <a> if href is present

    // If href is provided, render a link for Next.js
    if (href) {
      return (
        <Link href={href} passHref legacyBehavior>
          <a
            className={cn(buttonVariants({ variant, size, className }))}
            {...props}
          />
        </Link>
      );
    }

    // Render button normally if href is not provided
    return (
      <button
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);

Button.displayName = "Button";

export { Button, buttonVariants };

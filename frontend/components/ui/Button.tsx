import React from "react";

export interface ButtonProps {
  type?: "button" | "submit" | "reset";
  children: React.ReactNode;
  disabled?: boolean;
  className?: string;
  onClick?: () => void;
}

export function Button({
  type = "button",
  children,
  disabled,
  className,
  onClick,
}: ButtonProps) {
  return (
    <button
      type={type}
      disabled={disabled}
      className={`py-2 px-4 font-medium rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${disabled ? "bg-gray-400" : "bg-blue-600 text-white hover:bg-blue-700"} ${className || ""}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
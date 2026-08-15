import React from "react";

export function Loader({ size = "md" }: { size?: "sm" | "md" | "lg" } = {}) {
  const sizeStyles = {
    sm: "h-4 w-4",
    md: "h-8 w-8",
    lg: "h-12 w-12",
  };

  return (
    <div className={`flex items-center justify-center py-8 ${sizeStyles[size]}`}>
      <span className="animate-spin rounded-full h-full w-full border-4 border-blue-500"></span>
      <span className="ml-4">Loading...</span>
    </div>
  );
}
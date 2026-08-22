'use client';

import React from 'react';

type ButtonVariant = 'primary' | 'secondary' | 'tertiary';
type ButtonSize    = 'sm' | 'md';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  children: React.ReactNode;
}

const VARIANT_STYLES: Record<ButtonVariant, React.CSSProperties> = {
  primary: {
    backgroundColor: '#2eaec2',
    color:           '#0F1419',
    border:          '1px solid transparent',
    fontWeight:      600,
  },
  secondary: {
    backgroundColor: '#2D3748',
    color:           '#A0AEC0',
    border:          '1px solid transparent',
    fontWeight:      400,
  },
  tertiary: {
    backgroundColor: 'transparent',
    color:           '#00D9FF',
    border:          '1px solid #2D3748',
    fontWeight:      400,
  },
};

const SIZE_STYLES: Record<ButtonSize, React.CSSProperties> = {
  sm: { padding: '8px 16px',  fontSize: 13 },
  md: { padding: '12px 24px', fontSize: 14 },
};

const HOVER_STYLES: Record<ButtonVariant, React.CSSProperties> = {
  primary:   { filter: 'brightness(1.1)' },
  secondary: { backgroundColor: '#3D4758' },
  tertiary:  { backgroundColor: '#1A1F2E' },
};

/**
 * Unified button primitive used throughout the FRIDAY interface.
 * Supports three semantic variants and handles hover/active states
 * via inline style toggles for zero external dependency.
 */
const Button: React.FC<ButtonProps> = ({
  variant   = 'secondary',
  size      = 'md',
  isLoading = false,
  disabled,
  children,
  onMouseEnter,
  onMouseLeave,
  style,
  ...rest
}) => {
  const [isHovered, setIsHovered] = React.useState(false);
  const [isPressed, setIsPressed] = React.useState(false);

  const baseStyle: React.CSSProperties = {
    display:      'inline-flex',
    alignItems:   'center',
    justifyContent: 'center',
    gap:          8,
    borderRadius: 8,
    cursor:       disabled || isLoading ? 'not-allowed' : 'pointer',
    opacity:      disabled || isLoading ? 0.5 : 1,
    transition:   'background-color 150ms ease, filter 150ms ease, opacity 150ms ease',
    userSelect:   'none',
    whiteSpace:   'nowrap',
    lineHeight:   1,
    outline:      'none',
    ...VARIANT_STYLES[variant],
    ...SIZE_STYLES[size],
    ...(isHovered && !disabled ? HOVER_STYLES[variant] : {}),
    ...(isPressed && !disabled ? { filter: 'brightness(0.9)' } : {}),
    ...style,
  };

  return (
    <button
      style={baseStyle}
      disabled={disabled || isLoading}
      aria-disabled={disabled || isLoading}
      onMouseEnter={(e) => { setIsHovered(true);  onMouseEnter?.(e); }}
      onMouseLeave={(e) => { setIsHovered(false); setIsPressed(false); onMouseLeave?.(e); }}
      onMouseDown={() => setIsPressed(true)}
      onMouseUp={() => setIsPressed(false)}
      onFocus={() => setIsHovered(true)}
      onBlur={() => setIsHovered(false)}
      {...rest}
    >
      {isLoading ? (
        <span aria-hidden="true" style={{ opacity: 0.7 }}>...</span>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;

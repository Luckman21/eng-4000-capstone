import React from 'react';

interface CheckmarkIconProps extends React.SVGProps<SVGSVGElement> {}

export const CheckmarkIcon: React.FC<CheckmarkIconProps> = (props) => (
    <svg
        aria-hidden="true"
        fill="none"
        focusable="false"
        height="1em"
        role="presentation"
        viewBox="0 0 20 20"
        width="1em"
        {...props}
    >
        <path
            d="M5 10l3 3 7-7"
            stroke="green"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
        />
        <circle
            cx="10"
            cy="10"
            r="9"
            stroke="green"
            strokeWidth={1.5}
        />
    </svg>
);

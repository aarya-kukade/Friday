'use client';

import React from 'react';
import type { ConnectionStatus } from '@/types/voice';

interface StatusIndicatorProps {
  /** Semantic connection status */
  status: ConnectionStatus;
  /** Optional override label */
  label?: string;
  className?: string;
}

/** Dot color by status */
const DOT_COLORS: Record<ConnectionStatus, string> = {
  online:  '#10B981',
  offline: '#EF4444',
};

/**
 * A minimal, accessible status indicator showing a colored dot with a text label.
 * No animation — static for clarity and professionalism.
 */
const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  status,
  label,
  className = '',
}) => {
  const displayLabel = label ?? (status === 'online' ? 'Online' : 'Offline');

  return (
    <span
      className={`inline-flex items-center gap-1.5 ${className}`}
      role="status"
      aria-label={`Connection status: ${displayLabel}`}
    >
      <span
        aria-hidden="true"
        style={{
          display:         'inline-block',
          width:           6,
          height:          6,
          borderRadius:    '50%',
          backgroundColor: DOT_COLORS[status],
          flexShrink:      0,
        }}
      />
      <span
        style={{
          fontSize:   13,
          color:      '#A0AEC0',
          fontWeight: 400,
          lineHeight: 1,
        }}
      >
        {displayLabel}
      </span>
    </span>
  );
};

export default StatusIndicator;

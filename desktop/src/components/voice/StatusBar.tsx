'use client';

import React, { useEffect, useState } from 'react';
import type { StatusBarProps } from '@/types/voice';
import StatusIndicator from '@/components/shared/StatusIndicator';
import styles from './VoiceInterface.module.css';

/** Inline SVG gear icon — no external icon library required. */
const GearIcon: React.FC = () => (
  <svg
    width={16}
    height={16}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.75}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <circle cx="12" cy="12" r="3" />
    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
  </svg>
);

const MODE_LABELS: Record<string, string> = {
  local:  'Local',
  hybrid: 'Hybrid',
  cloud:  'Cloud',
};

/**
 * Sticky top status bar displaying connection status, operating mode,
 * a live 24-hour clock, and a settings trigger.
 */
const StatusBar: React.FC<StatusBarProps> = ({
  connectionStatus,
  operatingMode,
  onSettingsClick,
}) => {
  const [time, setTime] = useState('');

  useEffect(() => {
    const format = () => {
      const now = new Date();
      return now.toLocaleTimeString('en-GB', {
        hour:   '2-digit',
        minute: '2-digit',
        hour12: false,
      });
    };

    setTime(format());
    const id = setInterval(() => setTime(format()), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <header className={styles.statusBar} role="banner">
      <div className={styles.statusBar__left}>
        <StatusIndicator status={connectionStatus} />
        <div className={styles.statusBar__separator} aria-hidden="true" />
        <span className={styles.statusBar__mode} aria-label={`Operating mode: ${MODE_LABELS[operatingMode]}`}>
          {MODE_LABELS[operatingMode]}
        </span>
        <div className={styles.statusBar__separator} aria-hidden="true" />
        <span className={styles.statusBar__label}>FRIDAY</span>
      </div>

      <div className={styles.statusBar__right}>
        <time
          className={styles.statusBar__time}
          dateTime={time}
          aria-label={`Current time: ${time}`}
        >
          {time}
        </time>
        {onSettingsClick && (
          <button
            className={styles.settingsBtn}
            onClick={onSettingsClick}
            aria-label="Open settings"
            type="button"
          >
            <GearIcon />
          </button>
        )}
      </div>
    </header>
  );
};

export default StatusBar;

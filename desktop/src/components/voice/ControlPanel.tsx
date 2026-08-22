'use client';

import React from 'react';
import type { ControlPanelProps } from '@/types/voice';
import Button from '@/components/shared/Button';
import styles from './VoiceInterface.module.css';

/** Inline SVG microphone icon */
const MicIcon: React.FC<{ active?: boolean }> = ({ active = false }) => (
  <svg
    width={15}
    height={15}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={active ? 2 : 1.75}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
    <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
    <line x1="12" y1="19" x2="12" y2="23" />
    <line x1="8"  y1="23" x2="16" y2="23" />
  </svg>
);

/** Inline SVG pause icon */
const PauseIcon: React.FC = () => (
  <svg
    width={14}
    height={14}
    viewBox="0 0 24 24"
    fill="currentColor"
    aria-hidden="true"
  >
    <rect x="6"  y="4" width="4" height="16" rx="1" />
    <rect x="14" y="4" width="4" height="16" rx="1" />
  </svg>
);

/** Inline SVG settings/sliders icon */
const SlidersIcon: React.FC = () => (
  <svg
    width={14}
    height={14}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth={1.75}
    strokeLinecap="round"
    strokeLinejoin="round"
    aria-hidden="true"
  >
    <line x1="4"  y1="6"  x2="20" y2="6"  />
    <line x1="4"  y1="12" x2="20" y2="12" />
    <line x1="4"  y1="18" x2="20" y2="18" />
    <circle cx="8"  cy="6"  r="2" />
    <circle cx="16" cy="12" r="2" />
    <circle cx="10" cy="18" r="2" />
  </svg>
);

/**
 * ControlPanel — The primary action row below the waveform.
 * Shows Start/Stop Listening, Pause (during active states), and Settings.
 * Buttons are disabled during the processing state.
 */
const ControlPanel: React.FC<ControlPanelProps> = ({
  state,
  onStartListening,
  onStopListening,
  onPause,
  onSettingsClick,
}) => {
  const isListening   = state === 'listening';
  const isProcessing  = state === 'processing';
  const isSpeaking    = state === 'speaking';
  const isActive      = isListening || isSpeaking;

  return (
    <div className={styles.controlPanel} role="group" aria-label="Voice controls">
      {/* Primary: Start / Stop */}
      <Button
        variant="primary"
        size="md"
        onClick={isListening ? onStopListening : onStartListening}
        disabled={isProcessing}
        aria-label={isListening ? 'Stop listening' : 'Start listening'}
      >
        <MicIcon active={isListening} />
        {isListening ? 'Stop Listening' : 'Start Listening'}
      </Button>

      {/* Secondary: Pause — visible only during active states */}
      {isActive && (
        <Button
          variant="secondary"
          size="md"
          onClick={onPause}
          aria-label="Pause"
        >
          <PauseIcon />
          Pause
        </Button>
      )}

      {/* Tertiary: Settings — always visible, disabled during processing */}
      <Button
        variant="tertiary"
        size="md"
        onClick={onSettingsClick}
        disabled={isProcessing}
        aria-label="Open settings"
      >
        <SlidersIcon />
        Settings
      </Button>
    </div>
  );
};

export default ControlPanel;

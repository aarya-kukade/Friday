'use client';

import React, { useMemo } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import type { InteractionAreaProps } from '@/types/voice';
import styles from './VoiceInterface.module.css';

const TEXT_ENTER = { opacity: 0, y: 8 };
const TEXT_SHOWN = { opacity: 1, y: 0 };
const TEXT_EXIT  = { opacity: 0, y: -8 };
const TEXT_TRANS = { duration: 0.3, ease: 'easeOut' as const };

/** Splits response text into individually-animated words for a premium reveal. */
const WordReveal: React.FC<{ text: string }> = ({ text }) => {
  const words = useMemo(() => text.split(' '), [text]);
  return (
    <span aria-label={text}>
      {words.map((word, i) => (
        <motion.span
          key={`${i}-${word}`}
          className={styles.responseText__word}
          initial={{ opacity: 0, y: 4 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2, delay: i * 0.03, ease: 'easeOut' }}
          aria-hidden="true"
        >
          {word}{' '}
        </motion.span>
      ))}
    </span>
  );
};

/**
 * InteractionArea — Displays live transcription during listening,
 * the full AI response during speaking, and structured error details on failure.
 * All transitions use a 300ms fade-up to avoid jarring context switches.
 */
const InteractionArea: React.FC<InteractionAreaProps> = ({
  state,
  transcript,
  response,
  error,
}) => {
  return (
    <div
      className={styles.interactionArea}
      aria-live="polite"
      aria-atomic="false"
    >
      <AnimatePresence mode="wait">
        {/* ── Listening: transcription ──────────────────────────────── */}
        {state === 'listening' && transcript && (
          <motion.p
            key="transcript"
            className={styles.transcriptText}
            initial={TEXT_ENTER}
            animate={TEXT_SHOWN}
            exit={TEXT_EXIT}
            transition={TEXT_TRANS}
          >
            {transcript}
          </motion.p>
        )}

        {/* ── Speaking: word-by-word response ──────────────────────── */}
        {state === 'speaking' && response && (
          <motion.p
            key="response"
            className={styles.responseText}
            initial={TEXT_ENTER}
            animate={TEXT_SHOWN}
            exit={TEXT_EXIT}
            transition={TEXT_TRANS}
          >
            <WordReveal text={response} />
          </motion.p>
        )}

        {/* ── Processing: subtle status ─────────────────────────────── */}
        {state === 'processing' && transcript && (
          <motion.p
            key="processing-context"
            className={styles.transcriptText}
            initial={TEXT_ENTER}
            animate={{ ...TEXT_SHOWN, opacity: 0.5 }}
            exit={TEXT_EXIT}
            transition={TEXT_TRANS}
          >
            {transcript}
          </motion.p>
        )}

        {/* ── Error: structured message ─────────────────────────────── */}
        {state === 'error' && error && (
          <motion.div
            key="error"
            className={styles.errorText}
            initial={TEXT_ENTER}
            animate={TEXT_SHOWN}
            exit={TEXT_EXIT}
            transition={{ duration: 0.2, ease: 'easeOut' }}
            role="alert"
          >
            <span className={styles.errorText__label}>Unable to complete request</span>
            {error}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default InteractionArea;

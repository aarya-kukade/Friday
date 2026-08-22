'use client';

import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import type { VoiceWaveformProps } from '@/types/voice';
import styles from './VoiceInterface.module.css';

// ── Constants ────────────────────────────────────────────────────────────────

const BAR_COUNT   = 40;
const BAR_WIDTH   = 6;
const BAR_GAP     = 5;
const BAR_RADIUS  = 3;
const SVG_HEIGHT  = 100;
const MAX_HEIGHT  = 88;
const MIN_HEIGHT  = 4;
const SVG_WIDTH   = BAR_COUNT * BAR_WIDTH + (BAR_COUNT - 1) * BAR_GAP; // 435

// ── Helpers ──────────────────────────────────────────────────────────────────

function clampH(v: number): number {
  return Math.min(MAX_HEIGHT, Math.max(MIN_HEIGHT, Math.round(v)));
}

/** Bell-curve heights for idle — taller in center, tapers to edges */
function buildIdleHeights(): number[] {
  const center = (BAR_COUNT - 1) / 2;
  return Array.from({ length: BAR_COUNT }, (_, i) => {
    const dist = Math.abs(i - center) / center; // 0 center → 1 edge
    // Subtle low profile: 28px center, 4px edges
    return clampH(28 - dist * 24);
  });
}

/** Sine-wave heights for speaking — phase shifts over time */
function buildSpeakingHeights(t: number): number[] {
  return Array.from({ length: BAR_COUNT }, (_, i) => {
    const phase  = (i / BAR_COUNT) * Math.PI * 2.5;
    const wave   = Math.sin(t * 2.8 + phase);
    return clampH(44 + wave * 40);
  });
}

/** Processing — uniform mid-height bars; color handled externally */
const PROCESSING_HEIGHTS = Array.from({ length: BAR_COUNT }, (_, i) => {
  const center = (BAR_COUNT - 1) / 2;
  const dist   = Math.abs(i - center) / center;
  return clampH(70 - dist * 20);
});

/** Error — reduced, flat bars */
const ERROR_HEIGHTS = Array.from({ length: BAR_COUNT }, () => clampH(20));

// Gradient color interpolation: cyan → purple → cyan based on bar index + offset
function processingBarColor(i: number, offset: number): string {
  const t = ((i / (BAR_COUNT - 1)) + offset) % 1;
  // 0 → 0.5: cyan to purple; 0.5 → 1: purple to cyan
  const ease = t < 0.5 ? t * 2 : (1 - t) * 2;
  const r    = Math.round(0   + ease * 124);
  const g    = Math.round(217 - ease * 217);
  const b    = Math.round(255 - ease * 51);
  return `rgb(${r},${g},${b})`;
}

const IDLE_COLOR       = 'rgba(0, 217, 255, 0.55)';
const LISTENING_COLOR  = '#00D9FF';
const SPEAKING_COLOR   = '#7C3AED';
const ERROR_COLOR      = '#EF4444';

// ── Status Label Text ────────────────────────────────────────────────────────

const STATUS_LABELS: Record<string, string> = {
  idle:       'Ready to listen',
  listening:  'Listening',
  processing: 'Processing your request',
  speaking:   'Speaking',
  error:      'Error',
};

// ── Component ────────────────────────────────────────────────────────────────

/**
 * VoiceWaveform — The central audio visualization for the FRIDAY interface.
 *
 * Renders 40 SVG bars animated by Framer Motion across 5 distinct voice states.
 * Listening state uses the real `audioLevel` prop (0–100) from Web Audio API.
 * Processing state cycles a cyan→purple gradient across the bars.
 * Speaking state generates a sine-wave pattern via requestAnimationFrame.
 */
const VoiceWaveform: React.FC<VoiceWaveformProps> = ({
  state       = 'idle',
  audioLevel  = 0,
  error       = null,
}) => {
  const [heights,        setHeights]        = useState<number[]>(() => buildIdleHeights());
  const [gradientOffset, setGradientOffset] = useState(0);

  const rafRef      = useRef<number | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const startRef    = useRef(Date.now());

  const stopAll = useCallback(() => {
    if (rafRef.current      !== null) { cancelAnimationFrame(rafRef.current); rafRef.current = null; }
    if (intervalRef.current !== null) { clearInterval(intervalRef.current);   intervalRef.current = null; }
  }, []);

  // ── Drive heights per state ───────────────────────────────────────────────
  useEffect(() => {
    stopAll();
    startRef.current = Date.now();

    switch (state) {
      case 'idle': {
        setHeights(buildIdleHeights());
        setGradientOffset(0);
        break;
      }

      case 'listening': {
        // 20fps interval — real audio level drives bar heights
        intervalRef.current = setInterval(() => {
          const level = Math.max(audioLevel, 8);
          setHeights(Array.from({ length: BAR_COUNT }, (_, i) => {
            const center = (BAR_COUNT - 1) / 2;
            const dist   = Math.abs(i - center) / center;
            // Energy falls toward edges, plus per-bar noise
            const energy = level * (1 - dist * 0.45);
            const noise  = (Math.random() - 0.5) * 20;
            return clampH(energy + noise);
          }));
        }, 50);
        break;
      }

      case 'processing': {
        setHeights(PROCESSING_HEIGHTS);
        const tick = () => {
          const elapsed = (Date.now() - startRef.current) / 1000;
          setGradientOffset((elapsed / 2) % 1); // 2s cycle
          rafRef.current = requestAnimationFrame(tick);
        };
        rafRef.current = requestAnimationFrame(tick);
        break;
      }

      case 'speaking': {
        const tick = () => {
          const t = (Date.now() - startRef.current) / 1000;
          setHeights(buildSpeakingHeights(t));
          rafRef.current = requestAnimationFrame(tick);
        };
        rafRef.current = requestAnimationFrame(tick);
        break;
      }

      case 'error': {
        setHeights(ERROR_HEIGHTS);
        setGradientOffset(0);
        break;
      }
    }

    return stopAll;
  // audioLevel intentionally excluded — the interval loop reads it on each tick
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state, stopAll]);

  // Re-sync audioLevel into listening interval without restarting the loop
  const audioRef = useRef(audioLevel);
  useEffect(() => { audioRef.current = audioLevel; }, [audioLevel]);

  // ── Bar color by state ────────────────────────────────────────────────────
  const barColor = useCallback(
    (i: number): string => {
      switch (state) {
        case 'idle':       return IDLE_COLOR;
        case 'listening':  return LISTENING_COLOR;
        case 'processing': return processingBarColor(i, gradientOffset);
        case 'speaking':   return SPEAKING_COLOR;
        case 'error':      return ERROR_COLOR;
        default:           return IDLE_COLOR;
      }
    },
    [state, gradientOffset]
  );

  // ── Bar Framer Motion transition ──────────────────────────────────────────
  const transition = useMemo(() => {
    switch (state) {
      case 'listening':  return { duration: 0.05, ease: 'easeOut' as const };
      case 'processing': return { duration: 0.2,  ease: 'easeInOut' as const };
      case 'speaking':   return { duration: 0.1,  ease: 'easeOut' as const };
      default:           return { duration: 0.4,  ease: 'easeOut' as const };
    }
  }, [state]);

  // ── Status label ──────────────────────────────────────────────────────────
  const labelClass = [
    styles.statusLabel,
    state !== 'idle' ? styles[`statusLabel--${state}`] : '',
  ].filter(Boolean).join(' ');

  const svgWrapperClass = [
    styles.waveformSvg,
    styles[`waveformSvg--${state}`] ?? '',
  ].filter(Boolean).join(' ');

  return (
    <div className={styles.waveformContainer}>
      {/* Status label */}
      <AnimatePresence mode="wait">
        <motion.p
          key={state}
          className={labelClass}
          initial={{ opacity: 0, y: 6 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -6 }}
          transition={{ duration: 0.2, ease: 'easeOut' }}
          aria-live="polite"
          aria-atomic="true"
          role="status"
        >
          {state === 'error' && error ? error : STATUS_LABELS[state]}
        </motion.p>
      </AnimatePresence>

      {/* SVG waveform */}
      <div className={svgWrapperClass}>
        <svg
          width={SVG_WIDTH}
          height={SVG_HEIGHT}
          viewBox={`0 0 ${SVG_WIDTH} ${SVG_HEIGHT}`}
          role="img"
          aria-label={`Voice activity visualization — state: ${state}`}
          style={{ overflow: 'visible', maxWidth: '100%' }}
        >
          {heights.map((h, i) => {
            const x   = i * (BAR_WIDTH + BAR_GAP);
            const y   = SVG_HEIGHT - h;
            return (
              <motion.rect
                key={i}
                x={x}
                width={BAR_WIDTH}
                rx={BAR_RADIUS}
                ry={BAR_RADIUS}
                fill={barColor(i)}
                initial={{ y: SVG_HEIGHT, height: MIN_HEIGHT }}
                animate={{ y, height: h }}
                transition={transition}
              />
            );
          })}
        </svg>
      </div>
    </div>
  );
};

export default VoiceWaveform;

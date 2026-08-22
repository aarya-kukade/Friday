'use client';

import { useCallback, useRef, useState } from 'react';
import type { VoiceState } from '@/types/voice';
import { useVoiceStore } from '@/store/voiceStore';

interface UseVoiceStateReturn {
  transitionTo: (next: VoiceState) => void;
  isTransitioning: boolean;
}

const TRANSITION_DURATION_MS = 0;

/**
 * Manages timed, debounced transitions between voice states.
 * Prevents rapid state flickering by enforcing a minimum transition duration.
 */
export function useVoiceState(): UseVoiceStateReturn {
  const { setVoiceState } = useVoiceStore();
  const [isTransitioning, setIsTransitioning] = useState(false);
  const timerRef = useRef<NodeJS.Timeout | null>(null);

  const transitionTo = useCallback(
    (next: VoiceState) => {
      if (timerRef.current) {
        clearTimeout(timerRef.current);
      }
      setIsTransitioning(true);
      timerRef.current = setTimeout(() => {
        setVoiceState(next);
        setIsTransitioning(false);
        timerRef.current = null;
      }, TRANSITION_DURATION_MS);
    },
    [setVoiceState]
  );

  return { transitionTo, isTransitioning };
}

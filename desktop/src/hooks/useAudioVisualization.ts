'use client';

import { useCallback, useEffect, useRef, useState } from 'react';

interface UseAudioVisualizationReturn {
  audioLevel: number;
  start: () => Promise<void>;
  stop: () => void;
  isActive: boolean;
}

/**
 * Uses the Web Audio API AnalyserNode to measure real-time microphone
 * amplitude and return a normalized 0–100 level suitable for waveform display.
 */
export function useAudioVisualization(): UseAudioVisualizationReturn {
  const [audioLevel, setAudioLevel] = useState(0);
  const [isActive, setIsActive] = useState(false);

  const contextRef  = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const streamRef   = useRef<MediaStream | null>(null);
  const rafRef      = useRef<number | null>(null);
  const dataRef     = useRef<Uint8Array<ArrayBuffer> | null>(null);

  const stop = useCallback(() => {
    if (rafRef.current !== null) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    if (contextRef.current && contextRef.current.state !== 'closed') {
      contextRef.current.close().catch(() => undefined);
      contextRef.current = null;
    }
    analyserRef.current = null;
    dataRef.current     = null;
    setAudioLevel(0);
    setIsActive(false);
  }, []);

  const start = useCallback(async () => {
    try {
      // Always stop previous session first
      stop();

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;

      const ctx      = new AudioContext();
      const analyser = ctx.createAnalyser();
      analyser.fftSize            = 256;
      analyser.smoothingTimeConstant = 0.6;

      const source = ctx.createMediaStreamSource(stream);
      source.connect(analyser);

      contextRef.current  = ctx;
      analyserRef.current = analyser;
      dataRef.current     = new Uint8Array(
        new ArrayBuffer(analyser.frequencyBinCount)
      );

      setIsActive(true);

      const tick = () => {
        if (!analyserRef.current || !dataRef.current) return;
        analyserRef.current.getByteFrequencyData(dataRef.current);

        // RMS amplitude of the frequency data
        let sum = 0;
        for (let i = 0; i < dataRef.current.length; i++) {
          sum += dataRef.current[i] * dataRef.current[i];
        }
        const rms       = Math.sqrt(sum / dataRef.current.length);
        const normalized = Math.min(100, Math.round((rms / 128) * 100));

        setAudioLevel(normalized);
        rafRef.current = requestAnimationFrame(tick);
      };

      rafRef.current = requestAnimationFrame(tick);
    } catch {
      // Microphone access denied or unavailable — fall back gracefully
      setIsActive(false);
    }
  }, [stop]);

  // Clean up on unmount
  useEffect(() => () => stop(), [stop]);

  return { audioLevel, start, stop, isActive };
}

'use client';

import { useCallback, useEffect, useRef, useState } from 'react';

type BrowserSpeechRecognitionResult = {
  isFinal: boolean;
  0: {
    transcript: string;
  };
};

type BrowserSpeechRecognitionEvent = {
  resultIndex: number;
  results: ArrayLike<BrowserSpeechRecognitionResult>;
};

type BrowserSpeechRecognitionErrorEvent = {
  error?: string;
};

type BrowserSpeechRecognition = {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  maxAlternatives: number;
  onresult: ((event: BrowserSpeechRecognitionEvent) => void) | null;
  onerror: ((event: BrowserSpeechRecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
  onstart: (() => void) | null;
  start: () => void;
  stop: () => void;
};

type BrowserSpeechRecognitionCtor = new () => BrowserSpeechRecognition;

interface UseVoiceInputReturn {
  transcript: string;
  interimTranscript: string;
  isSupported: boolean;
  start: () => void;
  stop: () => void;
  reset: () => void;
}

const LISTENING_TIMEOUT_MS = 10000; // 10 seconds
const MAX_RETRIES = 3;

/**
 * Wraps the Web Speech API SpeechRecognition for real-time voice transcription.
 * - 10 second listening timeout
 * - Max 3 retries on error
 * - Returns both interim (partial) and final transcript segments
 */
export function useVoiceInput(
  onTranscriptChange?: (text: string) => void,
  onListeningEnd?: () => void
): UseVoiceInputReturn {
  const [transcript,        setTranscript]        = useState('');
  const [interimTranscript, setInterimTranscript] = useState('');
  const [isSupported]                             = useState(
    () => typeof window !== 'undefined' &&
          ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window)
  );

  const recognitionRef = useRef<BrowserSpeechRecognition | null>(null);
  const finalRef       = useRef('');
  const isListeningRef = useRef(false);
  const retryCountRef  = useRef(0);
  const timeoutRef     = useRef<NodeJS.Timeout | null>(null);
  const listeningStartTimeRef = useRef<number>(0);

  const createRecognition = useCallback((): BrowserSpeechRecognition | null => {
    if (!isSupported) return null;

    const SpeechRec =
      (window as typeof window & {
        SpeechRecognition?: BrowserSpeechRecognitionCtor;
        webkitSpeechRecognition?: BrowserSpeechRecognitionCtor;
      })
        .SpeechRecognition ??
      (window as typeof window & {
        webkitSpeechRecognition?: BrowserSpeechRecognitionCtor;
      })
        .webkitSpeechRecognition;

    if (!SpeechRec) return null;

    const rec          = new SpeechRec();
    rec.continuous     = false;  // Don't use continuous mode - we'll manage timeout
    rec.interimResults = true;
    rec.lang           = 'en-US';
    rec.maxAlternatives = 1;

    rec.onstart = () => {
      console.log('[useVoiceInput] Listening started - speak now (10 sec timeout)');
      listeningStartTimeRef.current = Date.now();
    };

    rec.onresult = (event: BrowserSpeechRecognitionEvent) => {
      let interim = '';
      let final   = finalRef.current;

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        if (result.isFinal) {
          final += result[0].transcript + ' ';
          console.log('[useVoiceInput] Final result:', result[0].transcript);
        } else {
          interim += result[0].transcript;
        }
      }

      finalRef.current = final;
      setTranscript(final.trim());
      setInterimTranscript(interim);
      onTranscriptChange?.((final + interim).trim());
    };

    rec.onerror = (event: BrowserSpeechRecognitionErrorEvent) => {
      console.error('[useVoiceInput] Error:', event.error, '(Retry', retryCountRef.current + 1, 'of', MAX_RETRIES, ')');

      // Retry on specific errors, max 3 times
      if (isListeningRef.current && retryCountRef.current < MAX_RETRIES) {
        if (event.error === 'network' || event.error === 'no-speech' || event.error === 'audio-capture') {
          retryCountRef.current++;
          console.log('[useVoiceInput] Retrying... attempt', retryCountRef.current);

          if (timeoutRef.current) clearTimeout(timeoutRef.current);

          timeoutRef.current = setTimeout(() => {
  try {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
  } catch {}

  try {
    if (recognitionRef.current) {
      recognitionRef.current.start();
    }
  } catch (e) {
    console.error(e);
  }
}, 300);
        }
      } else if (isListeningRef.current && retryCountRef.current >= MAX_RETRIES) {
        console.log('[useVoiceInput] Max retries reached, stopping');
        stop();
        onListeningEnd?.();
      }
    };

    rec.onend = () => {
      console.log('[useVoiceInput] Recognition ended');
      
      // Check if we exceeded timeout
      const elapsed = Date.now() - listeningStartTimeRef.current;
      if (elapsed > LISTENING_TIMEOUT_MS) {
        console.log('[useVoiceInput] Timeout reached, stopping listening');
        stop();
        onListeningEnd?.();
      }
    };

    return rec;
  }, [isSupported, onTranscriptChange, onListeningEnd]);

  const start = useCallback(() => {
    console.log('[useVoiceInput] Starting...');
    
    // Clear any pending timers
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }

    if (recognitionRef.current) {
      try { recognitionRef.current.stop(); } catch { }
    }
    
    finalRef.current = '';
    setTranscript('');
    setInterimTranscript('');
    isListeningRef.current = true;
    retryCountRef.current = 0;

    const rec = createRecognition();
    if (!rec) {
      console.error('[useVoiceInput] Speech recognition not supported');
      return;
    }

    recognitionRef.current = rec;
    
    try { 
      rec.start();
      
      // Set 10 second timeout for listening
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      timeoutRef.current = setTimeout(() => {
        console.log('[useVoiceInput] 10 second timeout reached, stopping');
        if (recognitionRef.current) {
          try {
            recognitionRef.current.stop();
          } catch (e) {
            console.error('[useVoiceInput] Error stopping on timeout:', e);
          }
        }
        stop();
      }, LISTENING_TIMEOUT_MS);
    } catch (e) {
      console.error('[useVoiceInput] Failed to start:', e);
      stop();
    }
  }, [createRecognition]);

  const stop = useCallback(() => {
    console.log('[useVoiceInput] Stopping');
    
    isListeningRef.current = false;
    retryCountRef.current = 0;
    
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }

    if (recognitionRef.current) {
      try { recognitionRef.current.stop(); } catch { }
      recognitionRef.current = null;
    }
    
    setInterimTranscript('');
  }, []);

  const reset = useCallback(() => {
    stop();
    finalRef.current = '';
    setTranscript('');
    setInterimTranscript('');
  }, [stop]);

  useEffect(() => {
    return () => {
      isListeningRef.current = false;
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      if (recognitionRef.current) {
        try { recognitionRef.current.stop(); } catch { }
      }
    };
  }, []);

  return { transcript, interimTranscript, isSupported, start, stop, reset };
}

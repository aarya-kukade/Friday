'use client';

import React, { useCallback, useEffect, useRef, useState } from 'react';
import { useVoiceStore } from '@/store/voiceStore';
import { useVoiceInput } from '@/hooks/useVoiceInput';
import { useAudioVisualization } from '@/hooks/useAudioVisualization';
import { useVoiceState } from '@/hooks/useVoiceState';
import StatusBar from './StatusBar';
import VoiceWaveform from './VoiceWaveform';
import InteractionArea from './InteractionArea';
import ControlPanel from './ControlPanel';
import VoiceSettings from './VoiceSettings';
import { fileService } from '@/services/fileService';

const SPEAKING_DISPLAY_MS = 15000;

const VoiceInterface: React.FC = () => {
  const {
    voiceState,
    transcript,
    response,
    error,
    audioLevel,
    connectionStatus,
    operatingMode,
    setTranscript,
    setResponse,
    setAudioLevel,
    setPaused,
    reset,
  } = useVoiceStore();

  const { transitionTo } = useVoiceState();
  const processingTimer = useRef<NodeJS.Timeout | null>(null);
  const speakingTimer = useRef<NodeJS.Timeout | null>(null);
  const [listeningEnded, setListeningEnded] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  const {
    audioLevel: liveLevel,
    start: startAudio,
    stop: stopAudio,
  } = useAudioVisualization();

  useEffect(() => {
    if (voiceState === 'listening') {
      setAudioLevel(liveLevel);
    }
  }, [liveLevel, voiceState, setAudioLevel]);

  const runProcessingFlow = useCallback(async () => {
    if (!transcript.trim()) {
      console.log('[VoiceInterface] No transcript, showing idle message');
      setResponse('I did not catch any speech. Please try again.');
      transitionTo('idle');
      return;
    }

    try {
      console.log('[VoiceInterface] Processing command:', transcript);
      const commandResponse = await fileService.executeVoiceCommand(transcript);
      
      console.log('[VoiceInterface] Command response:', commandResponse);
      setResponse(commandResponse.message || 'Command completed.');
      transitionTo('speaking');

      if (speakingTimer.current) clearTimeout(speakingTimer.current);
      speakingTimer.current = setTimeout(() => {
        console.log('[VoiceInterface] Speaking timeout, transitioning to idle');
        transitionTo('idle');
      }, SPEAKING_DISPLAY_MS);
    } catch (err) {
      console.error('[VoiceInterface] Error executing command:', err);
      setResponse('Failed to execute command.');
      transitionTo('idle');
    }
  }, [transcript, transitionTo, setResponse]);

  const {
    transcript: liveTranscript,
    interimTranscript,
    start: startSpeech,
    stop: stopSpeech,
    reset: resetSpeech,
  } = useVoiceInput(
    (text) => {
      if (voiceState === 'listening') setTranscript(text);
    },
    () => {
      setListeningEnded(true);
    }
  );

  useEffect(() => {
    if (voiceState === 'listening') {
      setTranscript((liveTranscript + (interimTranscript ? ' ' + interimTranscript : '')).trim());
    }
  }, [liveTranscript, interimTranscript, voiceState, setTranscript]);

  useEffect(() => {
    if (voiceState === 'listening' && listeningEnded) {
      setListeningEnded(false);
      stopSpeech();
      stopAudio();
      transitionTo('processing');
      window.setTimeout(() => {
        void runProcessingFlow();
      }, 300);
    }
  }, [voiceState, listeningEnded, stopSpeech, stopAudio, transitionTo, runProcessingFlow]);

  const handleStartListening = useCallback(async () => {
    try {
      if (processingTimer.current) clearTimeout(processingTimer.current);
      if (speakingTimer.current) clearTimeout(speakingTimer.current);

      console.log('[VoiceInterface] Starting listening...');
      setListeningEnded(false);
      reset();
      transitionTo('listening');
      resetSpeech();
      startSpeech();
      await startAudio().catch((err) => {
        console.warn('[VoiceInterface] Audio visualization failed:', err);
      });
    } catch (err) {
      console.error('[VoiceInterface] Error in handleStartListening:', err);
      transitionTo('error');
    }
  }, [transitionTo, reset, resetSpeech, startSpeech, startAudio]);

  const handleStopListening = useCallback(() => {
    try {
      console.log('[VoiceInterface] Stopping listening...');
      stopSpeech();
      stopAudio();
      transitionTo('processing');
      void runProcessingFlow();
    } catch (err) {
      console.error('[VoiceInterface] Error in handleStopListening:', err);
      transitionTo('error');
    }
  }, [stopSpeech, stopAudio, transitionTo, runProcessingFlow]);

  const handlePause = useCallback(() => {
    try {
      console.log('[VoiceInterface] Pausing...');
      stopSpeech();
      stopAudio();
      setPaused(true);
      transitionTo('idle');
    } catch (err) {
      console.error('[VoiceInterface] Error in handlePause:', err);
      transitionTo('error');
    }
  }, [stopSpeech, stopAudio, setPaused, transitionTo]);

  const handleSettingsClick = useCallback(() => {
    try {
      console.log('[VoiceInterface] Opening settings...');
      setIsSettingsOpen(true);
    } catch (err) {
      console.error('[VoiceInterface] Error in handleSettingsClick:', err);
    }
  }, []);

  useEffect(() => {
    return () => {
      if (processingTimer.current) clearTimeout(processingTimer.current);
      if (speakingTimer.current) clearTimeout(speakingTimer.current);
      stopSpeech();
      stopAudio();
    };
  }, [stopSpeech, stopAudio]);

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#0F1419',
      }}
    >
      <StatusBar
        connectionStatus={connectionStatus}
        operatingMode={operatingMode}
        onSettingsClick={handleSettingsClick}
      />

      <main
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '32px 24px',
          gap: '48px',
          maxWidth: 800,
          margin: '0 auto',
          width: '100%',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <h1
            style={{
              fontSize: 32,
              fontWeight: 700,
              color: '#FFFFFF',
              margin: 0,
              lineHeight: 1.2,
              letterSpacing: '-0.01em',
            }}
          >
            FRIDAY
          </h1>
          <p
            style={{
              marginTop: 10,
              fontSize: 16,
              color: '#A0AEC0',
              fontWeight: 400,
              lineHeight: 1.6,
            }}
          >
            Direct voice conversation with AI
          </p>
        </div>

        <VoiceWaveform
          state={voiceState}
          audioLevel={audioLevel}
          transcript={transcript}
          response={response}
          error={error}
        />

        <InteractionArea
          state={voiceState}
          transcript={transcript}
          response={response}
          error={error}
        />

        <ControlPanel
          state={voiceState}
          onStartListening={handleStartListening}
          onStopListening={handleStopListening}
          onPause={handlePause}
          onSettingsClick={handleSettingsClick}
        />
      </main>

      {isSettingsOpen && <VoiceSettings onClose={() => setIsSettingsOpen(false)} />}
    </div>
  );
};

export default VoiceInterface;

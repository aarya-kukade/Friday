/**
 * Represents the current operational state of the FRIDAY voice interface.
 */
export type VoiceState = 'idle' | 'listening' | 'processing' | 'speaking' | 'error';

/**
 * Connection and infrastructure modes for the AI backend.
 */
export type ConnectionStatus = 'online' | 'offline';
export type OperatingMode = 'local' | 'hybrid' | 'cloud';

/**
 * Supported languages for TTS
 */
export type Language = 'en' | 'hi';

/**
 * Voice configuration
 */
export interface VoiceConfig {
  language: Language;
  voice: string;
  speed: number;
}

/**
 * Available voice information
 */
export interface VoiceInfo {
  name: string;
  gender: 'male' | 'female';
  lang: Language;
}

/**
 * Centralized voice interaction context.
 */
export interface VoiceContext {
  state: VoiceState;
  transcript: string;
  response: string;
  /** Microphone audio level (0–100) */
  audioLevel: number;
  isListening: boolean;
  isProcessing: boolean;
  isSpeaking: boolean;
  error: string | null;
  connectionStatus: ConnectionStatus;
  operatingMode: OperatingMode;
  voiceConfig: VoiceConfig;
}

/**
 * Props for the VoiceWaveform component.
 */
export interface VoiceWaveformProps {
  state: VoiceState;
  audioLevel?: number;
  transcript?: string;
  response?: string;
  error?: string | null;
}

/**
 * Props for the StatusBar component.
 */
export interface StatusBarProps {
  connectionStatus: ConnectionStatus;
  operatingMode: OperatingMode;
  onSettingsClick?: () => void;
}

/**
 * Props for the InteractionArea component.
 */
export interface InteractionAreaProps {
  state: VoiceState;
  transcript: string;
  response: string;
  error: string | null;
}

/**
 * Props for the ControlPanel component.
 */
export interface ControlPanelProps {
  state: VoiceState;
  onStartListening: () => void;
  onStopListening: () => void;
  onPause: () => void;
  onSettingsClick: () => void;
}

/**
 * Internal representation of a single rendered waveform bar.
 */
export interface WaveformBar {
  id: number;
  /** Normalized height 0–100 */
  height: number;
  color: string;
}

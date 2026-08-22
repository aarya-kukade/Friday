import { create } from 'zustand';
import { VoiceState, Language } from '@/types/voice';

interface FileItem {
  name: string;
  type: 'file' | 'folder';
  size?: number;
  modified?: string;
}

interface VoiceStore {
  // Voice State
  voiceState: VoiceState;
  transcript: string;
  response: string;
  audioLevel: number;
  isRecording: boolean;
  error: string | null;
  connectionStatus: 'online' | 'offline';
  operatingMode: 'local' | 'hybrid' | 'cloud';
  isPaused: boolean;
  
  // Voice Configuration (Kokoro TTS)
  language: Language;
  currentVoice: string;
  ttsSpeed: number;
  availableVoices: Record<string, any>;
  
  // File Operations
  currentFiles: FileItem[];
  currentDirectory: string;
  lastOperation: {
    type: string;
    result: string;
    timestamp: number;
  } | null;

  // Actions
  setVoiceState: (state: VoiceState) => void;
  setTranscript: (text: string) => void;
  setResponse: (text: string) => void;
  setAudioLevel: (level: number) => void;
  setRecording: (recording: boolean) => void;
  setError: (error: string | null) => void;
  setPaused: (paused: boolean) => void;
  setConnectionStatus: (status: 'online' | 'offline') => void;
  setOperatingMode: (mode: 'local' | 'hybrid' | 'cloud') => void;
  
  // Voice Configuration Actions
  setLanguage: (lang: Language) => void;
  setCurrentVoice: (voice: string) => void;
  setTtsSpeed: (speed: number) => void;
  setAvailableVoices: (voices: Record<string, any>) => void;
  
  // File Operations Actions
  setCurrentFiles: (files: FileItem[]) => void;
  setCurrentDirectory: (dir: string) => void;
  setLastOperation: (op: any) => void;
  
  reset: () => void;
}

export const useVoiceStore = create<VoiceStore>((set) => ({
  // Initial state
  voiceState: 'idle',
  transcript: '',
  response: '',
  audioLevel: 0,
  isRecording: false,
  error: null,
  connectionStatus: 'online',
  operatingMode: 'local',
  isPaused: false,
  
  // Voice Configuration defaults
  language: 'en',
  currentVoice: 'af_bella',  // Default to Bella (English female voice)
  ttsSpeed: 1.0,
  availableVoices: {},
  
  currentFiles: [],
  currentDirectory: '',
  lastOperation: null,
  
  // Setters
  setVoiceState: (state) => set({ voiceState: state }),
  setTranscript: (text) => set({ transcript: text }),
  setResponse: (text) => set({ response: text }),
  setAudioLevel: (level) => set({ audioLevel: Math.max(0, Math.min(100, level)) }),
  setRecording: (recording) => set({ isRecording: recording }),
  setError: (error) => set({ error }),
  setPaused: (paused) => set({ isPaused: paused }),
  setConnectionStatus: (status) => set({ connectionStatus: status }),
  setOperatingMode: (mode) => set({ operatingMode: mode }),
  
  // Voice Configuration Setters
  setLanguage: (lang) => set({ language: lang }),
  setCurrentVoice: (voice) => set({ currentVoice: voice }),
  setTtsSpeed: (speed) => set({ ttsSpeed: Math.max(0.5, Math.min(2.0, speed)) }),
  setAvailableVoices: (voices) => set({ availableVoices: voices }),
  
  setCurrentFiles: (files) => set({ currentFiles: files }),
  setCurrentDirectory: (dir) => set({ currentDirectory: dir }),
  setLastOperation: (op) => set({ lastOperation: op }),
  
  reset: () => set({
    voiceState: 'idle',
    transcript: '',
    response: '',
    audioLevel: 0,
    error: null,
    isPaused: false,
  }),
}));
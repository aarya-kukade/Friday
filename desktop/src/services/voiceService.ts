'use client';

type TranscriptCallback = (transcript: string, isFinal: boolean) => void;
type ErrorCallback = (message: string) => void;

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
  onstart: (() => void) | null;
  onresult: ((event: BrowserSpeechRecognitionEvent) => void) | null;
  onerror: ((event: BrowserSpeechRecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
  start: () => void;
  stop: () => void;
};

type SpeechRecognitionCtor = new () => BrowserSpeechRecognition;

class VoiceService {
  private recognition: BrowserSpeechRecognition | null = null;
  private isListeningRef: boolean = false;
  private restartTimeoutRef: NodeJS.Timeout | null = null;
  private onErrorCallback?: ErrorCallback;
  private audioElement: HTMLAudioElement | null = null;
  private currentLanguage: string = 'en';
  private currentVoice: string = 'af_bella';

  private getFriendlyErrorMessage(error?: string): string {
    switch (error) {
      case 'not-allowed':
      case 'service-not-allowed':
        return 'Microphone access is blocked. Allow mic permission and use Chrome or Edge on localhost.';
      case 'audio-capture':
        return 'No microphone was found. Connect a mic and try again.';
      case 'network':
        return 'Speech recognition will retry... Please speak now.';
      case 'no-speech':
        return 'No speech detected. Please speak louder or closer to the microphone.';
      case 'aborted':
        return 'Speech recognition was stopped. Try again.';
      default:
        return 'Unable to start speech recognition. Use Chrome or Edge and allow microphone access.';
    }
  }

  private getRecognitionCtor(): SpeechRecognitionCtor | null {
    if (typeof window === 'undefined') {
      return null;
    }

    const speechWindow = window as typeof window & {
      SpeechRecognition?: SpeechRecognitionCtor;
      webkitSpeechRecognition?: SpeechRecognitionCtor;
    };

    return speechWindow.SpeechRecognition ?? speechWindow.webkitSpeechRecognition ?? null;
  }

  private restartListening(): void {
    if (!this.isListeningRef) return;

    if (this.restartTimeoutRef) {
      clearTimeout(this.restartTimeoutRef);
    }

    this.restartTimeoutRef = setTimeout(() => {
      try {
        if (this.isListeningRef && this.recognition) {
          this.recognition.start();
        }
      } catch (e) {
        console.error('[VoiceService] Failed to restart:', e);
      }
    }, 500);
  }

  private waitForSpeechSynthesisVoices(timeoutMs = 2000): Promise<SpeechSynthesisVoice[]> {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      return Promise.resolve([]);
    }

    const synth = window.speechSynthesis;
    const voices = synth.getVoices();
    if (voices.length > 0) {
      return Promise.resolve(voices);
    }

    return new Promise((resolve) => {
      const handleVoicesChanged = () => {
        synth.removeEventListener('voiceschanged', handleVoicesChanged);
        resolve(synth.getVoices());
      };

      synth.addEventListener('voiceschanged', handleVoicesChanged);
      setTimeout(() => {
        synth.removeEventListener('voiceschanged', handleVoicesChanged);
        resolve(synth.getVoices());
      }, timeoutMs);
    });
  }

  private async fallbackToBrowserSpeech(message: string, language: string, speed = 1.0): Promise<void> {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      return;
    }

    const utterance = new SpeechSynthesisUtterance(message);
    utterance.lang = language === 'hi' ? 'hi-IN' : 'en-US';
    utterance.rate = Math.max(0.5, Math.min(2.0, speed));
    utterance.pitch = 1;
    utterance.volume = 1;

    const voices = await this.waitForSpeechSynthesisVoices();
    const preferredVoice = voices.find((voice) => voice.lang.startsWith(language === 'hi' ? 'hi' : 'en'));
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }

    return new Promise((resolve) => {
      utterance.onend = () => resolve();
      utterance.onerror = () => resolve();
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utterance);
    });
  }

  public async speakBrowserFallback(message: string, language: string, speed = 1.0): Promise<void> {
    return this.fallbackToBrowserSpeech(message, language, speed);
  }

  startListening(onTranscript: TranscriptCallback, onError?: ErrorCallback): void {
    const RecognitionCtor = this.getRecognitionCtor();

    if (!RecognitionCtor) {
      onError?.('Speech recognition is not supported in this browser.');
      return;
    }

    this.stopListening();
    this.isListeningRef = true;
    this.onErrorCallback = onError;

    const recognition = new RecognitionCtor();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      console.log('[VoiceService] Listening started - speak now...');
    };

    recognition.onresult = (event: BrowserSpeechRecognitionEvent) => {
      let transcript = '';

      for (let index = event.resultIndex; index < event.results.length; index += 1) {
        transcript += event.results[index][0].transcript;
      }

      const latestResult = event.results[event.results.length - 1];
      onTranscript(transcript.trim(), latestResult?.isFinal ?? false);
    };

    recognition.onerror = (event: BrowserSpeechRecognitionErrorEvent) => {
      const msg = this.getFriendlyErrorMessage(event.error);
      onError?.(msg);

      if (event.error === 'not-allowed' || event.error === 'service-not-allowed' || event.error === 'audio-capture') {
        this.isListeningRef = false;
        return;
      }

      if (event.error === 'network' || event.error === 'no-speech') {
        this.restartListening();
      }
    };

    recognition.onend = () => {
      if (this.isListeningRef) {
        this.restartListening();
      }
    };

    try {
      recognition.start();
      this.recognition = recognition;
    } catch (e) {
      console.error('[VoiceService] Failed to start:', e);
      onError?.(this.getFriendlyErrorMessage());
    }
  }

  stopListening(): void {
    this.isListeningRef = false;

    if (this.restartTimeoutRef) {
      clearTimeout(this.restartTimeoutRef);
      this.restartTimeoutRef = null;
    }

    if (!this.recognition) {
      return;
    }

    try {
      this.recognition.stop();
    } catch {
      // Ignore stop failures from already-ended browser sessions.
    } finally {
      this.recognition = null;
    }
  }

  setLanguage(language: 'en' | 'hi'): void {
    this.currentLanguage = language;
  }

  setVoice(voice: string): void {
    this.currentVoice = voice;
  }

  async getAvailableVoices(language: string = 'en'): Promise<Record<string, any>> {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${apiUrl}/api/tts/voices?language=${language}`);
      if (!response.ok) throw new Error('Failed to fetch voices');
      const data = await response.json();
      return data.available_voices || {};
    } catch (error) {
      console.error('Failed to get available voices:', error);
      return {};
    }
  }

  async getAllVoices(): Promise<Record<string, any>> {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const response = await fetch(`${apiUrl}/api/tts/voices/all`);
      if (!response.ok) throw new Error('Failed to fetch all voices');
      return await response.json();
    } catch (error) {
      console.error('Failed to get all voices:', error);
      return {};
    }
  }

  async speak(
    message: string,
    onEnd?: () => void,
    language?: string,
    voice?: string,
    speed?: number
  ): Promise<void> {
    if (typeof window === 'undefined') {
      onEnd?.();
      return;
    }

    const lang = language || this.currentLanguage;
    const voiceCode = voice || this.currentVoice;

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';
      const speedValue = typeof speed === 'number' ? Math.max(0.5, Math.min(2.0, speed)) : 1.0;
      const response = await fetch(`${apiUrl}/api/tts/synthesize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: message,
          voice: voiceCode,
          language: lang,
          speed: speedValue,
        }),
      });

      if (!response.ok) {
        throw new Error(`TTS synthesis failed: ${response.statusText}`);
      }

      const isFallback = response.headers.get('x-kokoro-fallback') === 'true';
      const audioBlob = await response.blob();

      if (isFallback || audioBlob.size < 5000) {
        console.log('[VoiceService] Using browser speech synthesis fallback');
        await this.fallbackToBrowserSpeech(message, lang, speedValue);
        onEnd?.();
        return;
      }

      const audioUrl = URL.createObjectURL(audioBlob);

      if (!this.audioElement) {
        this.audioElement = new Audio();
      }

      this.audioElement.pause();
      this.audioElement.currentTime = 0;

      const handleEnd = () => {
        URL.revokeObjectURL(audioUrl);
        onEnd?.();
      };

      this.audioElement.onended = handleEnd;
      this.audioElement.onerror = handleEnd;
      this.audioElement.src = audioUrl;
      await this.audioElement.play();
    } catch (error) {
      console.error('Kokoro TTS error:', error);
      await this.fallbackToBrowserSpeech(message, lang);
      onEnd?.();
    }
  }

  stopSpeaking(): void {
    if (this.audioElement) {
      this.audioElement.pause();
      this.audioElement.currentTime = 0;
    }
  }
}

export const voiceService = new VoiceService();

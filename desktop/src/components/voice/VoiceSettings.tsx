'use client';

import React, { useEffect, useState } from 'react';
import { useVoiceStore } from '@/store/voiceStore';
import { voiceService } from '@/services/voiceService';

interface VoiceOption {
  code: string;
  name: string;
  gender: string;
}

/**
 * VoiceSettings Component
 * Allows users to configure voice language and voice selection
 */
const VoiceSettings: React.FC<{
  onClose?: () => void;
}> = ({ onClose }) => {
  const store = useVoiceStore();
  const [voices, setVoices] = useState<Record<string, VoiceOption>>({});
  const [englishVoices, setEnglishVoices] = useState<VoiceOption[]>([]);
  const [hindiVoices, setHindiVoices] = useState<VoiceOption[]>([]);
  const [loading, setLoading] = useState(true);

  // Load available voices on mount
  useEffect(() => {
    const loadVoices = async () => {
      try {
        setLoading(true);
        
        // Fetch all available voices
        const allVoices = await voiceService.getAllVoices();
        
        // Process English voices
        const enVoices: VoiceOption[] = Object.entries(allVoices.en || {}).map(
          ([code, info]: [string, any]) => ({
            code: code.startsWith('a') ? code : `a_${code}`,
            name: info.name,
            gender: info.gender,
          })
        );
        
        // Process Hindi voices
        const hiVoices: VoiceOption[] = Object.entries(allVoices.hi || {}).map(
          ([code, info]: [string, any]) => ({
            code: code.startsWith('hi_') ? code : `hi_${code}`,
            name: info.name,
            gender: info.gender,
          })
        );
        
        setEnglishVoices(enVoices);
        setHindiVoices(hiVoices);
      } catch (error) {
        console.error('Failed to load voices:', error);
        // Provide default voices on error
        setEnglishVoices([
          { code: 'af_bella', name: 'Bella', gender: 'female' },
          { code: 'af_abreeze', name: 'Abreeze', gender: 'female' },
          { code: 'af_sarah', name: 'Sarah', gender: 'female' },
          { code: 'af_nicole', name: 'Nicole', gender: 'female' },
          { code: 'am_alpha', name: 'Alpha', gender: 'male' },
          { code: 'am_charlie', name: 'Charlie', gender: 'male' },
          { code: 'am_josh', name: 'Josh', gender: 'male' },
        ]);
        setHindiVoices([
          { code: 'hi_maya', name: 'Maya', gender: 'female' },
          { code: 'hi_arjun', name: 'Arjun', gender: 'male' },
        ]);
      } finally {
        setLoading(false);
      }
    };

    loadVoices();
  }, []);

  const handleLanguageChange = (lang: 'en' | 'hi') => {
    store.setLanguage(lang);
    voiceService.setLanguage(lang);
    
    // Set default voice for language
    if (lang === 'en' && englishVoices.length > 0) {
      const defaultVoice = englishVoices[0].code;
      store.setCurrentVoice(defaultVoice);
      voiceService.setVoice(defaultVoice);
    } else if (lang === 'hi' && hindiVoices.length > 0) {
      const defaultVoice = hindiVoices[0].code;
      store.setCurrentVoice(defaultVoice);
      voiceService.setVoice(defaultVoice);
    }
  };

  const handleVoiceChange = (voiceCode: string) => {
    store.setCurrentVoice(voiceCode);
    voiceService.setVoice(voiceCode);
  };

  const handleSpeedChange = (speed: number) => {
    store.setTtsSpeed(speed);
  };

  const currentVoices = store.language === 'en' ? englishVoices : hindiVoices;

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        style={{
          backgroundColor: '#1a1f2e',
          borderRadius: '12px',
          padding: '24px',
          maxWidth: '500px',
          width: '90%',
          boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)',
          border: '1px solid rgba(138, 43, 226, 0.3)',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 style={{ margin: '0 0 20px 0', color: '#fff', fontSize: '20px' }}>
          Voice Settings
        </h2>

        {/* Language Selection */}
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', color: '#a0a0a0', marginBottom: '8px', fontSize: '14px' }}>
            Language
          </label>
          <div style={{ display: 'flex', gap: '8px' }}>
            {(['en', 'hi'] as const).map((lang) => (
              <button
                key={lang}
                onClick={() => handleLanguageChange(lang)}
                style={{
                  flex: 1,
                  padding: '10px 16px',
                  borderRadius: '8px',
                  border: 'none',
                  backgroundColor: store.language === lang ? '#8a2be2' : '#2a2f3f',
                  color: '#fff',
                  cursor: 'pointer',
                  fontWeight: store.language === lang ? '600' : '400',
                  transition: 'all 0.2s',
                }}
              >
                {lang === 'en' ? '🇬🇧 English' : '🇮🇳 हिंदी'}
              </button>
            ))}
          </div>
        </div>

        {/* Voice Selection */}
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', color: '#a0a0a0', marginBottom: '8px', fontSize: '14px' }}>
            Voice
          </label>
          {loading ? (
            <div style={{ color: '#a0a0a0', textAlign: 'center', padding: '12px' }}>
              Loading voices...
            </div>
          ) : (
            <select
              value={store.currentVoice}
              onChange={(e) => handleVoiceChange(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px',
                borderRadius: '8px',
                border: '1px solid rgba(138, 43, 226, 0.3)',
                backgroundColor: '#2a2f3f',
                color: '#fff',
                cursor: 'pointer',
                fontSize: '14px',
              }}
            >
              {currentVoices.map((voice) => (
                <option key={voice.code} value={voice.code}>
                  {voice.name} ({voice.gender})
                </option>
              ))}
            </select>
          )}
        </div>

        {/* Speed Selection */}
        <div style={{ marginBottom: '24px' }}>
          <label style={{ display: 'block', color: '#a0a0a0', marginBottom: '8px', fontSize: '14px' }}>
            Speech Speed: {store.ttsSpeed.toFixed(1)}x
          </label>
          <input
            type="range"
            min="0.5"
            max="2.0"
            step="0.1"
            value={store.ttsSpeed}
            onChange={(e) => handleSpeedChange(parseFloat(e.target.value))}
            style={{
              width: '100%',
              height: '6px',
              borderRadius: '3px',
              backgroundColor: '#2a2f3f',
              outline: 'none',
              cursor: 'pointer',
              accentColor: '#8a2be2',
            }}
          />
          <div style={{ fontSize: '12px', color: '#707080', marginTop: '4px' }}>
            0.5x (Slow) - 2.0x (Fast)
          </div>
        </div>

        {/* Test Button */}
        <div style={{ marginBottom: '16px' }}>
          <button
            onClick={async () => {
              const testText = store.language === 'en'
                ? "This is a test of the Kokoro text to speech engine."
                : "यह कोकोरो टेक्स्ट टू स्पीच इंजन का परीक्षण है।";

              try {
                await voiceService.speak(
                  testText,
                  undefined,
                  store.language,
                  store.currentVoice,
                  store.ttsSpeed
                );
              } catch (error) {
                console.error('Voice test failed:', error);
                await voiceService.speakBrowserFallback(testText, store.language, store.ttsSpeed);
              }
            }}
            style={{
              width: '100%',
              padding: '10px 16px',
              borderRadius: '8px',
              border: 'none',
              backgroundColor: '#4a9eff',
              color: '#fff',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '14px',
              transition: 'all 0.2s',
            }}
            onMouseOver={(e) => (e.currentTarget.style.backgroundColor = '#3a8eef')}
            onMouseOut={(e) => (e.currentTarget.style.backgroundColor = '#4a9eff')}
          >
            🔊 Test Voice
          </button>
        </div>

        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            width: '100%',
            padding: '10px 16px',
            borderRadius: '8px',
            border: '1px solid rgba(138, 43, 226, 0.3)',
            backgroundColor: 'transparent',
            color: '#a0a0a0',
            cursor: 'pointer',
            fontWeight: '500',
            fontSize: '14px',
            transition: 'all 0.2s',
          }}
          onMouseOver={(e) => (e.currentTarget.style.backgroundColor = 'rgba(138, 43, 226, 0.1)')}
          onMouseOut={(e) => (e.currentTarget.style.backgroundColor = 'transparent')}
        >
          Close
        </button>

        {/* Info Section */}
        <div
          style={{
            marginTop: '20px',
            padding: '12px',
            backgroundColor: 'rgba(74, 158, 255, 0.1)',
            borderRadius: '8px',
            borderLeft: '3px solid #4a9eff',
            fontSize: '12px',
            color: '#a0a0a0',
          }}
        >
          <strong style={{ color: '#4a9eff' }}>💡 Tip:</strong> Select your preferred language and voice for the FRIDAY AI assistant. Test the voice to hear how it sounds before confirming.
        </div>
      </div>
    </div>
  );
};

export default VoiceSettings;

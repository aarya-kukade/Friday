/**
 * Voice Handler Hook
 * Manages voice input/output and command execution
 */

import { useCallback, useRef } from 'react';
import { voiceService } from '@/services/voiceService';
import { fileService } from '@/services/fileService';
import { useVoiceStore } from '@/store/voiceStore';

export const useVoiceHandler = () => {
  const store = useVoiceStore();
  const stopRequestedRef = useRef(false);

  /**
   * Stable ref to processCommand so startListening/stopListening can call it
   * without creating a circular useCallback dependency chain.
   */
  const processCommandRef = useRef<((transcription: string) => Promise<void>) | null>(null);

  const processCommand = useCallback(
    async (transcription: string) => {
      const cleanedTranscription = transcription.trim();

      if (!cleanedTranscription) {
        store.setRecording(false);
        store.setVoiceState('idle');
        return;
      }

      stopRequestedRef.current = false;
      store.setRecording(false);
      store.setVoiceState('processing');
      store.setTranscript(cleanedTranscription);
      store.setError(null);

      try {
        // Send to backend for parsing and execution
        const commandResponse = await fileService.executeVoiceCommand(
          cleanedTranscription
        );

        if (commandResponse.status === 'success') {
          const message = commandResponse.message;
          store.setResponse(message);
          store.setError(null);
          store.setVoiceState('speaking');

          // Speak the response using configured language and voice
          await voiceService.speak(
            message,
            () => {
              store.setVoiceState('idle');
            },
            store.language,
            store.currentVoice
          );

          // Update file list if needed
          if (
            commandResponse.command_type === 'list_files' ||
            commandResponse.command_type === 'create_file' ||
            commandResponse.command_type === 'delete_file' ||
            commandResponse.command_type === 'rename_file' ||
            commandResponse.command_type === 'update_file'
          ) {
            const filesResponse = await fileService.listFiles();
            if (filesResponse.status === 'success') {
              store.setCurrentFiles(filesResponse.files || []);
            }
          }

          store.setLastOperation({
            type: commandResponse.command_type,
            result: message,
            timestamp: Date.now(),
          });
        } else {
          store.setError(commandResponse.message);
          store.setResponse(commandResponse.message);
          await voiceService.speak(
            commandResponse.message,
            undefined,
            store.language,
            store.currentVoice
          );
        }
      } catch (error: unknown) {
        const errorMsg =
          error instanceof Error ? error.message : 'An error occurred';
        store.setError(errorMsg);
        store.setResponse(errorMsg);
        await voiceService.speak(
          errorMsg,
          undefined,
          store.language,
          store.currentVoice
        );
      }
    },
    [store]
  );

  // Keep the ref in sync with the latest processCommand without adding it as a dep
  processCommandRef.current = processCommand;

  const startListening = useCallback(async () => {
    stopRequestedRef.current = false;
    store.setVoiceState('listening');
    store.setRecording(true);
    store.setTranscript('');
    store.setResponse('');
    store.setError(null);

    voiceService.startListening(
      async (transcript, isFinal) => {
        if (stopRequestedRef.current) return;

        store.setTranscript(transcript);

        if (isFinal) {
          await processCommandRef.current?.(transcript);
        }
      },
      (error) => {
        if (stopRequestedRef.current) return;

        store.setRecording(false);
        store.setError(error);
        store.setResponse(error);
      }
    );
  }, [store]);

  const stopListening = useCallback(() => {
    const transcript = useVoiceStore.getState().transcript;

    stopRequestedRef.current = true;
    voiceService.stopListening();
    store.setRecording(false);

    if (transcript.trim()) {
      void processCommandRef.current?.(transcript);
      return;
    }

    store.setVoiceState('idle');
  }, [store]);

  return {
    startListening,
    stopListening,
    processCommand,
  };
};

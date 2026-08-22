export type FileOperationResponse = {
  status: 'success' | 'error';
  message: string;
  [key: string]: unknown;
};

export type VoiceCommandResponse = {
  status: 'success' | 'error';
  message: string;
  command_type: string;
  result?: FileOperationResponse;
};

export type FileEntry = {
  name: string;
  type: 'file' | 'folder';
};

type ListFilesResponse = {
  status: 'success' | 'error';
  files?: FileEntry[];
  message?: string;
  directory?: string;
  count?: number;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

class FileService {
  private async request<T>(path: string, init?: RequestInit): Promise<T> {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      headers: {
        'Content-Type': 'application/json',
        ...(init?.headers ?? {}),
      },
      ...init,
    });

    const payload = (await response.json()) as T | { detail?: string };

    if (!response.ok) {
      throw new Error(
        typeof payload === 'object' && payload && 'detail' in payload
          ? payload.detail || `Request failed with status ${response.status}`
          : `Request failed with status ${response.status}`
      );
    }

    return payload as T;
  }

  async listFiles(directory = ''): Promise<ListFilesResponse> {
    try {
      const query = directory
        ? `?directory=${encodeURIComponent(directory)}`
        : '';

      return await this.request<ListFilesResponse>(`/api/files/list${query}`, {
        method: 'GET',
      });
    } catch (error) {
      return {
        status: 'error',
        message:
          error instanceof Error
            ? error.message
            : 'Unable to list files.',
      };
    }
  }

  async executeVoiceCommand(transcription: string): Promise<VoiceCommandResponse> {
    try {
      return await this.request<VoiceCommandResponse>('/api/voice/execute', {
        method: 'POST',
        body: JSON.stringify({ transcription }),
      });
    } catch (error) {
      return {
        status: 'error',
        message:
          error instanceof Error
            ? error.message
            : 'Unable to process the voice command.',
        command_type: 'unknown',
      };
    }
  }
}

export const fileService = new FileService();

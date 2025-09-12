import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const API_BASE_URL = 'http://localhost:8000/api/v1';

// Types for API responses
export interface BreachExposure {
  id: number;
  breach_name: string;
  breach_date: string;
  breach_description: string;
  data_classes: string[];
  severity: string;
  source: string;
  source_id: string;
  created_at: string;
}

export interface IPReputation {
  ip_address: string;
  abuse_confidence_score: number;
  country_code: string;
  usage_type: string;
  isp: string;
  domain: string;
  total_reports: number;
  num_distinct_users: number;
  last_reported_at: string;
}

export interface PhishingCheckResult {
  url: string;
  is_phishing: boolean;
  confidence: number;
  threat_type: string;
  description: string;
  timestamp: string;
}

export interface ChatSession {
  id: number;
  session_id: string;
  user_id: number;
  fraud_type: string | null;
  status: string;
  vulnerability_factors: string[];
  created_at: string;
  updated_at: string;
  last_activity: string;
}

export interface ChatMessage {
  id: number;
  session_id: number;
  message_type: 'user' | 'bot' | 'system';
  content: string;
  metadata: Record<string, any>;
  ai_model: string | null;
  ai_confidence: number | null;
  ai_reasoning: string | null;
  created_at: string;
}

export interface ChatSessionCreate {
  fraud_type?: string;
  vulnerability_factors?: string[];
}

export interface ChatMessageCreate {
  content: string;
  metadata?: Record<string, any>;
}

export interface ChatSessionResponse {
  id: number;
  session_id: string;
  user_id: number;
  fraud_type: string | null;
  status: string;
  vulnerability_factors: string[];
  created_at: string;
  updated_at: string;
  last_activity: string;
}

export interface ChatMessageResponse {
  id: number;
  session_id: number;
  message_type: 'user' | 'bot' | 'system';
  content: string;
  metadata: Record<string, any>;
  ai_model: string | null;
  ai_confidence: number | null;
  ai_reasoning: string | null;
  created_at: string;
}

// API functions
export const api = {
  // Health check
  health: async () => {
    const response = await fetch(`${API_BASE_URL.replace('/api/v1', '')}/healthz`);
    return response.json();
  },

  // Email breach check
  checkEmailBreaches: async (email: string): Promise<BreachExposure[]> => {
    const response = await fetch(`${API_BASE_URL}/threat-intelligence/breach-check/${encodeURIComponent(email)}`);
    if (!response.ok) {
      throw new Error('Failed to check email breaches');
    }
    return response.json();
  },

  // IP reputation check
  checkIPReputation: async (ip: string): Promise<IPReputation> => {
    const response = await fetch(`${API_BASE_URL}/threat-intelligence/ip-check/${encodeURIComponent(ip)}`);
    if (!response.ok) {
      throw new Error('Failed to check IP reputation');
    }
    return response.json();
  },

  // Phishing URL check
  checkPhishingURL: async (url: string): Promise<PhishingCheckResult> => {
    const response = await fetch(`${API_BASE_URL}/threat-intelligence/phishing-check`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });
    if (!response.ok) {
      throw new Error('Failed to check phishing URL');
    }
    return response.json();
  },

  // Get threat statistics
  getThreatStats: async (): Promise<ThreatStats> => {
    const response = await fetch(`${API_BASE_URL}/threat-intelligence/stats`);
    if (!response.ok) {
      throw new Error('Failed to fetch threat statistics');
    }
    return response.json();
  },

  // Get IOCs
  getIOCs: async (skip = 0, limit = 100) => {
    const response = await fetch(`${API_BASE_URL}/threat-intelligence/iocs?skip=${skip}&limit=${limit}`);
    if (!response.ok) {
      throw new Error('Failed to fetch IOCs');
    }
    return response.json();
  },

  // Get threat alerts
  getThreatAlerts: async (skip = 0, limit = 100) => {
    const response = await fetch(`${API_BASE_URL}/threat-intelligence/alerts?skip=${skip}&limit=${limit}`);
    if (!response.ok) {
      throw new Error('Failed to fetch threat alerts');
    }
    return response.json();
  },

  // Chatbot API functions (No auth required)
  // Create a new chat session
  createChatSession: async (sessionData: ChatSessionCreate): Promise<ChatSessionResponse> => {
    const response = await fetch(`${API_BASE_URL}/chatbot/sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(sessionData),
    });
    if (!response.ok) {
      throw new Error('Failed to create chat session');
    }
    return response.json();
  },

  // Send a message and get AI response
  sendChatMessage: async (sessionId: string, message: ChatMessageCreate): Promise<ChatMessageResponse> => {
    const response = await fetch(`${API_BASE_URL}/chatbot/sessions/${sessionId}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(message),
    });
    if (!response.ok) {
      throw new Error('Failed to send chat message');
    }
    return response.json();
  },

  // Get chat messages for a session
  getChatMessages: async (sessionId: string, skip = 0, limit = 100): Promise<ChatMessageResponse[]> => {
    const response = await fetch(`${API_BASE_URL}/chatbot/sessions/${sessionId}/messages?skip=${skip}&limit=${limit}`);
    if (!response.ok) {
      throw new Error('Failed to fetch chat messages');
    }
    return response.json();
  },

  // Get all chat sessions for the current user
  getChatSessions: async (skip = 0, limit = 100): Promise<ChatSessionResponse[]> => {
    const response = await fetch(`${API_BASE_URL}/chatbot/sessions?skip=${skip}&limit=${limit}`);
    if (!response.ok) {
      throw new Error('Failed to fetch chat sessions');
    }
    return response.json();
  },

  // Authentication API functions
  login: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      throw new Error('Login failed');
    }
    return response.json();
  },

  register: async (email: string, password: string, name: string) => {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password, name }),
    });
    if (!response.ok) {
      throw new Error('Registration failed');
    }
    return response.json();
  },

  getCurrentUser: async () => {
    const token = localStorage.getItem('auth_token');
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      },
    });
    if (!response.ok) {
      throw new Error('Failed to get current user');
    }
    return response.json();
  },
};

// React Query hooks
export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: api.health,
    refetchInterval: 30000, // Check every 30 seconds
  });
};

export const useEmailBreachCheck = (email: string, enabled = false) => {
  return useQuery({
    queryKey: ['email-breaches', email],
    queryFn: () => api.checkEmailBreaches(email),
    enabled: enabled && email.length > 0,
    retry: 1,
  });
};

export const useIPReputationCheck = (ip: string, enabled = false) => {
  return useQuery({
    queryKey: ['ip-reputation', ip],
    queryFn: () => api.checkIPReputation(ip),
    enabled: enabled && ip.length > 0,
    retry: 1,
  });
};

export const usePhishingCheck = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: api.checkPhishingURL,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['threat-stats'] });
    },
  });
};

export const useThreatStats = () => {
  return useQuery({
    queryKey: ['threat-stats'],
    queryFn: api.getThreatStats,
    refetchInterval: 60000, // Refresh every minute
  });
};

export const useIOCs = (skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ['iocs', skip, limit],
    queryFn: () => api.getIOCs(skip, limit),
    refetchInterval: 300000, // Refresh every 5 minutes
  });
};

export const useThreatAlerts = (skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ['threat-alerts', skip, limit],
    queryFn: () => api.getThreatAlerts(skip, limit),
    refetchInterval: 300000, // Refresh every 5 minutes
  });
};

// Chatbot React Query hooks
export const useCreateChatSession = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: api.createChatSession,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['chat-sessions'] });
    },
  });
};

export const useSendChatMessage = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ sessionId, message }: { sessionId: string; message: ChatMessageCreate }) => 
      api.sendChatMessage(sessionId, message),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['chat-messages', variables.sessionId] });
    },
  });
};

export const useChatMessages = (sessionId: string | null, skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ['chat-messages', sessionId, skip, limit],
    queryFn: () => sessionId ? api.getChatMessages(sessionId, skip, limit) : Promise.resolve([]),
    enabled: !!sessionId,
    refetchOnWindowFocus: false, // Disable auto-refresh
  });
};

export const useChatSessions = (skip = 0, limit = 100) => {
  return useQuery({
    queryKey: ['chat-sessions', skip, limit],
    queryFn: () => api.getChatSessions(skip, limit),
    refetchOnWindowFocus: false, // Disable auto-refresh
  });
};

// Authentication React Query hooks
export const useLogin = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) => 
      api.login(email, password),
    onSuccess: (data) => {
      localStorage.setItem('auth_token', data.access_token);
      queryClient.invalidateQueries({ queryKey: ['auth'] });
    },
  });
};

export const useRegister = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ email, password, name }: { email: string; password: string; name: string }) => 
      api.register(email, password, name),
    onSuccess: (data) => {
      localStorage.setItem('auth_token', data.access_token);
      queryClient.invalidateQueries({ queryKey: ['auth'] });
    },
  });
};

export const useCurrentUser = () => {
  return useQuery({
    queryKey: ['auth', 'current-user'],
    queryFn: api.getCurrentUser,
    enabled: !!localStorage.getItem('auth_token'),
    retry: false,
  });
};

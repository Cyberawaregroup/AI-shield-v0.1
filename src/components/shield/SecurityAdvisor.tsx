import { useState, useEffect } from "react";
import { MessageCircle, Shield, AlertTriangle, CheckCircle, Globe, Mail, Phone, Loader2, Send, Bot, User, Link, Trash2, RefreshCw } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  api, 
  useCreateChatSession, 
  useSendChatMessage, 
  useChatMessages, 
  useChatSessions,
  ChatMessageResponse,
  ChatSessionResponse
} from "@/lib/api";
import { toast } from "sonner";

interface ChatMessage {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: Date;
  aiModel?: string;
  aiConfidence?: number;
  aiReasoning?: string;
}

export default function SecurityAdvisor() {
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [email, setEmail] = useState("");
  const [isChecking, setIsChecking] = useState(false);
  const [breaches, setBreaches] = useState<any[]>([]);
  const [hasChecked, setHasChecked] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [isLoadingChat, setIsLoadingChat] = useState(false);

  // API hooks
  const createSessionMutation = useCreateChatSession();
  const sendMessageMutation = useSendChatMessage();
  const { data: chatSessions, refetch: refetchSessions } = useChatSessions();
  const { data: apiMessages, refetch: refetchMessages } = useChatMessages(currentSessionId);

  // Convert API messages to local format
  useEffect(() => {
    if (apiMessages) {
      const convertedMessages: ChatMessage[] = apiMessages.map((msg: ChatMessageResponse) => ({
        id: msg.id.toString(),
        content: msg.content,
        isUser: msg.message_type === 'user',
        timestamp: new Date(msg.created_at),
        aiModel: msg.ai_model || undefined,
        aiConfidence: msg.ai_confidence || undefined,
        aiReasoning: msg.ai_reasoning || undefined,
      }));
      setChatMessages(convertedMessages);
    }
  }, [apiMessages]);

  // Create initial session on component mount
  useEffect(() => {
    if (!currentSessionId && !createSessionMutation.isPending) {
      createSessionMutation.mutate({
        fraud_type: 'general_security',
        vulnerability_factors: []
      }, {
        onSuccess: (session: ChatSessionResponse) => {
          setCurrentSessionId(session.session_id);
          toast.success("Chat session started!");
        },
        onError: (error) => {
          console.error("Failed to create chat session:", error);
          toast.error("Failed to start chat session. Please refresh the page.");
        }
      });
    }
  }, [currentSessionId, createSessionMutation]);

  // Handle authentication errors
  useEffect(() => {
    if (createSessionMutation.error || sendMessageMutation.error) {
      const error = createSessionMutation.error || sendMessageMutation.error;
      if (error && 'status' in error && error.status === 401) {
        toast.error("Authentication expired. Please login again.");
        // Don't auto-refresh, let user manually login
      }
    }
  }, [createSessionMutation.error, sendMessageMutation.error]);

  const handleEmailCheck = async () => {
    if (!email || !email.includes('@')) {
      toast.error("Please enter a valid email address");
      return;
    }
    
    setIsChecking(true);
    setHasChecked(true);
    setBreaches([]);
    
    try {
      const result = await api.checkEmailBreaches(email);
      setBreaches(result);
      
      if (result && result.length > 0) {
        toast.warning(`Found ${result.length} breach(es) for this email!`);
      } else {
        toast.success("No breaches found for this email address.");
      }
    } catch (error) {
      console.error("Error checking breaches:", error);
      toast.error("Failed to check email breaches. Please try again.");
    } finally {
      setIsChecking(false);
    }
  };

  const handleChatSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim() || !currentSessionId || sendMessageMutation.isPending) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: chatInput.trim(),
      isUser: true,
      timestamp: new Date()
    };

    // Add user message immediately to UI
    setChatMessages(prev => [...prev, userMessage]);
    const inputValue = chatInput.trim();
    setChatInput("");
    setIsLoadingChat(true);

    try {
      // Send message to API
      await sendMessageMutation.mutateAsync({
        sessionId: currentSessionId,
        message: {
          content: inputValue,
          metadata: {
            timestamp: new Date().toISOString(),
            user_agent: navigator.userAgent
          }
        }
      });

      // Refresh messages to get AI response
      await refetchMessages();
      
    } catch (error) {
      console.error("Error sending message:", error);
      toast.error("Failed to send message. Please try again.");
      
      // Remove the user message if sending failed
      setChatMessages(prev => prev.filter(msg => msg.id !== userMessage.id));
    } finally {
      setIsLoadingChat(false);
    }
  };

  const handleNewSession = async () => {
    try {
      const session = await createSessionMutation.mutateAsync({
        fraud_type: 'general_security',
        vulnerability_factors: []
      });
      setCurrentSessionId(session.session_id);
      setChatMessages([]);
      toast.success("New chat session started!");
    } catch (error) {
      console.error("Failed to create new session:", error);
      toast.error("Failed to start new session. Please try again.");
    }
  };

  const getSeverityBadge = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high': return 'bg-red-500/20 border-red-500/50 text-red-400';
      case 'medium': return 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400';
      case 'low': return 'bg-green-500/20 border-green-500/50 text-green-400';
      default: return 'bg-gray-500/20 border-gray-500/50 text-gray-400';
    }
  };

  const getRiskLevelBadge = (confidence?: number) => {
    if (!confidence) return 'bg-gray-500/20 border-gray-500/50 text-gray-400';
    
    if (confidence >= 0.8) return 'bg-red-500/20 border-red-500/50 text-red-400';
    if (confidence >= 0.6) return 'bg-yellow-500/20 border-yellow-500/50 text-yellow-400';
    return 'bg-green-500/20 border-green-500/50 text-green-400';
  };

  return (
    <div className="space-y-6">
      {/* AI Security Advisor - Full Width */}
      <Card className="bg-gradient-to-br from-purple-900/40 to-blue-900/40 border-purple-300/40 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg">
                <MessageCircle className="w-6 h-6 text-white" />
              </div>
              <CardTitle className="text-xl text-white font-bold">AI Security Advisor</CardTitle>
            </div>
            <div className="flex gap-2">
              <Button
                onClick={handleNewSession}
                disabled={createSessionMutation.isPending}
                size="sm"
                className="bg-white/20 hover:bg-white/30 text-white border border-white/40"
              >
                <RefreshCw className="w-4 h-4 mr-2" />
                New Chat
              </Button>
            </div>
          </div>
        </CardHeader>
        
        <CardContent className="space-y-6">
          {/* Chat Interface - Always Visible */}
          <div className="p-4 bg-white/25 rounded-lg border border-white/40 shadow-lg">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
              <p className="text-white font-bold text-base">AI Security Chat</p>
              {currentSessionId && (
                <Badge className="bg-blue-500/20 border-blue-500/50 text-blue-300 text-xs">
                  Session Active
                </Badge>
              )}
            </div>
            
            {/* Chat Messages */}
            <div className="space-y-3 max-h-96 overflow-y-auto mb-4">
              {chatMessages.length === 0 ? (
                <div className="text-center py-8">
                  <Bot className="w-12 h-12 mx-auto mb-3 text-blue-300" />
                  <p className="text-white font-bold text-sm mb-1">Start a conversation with your AI security advisor</p>
                  <p className="text-blue-100 text-xs">Ask about cybersecurity, threats, or get security advice</p>
                </div>
              ) : (
                chatMessages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-3 ${message.isUser ? 'justify-end' : 'justify-start'}`}
                  >
                    {!message.isUser && (
                      <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                        <Bot className="w-4 h-4 text-white" />
                      </div>
                    )}
                    <div
                      className={`max-w-xs p-3 rounded-lg ${
                        message.isUser
                          ? 'bg-purple-600 text-white shadow-lg'
                          : 'bg-white/40 text-white border border-white/50 shadow-lg'
                      }`}
                    >
                      <p className="text-sm whitespace-pre-line leading-relaxed font-medium">{message.content}</p>
                      <div className="flex items-center justify-between mt-2">
                        <p className="text-xs text-blue-100 font-medium">
                          {message.timestamp.toLocaleTimeString()}
                        </p>
                        {!message.isUser && message.aiModel && (
                          <div className="flex gap-1">
                            <Badge className={`text-xs ${getRiskLevelBadge(message.aiConfidence)}`}>
                              {message.aiModel}
                            </Badge>
                            {message.aiConfidence && (
                              <Badge className="text-xs bg-purple-500/20 border-purple-500/50 text-purple-300">
                                {Math.round(message.aiConfidence * 100)}%
                              </Badge>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                    {message.isUser && (
                      <div className="w-8 h-8 bg-purple-600 rounded-full flex items-center justify-center">
                        <User className="w-4 h-4 text-white" />
                      </div>
                    )}
                  </div>
                ))
              )}
              
              {/* Loading indicator */}
              {isLoadingChat && (
                <div className="flex gap-3 justify-start">
                  <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-white/40 text-white border border-white/50 shadow-lg rounded-lg p-3">
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin text-blue-300" />
                      <p className="text-sm font-medium">AI is analyzing your message...</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Chat Input */}
            <form onSubmit={handleChatSubmit} className="flex gap-2">
              <Input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Ask me about cybersecurity..."
                className="flex-1 bg-white/30 border-white/50 text-white placeholder-blue-100 focus:ring-purple-400"
                disabled={sendMessageMutation.isPending || !currentSessionId}
              />
              <Button
                type="submit"
                disabled={!chatInput.trim() || sendMessageMutation.isPending || !currentSessionId}
                className="bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white p-2 disabled:opacity-50"
              >
                {sendMessageMutation.isPending ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </Button>
            </form>
          </div>
        </CardContent>
      </Card>

      {/* Email Check - Full Width Below */}
      <Card className="bg-gradient-to-br from-red-900/40 to-orange-900/40 border-red-300/40 backdrop-blur-sm">
        <CardHeader className="pb-3">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-r from-red-600 to-orange-600 rounded-lg">
              <Shield className="w-5 h-5 text-white" />
            </div>
            <CardTitle className="text-lg text-white font-bold">Email Breach Check</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="relative">
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter email address to check for breaches..."
              className="w-full bg-white/30 border-white/50 text-white placeholder-orange-100 focus:ring-red-400"
              onKeyPress={(e) => e.key === 'Enter' && handleEmailCheck()}
            />
            <Button 
              onClick={handleEmailCheck}
              disabled={isChecking}
              size="sm"
              className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-700 hover:to-orange-700 text-white px-4 py-2 disabled:opacity-50"
            >
              {isChecking ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>
                  <Shield className="w-4 h-4 mr-2" />
                  Check
                </>
              )}
            </Button>
          </div>

          {/* Breach Results */}
          {isChecking && (
            <div className="p-3 bg-white/30 rounded-lg border border-white/50 shadow-lg">
              <div className="flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-red-400" />
                <p className="text-white font-bold text-sm">Checking for breaches...</p>
              </div>
            </div>
          )}

          {breaches && breaches.length > 0 && hasChecked && (
            <div className="p-3 bg-red-500/30 rounded-lg border border-red-400/50 shadow-lg">
              <div className="flex items-center gap-2 mb-3">
                <AlertTriangle className="w-4 h-4 text-red-400" />
                <p className="text-white font-bold text-sm">
                  Found {breaches.length} breach(es) for {email}
                </p>
              </div>
              <div className="space-y-3">
                {breaches.slice(0, 3).map((breach, index) => (
                  <div key={index} className="p-3 bg-white/40 rounded-lg border border-white/50 shadow-lg">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="text-white font-bold text-sm">{breach.breach_name}</h4>
                      <Badge className={`text-xs font-bold ${getSeverityBadge(breach.severity)}`}>
                        {breach.severity.toUpperCase()}
                      </Badge>
                    </div>
                    <p className="text-white text-sm mb-2 leading-relaxed font-medium">{breach.breach_description}</p>
                    <div className="text-xs text-blue-100 font-bold">
                      Date: {new Date(breach.breach_date).toLocaleDateString()}
                    </div>
                  </div>
                ))}
                {breaches.length > 3 && (
                  <p className="text-center text-sm text-white font-bold py-2">
                    +{breaches.length - 3} more breaches
                  </p>
                )}
              </div>
            </div>
          )}

          {breaches && breaches.length === 0 && !isChecking && hasChecked && (
            <div className="p-3 bg-green-500/30 rounded-lg border border-green-400/50 shadow-lg">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-400" />
                <p className="text-white font-bold text-sm">No breaches found for this email address. Your account appears to be secure!</p>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
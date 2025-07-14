"use client"

import { useState, useEffect } from "react"
import {
  AlertTriangle,
  CheckCircle,
  X,
  Shield,
  MessageSquare,
  Video,
  Mic,
  MapPin,
  Eye,
  Brain,
  Zap,
  Activity,
  Radar,
  Database,
  Clock,
  Wifi,
  WifiOff,
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { Switch } from "@/components/ui/switch"
import { ThreatIntelligenceService, type ThreatAlert, type DarkWebIntel } from "../services/threat-intelligence"
import {
  AIAnalysisService,
  type AIAnalysisResult,
  type DeepfakeAnalysis,
  type VoiceAnalysis,
} from "../services/ai-analysis"

export function EnhancedScamDetection() {
  const [messageText, setMessageText] = useState("")
  const [analysisResult, setAnalysisResult] = useState<AIAnalysisResult | null>(null)
  const [voiceAnalysis, setVoiceAnalysis] = useState<VoiceAnalysis | null>(null)
  const [videoAnalysis, setVideoAnalysis] = useState<DeepfakeAnalysis | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [realtimeMonitoring, setRealtimeMonitoring] = useState(true)
  const [threats, setThreats] = useState<ThreatAlert[]>([])
  const [darkWebIntel, setDarkWebIntel] = useState<DarkWebIntel[]>([])
  const [selectedLocation, setSelectedLocation] = useState<string>("")

  const threatService = ThreatIntelligenceService.getInstance()
  const aiService = AIAnalysisService.getInstance()

  useEffect(() => {
    // Load initial threat data
    setThreats(threatService.getRecentThreats())
    setDarkWebIntel(threatService.getDarkWebIntelligence())

    // Simulate real-time updates
    const interval = setInterval(() => {
      if (realtimeMonitoring) {
        setThreats(threatService.getRecentThreats())
        setDarkWebIntel(threatService.getDarkWebIntelligence())
      }
    }, 30000) // Update every 30 seconds

    return () => clearInterval(interval)
  }, [realtimeMonitoring])

  const analyzeMessage = async () => {
    setIsAnalyzing(true)
    try {
      const result = await aiService.analyzeText(messageText)
      setAnalysisResult(result)
    } catch (error) {
      console.error("Analysis failed:", error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const analyzeVoiceFile = async (file: File) => {
    setIsAnalyzing(true)
    try {
      const result = await aiService.analyzeVoice(file)
      setVoiceAnalysis(result)
    } catch (error) {
      console.error("Voice analysis failed:", error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const analyzeVideoFile = async (file: File) => {
    setIsAnalyzing(true)
    try {
      const result = await aiService.analyzeVideo(file)
      setVideoAnalysis(result)
    } catch (error) {
      console.error("Video analysis failed:", error)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const getRiskColor = (level: string) => {
    switch (level) {
      case "critical":
        return "text-red-600 bg-red-50 border-red-200"
      case "high":
        return "text-shield-orange bg-orange-50 border-orange-200"
      case "medium":
        return "text-yellow-600 bg-yellow-50 border-yellow-200"
      case "low":
        return "text-blue-600 bg-blue-50 border-blue-200"
      case "safe":
        return "text-shield-green bg-green-50 border-green-200"
      default:
        return "text-gray-600 bg-gray-50 border-gray-200"
    }
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "critical":
        return "bg-red-600"
      case "high":
        return "bg-shield-orange"
      case "medium":
        return "bg-yellow-500"
      case "low":
        return "bg-blue-500"
      default:
        return "bg-gray-500"
    }
  }

  const filteredThreats = selectedLocation ? threats.filter((t) => t.location === selectedLocation) : threats

  const threatStats = threatService.getThreatStatistics()

  return (
    <div className="space-y-6">
      {/* Header with Real-time Status */}
      <div className="text-center py-4">
        <div className="flex items-center justify-center space-x-3 mb-2">
          <div
            className={`flex items-center space-x-2 px-3 py-1 rounded-full ${realtimeMonitoring ? "bg-green-100 text-green-800" : "bg-gray-100 text-gray-600"}`}
          >
            {realtimeMonitoring ? <Wifi className="h-4 w-4" /> : <WifiOff className="h-4 w-4" />}
            <span className="text-sm font-medium">
              {realtimeMonitoring ? "Live Monitoring Active" : "Monitoring Paused"}
            </span>
          </div>
          <Switch checked={realtimeMonitoring} onCheckedChange={setRealtimeMonitoring} />
        </div>
        <h2 className="text-3xl font-bold text-shield-blue mb-2">AI-Powered Threat Detection</h2>
        <p className="text-lg text-gray-600">Advanced cybersecurity monitoring with real-time intelligence</p>
      </div>

      {/* Threat Intelligence Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Activity className="h-8 w-8 text-shield-blue" />
              <div>
                <p className="text-2xl font-bold text-shield-blue">{threatStats.total}</p>
                <p className="text-sm text-gray-600">Active Threats</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Clock className="h-8 w-8 text-shield-orange" />
              <div>
                <p className="text-2xl font-bold text-shield-orange">{threatStats.last24Hours}</p>
                <p className="text-sm text-gray-600">Last 24 Hours</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Database className="h-8 w-8 text-purple-600" />
              <div>
                <p className="text-2xl font-bold text-purple-600">{darkWebIntel.length}</p>
                <p className="text-sm text-gray-600">Dark Web Alerts</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center space-x-2">
              <Radar className="h-8 w-8 text-shield-green" />
              <div>
                <p className="text-2xl font-bold text-shield-green">98.7%</p>
                <p className="text-sm text-gray-600">Detection Rate</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Enhanced Detection Tabs */}
      <Tabs defaultValue="realtime" className="w-full">
        <TabsList className="grid w-full grid-cols-5 h-14 text-base">
          <TabsTrigger value="realtime" className="flex items-center space-x-2">
            <Activity className="h-5 w-5" />
            <span>Live Threats</span>
          </TabsTrigger>
          <TabsTrigger value="message" className="flex items-center space-x-2">
            <MessageSquare className="h-5 w-5" />
            <span>Text Analysis</span>
          </TabsTrigger>
          <TabsTrigger value="voice" className="flex items-center space-x-2">
            <Mic className="h-5 w-5" />
            <span>Voice AI</span>
          </TabsTrigger>
          <TabsTrigger value="video" className="flex items-center space-x-2">
            <Video className="h-5 w-5" />
            <span>Deepfake</span>
          </TabsTrigger>
          <TabsTrigger value="darkweb" className="flex items-center space-x-2">
            <Eye className="h-5 w-5" />
            <span>Dark Web</span>
          </TabsTrigger>
        </TabsList>

        {/* Real-time Threat Monitoring */}
        <TabsContent value="realtime" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Threat Map/List */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="flex items-center text-xl">
                      <MapPin className="h-6 w-6 mr-2 text-shield-blue" />
                      Live Threat Map
                    </CardTitle>
                    <select
                      value={selectedLocation}
                      onChange={(e) => setSelectedLocation(e.target.value)}
                      className="px-3 py-1 border rounded-md text-sm"
                    >
                      <option value="">All Locations</option>
                      <option value="Downtown">Downtown</option>
                      <option value="Suburb North">Suburb North</option>
                      <option value="City Center">City Center</option>
                      <option value="East District">East District</option>
                      <option value="West Side">West Side</option>
                    </select>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {filteredThreats.slice(0, 10).map((threat) => (
                      <Alert key={threat.id} className={`border-l-4 ${getSeverityColor(threat.severity)} border-l-4`}>
                        <AlertTriangle className="h-5 w-5" />
                        <AlertDescription>
                          <div className="flex justify-between items-start">
                            <div className="flex-1">
                              <div className="flex items-center space-x-2 mb-1">
                                <Badge className={getSeverityColor(threat.severity) + " text-white"}>
                                  {threat.severity.toUpperCase()}
                                </Badge>
                                <Badge variant="outline" className="text-xs">
                                  {threat.source.toUpperCase()}
                                </Badge>
                              </div>
                              <p className="font-semibold text-shield-blue">{threat.type}</p>
                              <p className="text-sm text-gray-600 mb-2">{threat.description}</p>
                              <div className="flex items-center space-x-4 text-xs text-gray-500">
                                <span>📍 {threat.location}</span>
                                <span>🕒 {threat.timestamp.toLocaleTimeString()}</span>
                                <span>👥 {threat.affectedDemographics.join(", ")}</span>
                              </div>
                            </div>
                          </div>
                        </AlertDescription>
                      </Alert>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Threat Statistics */}
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Threat Breakdown</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {Object.entries(threatStats.severityCounts).map(([severity, count]) => (
                      <div key={severity} className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <div className={`w-3 h-3 rounded-full ${getSeverityColor(severity)}`}></div>
                          <span className="capitalize text-sm">{severity}</span>
                        </div>
                        <span className="font-semibold">{count}</span>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Top Threat Types</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {Object.entries(threatStats.typeCounts)
                      .sort(([, a], [, b]) => b - a)
                      .slice(0, 5)
                      .map(([type, count]) => (
                        <div key={type} className="flex justify-between items-center text-sm">
                          <span className="truncate">{type}</span>
                          <Badge variant="secondary">{count}</Badge>
                        </div>
                      ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        {/* Enhanced Message Analysis */}
        <TabsContent value="message" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl flex items-center">
                <Brain className="h-6 w-6 mr-2 text-shield-blue" />
                Advanced AI Text Analysis
              </CardTitle>
              <CardDescription className="text-base">
                Multi-layered AI analysis including NLP, sentiment analysis, and behavioral pattern detection
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Paste the suspicious message, email, or text here for comprehensive AI analysis..."
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
                className="min-h-32 text-base"
              />
              <Button
                onClick={analyzeMessage}
                disabled={!messageText.trim() || isAnalyzing}
                className="w-full bg-shield-blue hover:bg-shield-blue/90 text-white text-lg py-3"
              >
                {isAnalyzing ? (
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    <span>AI Analysis in Progress...</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-2">
                    <Zap className="h-5 w-5" />
                    <span>Run AI Analysis</span>
                  </div>
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Enhanced Analysis Results */}
          {analysisResult && (
            <Card className={`border-2 ${getRiskColor(analysisResult.riskLevel)}`}>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {analysisResult.riskLevel === "critical" || analysisResult.riskLevel === "high" ? (
                      <AlertTriangle className="h-6 w-6 text-red-600" />
                    ) : analysisResult.riskLevel === "safe" ? (
                      <CheckCircle className="h-6 w-6 text-shield-green" />
                    ) : (
                      <Shield className="h-6 w-6 text-yellow-600" />
                    )}
                    <span
                      className={`text-xl font-bold ${analysisResult.riskLevel === "critical" || analysisResult.riskLevel === "high" ? "text-red-600" : analysisResult.riskLevel === "safe" ? "text-shield-green" : "text-yellow-600"}`}
                    >
                      Risk Level: {analysisResult.riskLevel.toUpperCase()}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold">{analysisResult.riskScore}/100</div>
                    <div className="text-sm text-gray-600">{analysisResult.confidence}% confidence</div>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Risk Score Visualization */}
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span>Risk Score</span>
                    <span>{analysisResult.riskScore}/100</span>
                  </div>
                  <Progress value={analysisResult.riskScore} className="h-3" />
                </div>

                {/* Detected Patterns */}
                {analysisResult.detectedPatterns.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-base mb-3">🚨 Detected Threat Patterns:</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {analysisResult.detectedPatterns.map((pattern, index) => (
                        <Badge key={index} variant="destructive" className="text-sm justify-start">
                          {pattern}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* Technical Analysis Details */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Card className="bg-gray-50">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm">Technical Analysis</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>NLP Score:</span>
                        <span className="font-semibold">{analysisResult.technicalDetails.nlpScore}/100</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Sentiment:</span>
                        <span className="font-semibold">{analysisResult.technicalDetails.sentimentAnalysis}</span>
                      </div>
                      <div>
                        <span>Linguistic Patterns:</span>
                        <div className="mt-1 space-y-1">
                          {analysisResult.technicalDetails.linguisticPatterns.map((pattern, i) => (
                            <Badge key={i} variant="outline" className="text-xs mr-1">
                              {pattern}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="bg-gray-50">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-sm">Behavioral Indicators</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-2 text-sm">
                      {analysisResult.technicalDetails.behavioralIndicators.map((indicator, i) => (
                        <div key={i} className="flex items-center space-x-2">
                          <AlertTriangle className="h-4 w-4 text-orange-500" />
                          <span>{indicator}</span>
                        </div>
                      ))}
                    </CardContent>
                  </Card>
                </div>

                {/* AI Recommendations */}
                <Alert className="border-shield-blue">
                  <Shield className="h-5 w-5" />
                  <AlertDescription>
                    <div>
                      <h4 className="font-semibold mb-2">🤖 AI Recommendations:</h4>
                      <ul className="space-y-1">
                        {analysisResult.recommendations.map((rec, index) => (
                          <li key={index} className="flex items-start space-x-2">
                            <span className="text-shield-blue">•</span>
                            <span>{rec}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </AlertDescription>
                </Alert>

                {/* Action Buttons */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-3 pt-4">
                  <Button variant="destructive" className="text-base py-3">
                    <X className="h-5 w-5 mr-2" />
                    Block Sender
                  </Button>
                  <Button
                    variant="outline"
                    className="text-base py-3 border-shield-blue text-shield-blue bg-transparent"
                  >
                    <Shield className="h-5 w-5 mr-2" />
                    Verify Source
                  </Button>
                  <Button variant="secondary" className="text-base py-3">
                    <AlertTriangle className="h-5 w-5 mr-2" />
                    Report Threat
                  </Button>
                  <Button variant="outline" className="text-base py-3 bg-transparent">
                    Learn More
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Enhanced Voice Analysis */}
        <TabsContent value="voice" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl flex items-center">
                <Mic className="h-6 w-6 mr-2 text-shield-blue" />
                AI Voice & Audio Analysis
              </CardTitle>
              <CardDescription className="text-base">
                Detect AI-generated voices, emotional manipulation, and call center patterns
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <Mic className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                <p className="text-lg text-gray-600 mb-4">Upload audio file or record suspicious call</p>
                <input
                  type="file"
                  accept="audio/*"
                  onChange={(e) => {
                    const file = e.target.files?.[0]
                    if (file) analyzeVoiceFile(file)
                  }}
                  className="hidden"
                  id="voice-upload"
                />
                <label htmlFor="voice-upload">
                  <Button className="bg-shield-blue hover:bg-shield-blue/90 text-white" asChild>
                    <span>Choose Audio File</span>
                  </Button>
                </label>
              </div>

              <Alert>
                <Brain className="h-5 w-5" />
                <AlertDescription className="text-base">
                  <strong>AI Detection Capabilities:</strong> Voice cloning, robotic speech patterns, background
                  analysis, emotional manipulation detection, call center identification
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>

          {/* Voice Analysis Results */}
          {voiceAnalysis && (
            <Card
              className={`border-2 ${voiceAnalysis.isAISynthetic ? "border-red-500 bg-red-50" : "border-green-500 bg-green-50"}`}
            >
              <CardHeader>
                <CardTitle
                  className={`flex items-center space-x-2 ${voiceAnalysis.isAISynthetic ? "text-red-600" : "text-green-600"}`}
                >
                  {voiceAnalysis.isAISynthetic ? (
                    <AlertTriangle className="h-6 w-6" />
                  ) : (
                    <CheckCircle className="h-6 w-6" />
                  )}
                  <span>
                    {voiceAnalysis.isAISynthetic ? "⚠️ AI-Generated Voice Detected" : "✅ Voice Appears Authentic"}
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold mb-2">Analysis Results</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Confidence Level:</span>
                        <span className="font-semibold">{voiceAnalysis.confidence}%</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Voice Print ID:</span>
                        <span className="font-mono text-xs">{voiceAnalysis.voiceprint}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Emotional Manipulation:</span>
                        <span
                          className={
                            voiceAnalysis.emotionalManipulation ? "text-red-600 font-semibold" : "text-green-600"
                          }
                        >
                          {voiceAnalysis.emotionalManipulation ? "Detected" : "Not Detected"}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-2">Background Analysis</h4>
                    <div className="space-y-1">
                      {voiceAnalysis.backgroundAnalysis.map((analysis, i) => (
                        <div key={i} className="flex items-center space-x-2 text-sm">
                          <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                          <span>{analysis}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <Alert className={voiceAnalysis.isAISynthetic ? "border-red-500" : "border-green-500"}>
                  <Shield className="h-5 w-5" />
                  <AlertDescription className="text-base font-medium">{voiceAnalysis.recommendation}</AlertDescription>
                </Alert>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Enhanced Video/Deepfake Analysis */}
        <TabsContent value="video" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl flex items-center">
                <Video className="h-6 w-6 mr-2 text-shield-blue" />
                Deepfake & Video Analysis
              </CardTitle>
              <CardDescription className="text-base">
                Advanced AI detection of deepfakes, face swaps, and manipulated media
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <Video className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                <p className="text-lg text-gray-600 mb-4">Upload suspicious video or image file</p>
                <input
                  type="file"
                  accept="video/*,image/*"
                  onChange={(e) => {
                    const file = e.target.files?.[0]
                    if (file) analyzeVideoFile(file)
                  }}
                  className="hidden"
                  id="video-upload"
                />
                <label htmlFor="video-upload">
                  <Button className="bg-shield-blue hover:bg-shield-blue/90 text-white" asChild>
                    <span>Choose Media File</span>
                  </Button>
                </label>
              </div>

              <Alert>
                <Eye className="h-5 w-5" />
                <AlertDescription className="text-base">
                  <strong>Detection Methods:</strong> Facial landmark analysis, temporal coherence, compression
                  artifacts, pixel-level inconsistencies, audio-visual synchronization
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>

          {/* Video Analysis Results */}
          {videoAnalysis && (
            <Card
              className={`border-2 ${videoAnalysis.isDeepfake ? "border-red-500 bg-red-50" : "border-green-500 bg-green-50"}`}
            >
              <CardHeader>
                <CardTitle
                  className={`flex items-center space-x-2 ${videoAnalysis.isDeepfake ? "text-red-600" : "text-green-600"}`}
                >
                  {videoAnalysis.isDeepfake ? (
                    <AlertTriangle className="h-6 w-6" />
                  ) : (
                    <CheckCircle className="h-6 w-6" />
                  )}
                  <span>{videoAnalysis.isDeepfake ? "🚨 DEEPFAKE DETECTED" : "✅ Media Appears Authentic"}</span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-semibold mb-2">Detection Results</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Confidence Level:</span>
                        <span className="font-semibold">{videoAnalysis.confidence}%</span>
                      </div>
                      <div>
                        <span>Technical Markers:</span>
                        <div className="mt-1 space-y-1">
                          {videoAnalysis.technicalMarkers.map((marker, i) => (
                            <div key={i} className="flex items-center space-x-2 text-xs">
                              <CheckCircle className="h-3 w-3 text-green-500" />
                              <span>{marker}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                  {videoAnalysis.anomalies.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2 text-red-600">Detected Anomalies</h4>
                      <div className="space-y-1">
                        {videoAnalysis.anomalies.map((anomaly, i) => (
                          <div key={i} className="flex items-center space-x-2 text-sm">
                            <AlertTriangle className="h-4 w-4 text-red-500" />
                            <span>{anomaly}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <Alert className={videoAnalysis.isDeepfake ? "border-red-500" : "border-green-500"}>
                  <Shield className="h-5 w-5" />
                  <AlertDescription className="text-base font-medium">{videoAnalysis.recommendation}</AlertDescription>
                </Alert>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Dark Web Intelligence */}
        <TabsContent value="darkweb" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl flex items-center">
                <Eye className="h-6 w-6 mr-2 text-purple-600" />
                Dark Web Intelligence
              </CardTitle>
              <CardDescription className="text-base">
                Real-time monitoring of underground markets and threat actor activities
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Alert className="mb-4 border-purple-200 bg-purple-50">
                <Database className="h-5 w-5" />
                <AlertDescription className="text-base">
                  <strong>Intelligence Sources:</strong> Underground forums, marketplace monitoring, threat actor
                  communications, stolen data listings
                </AlertDescription>
              </Alert>

              <div className="space-y-4">
                {darkWebIntel.map((intel) => (
                  <Card key={intel.id} className="border-l-4 border-l-purple-500">
                    <CardContent className="pt-4">
                      <div className="flex justify-between items-start mb-3">
                        <div>
                          <h4 className="font-semibold text-lg text-purple-700">{intel.threatType}</h4>
                          <p className="text-sm text-gray-600">{intel.description}</p>
                        </div>
                        <Badge className="bg-purple-600 text-white">Risk: {intel.riskLevel}/100</Badge>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                        <div>
                          <span className="font-medium">Market Activity:</span>
                          <p className="text-gray-600">{intel.marketActivity}</p>
                        </div>
                        <div>
                          <span className="font-medium">Price Range:</span>
                          <p className="text-gray-600">{intel.priceRange}</p>
                        </div>
                        <div>
                          <span className="font-medium">Target Region:</span>
                          <p className="text-gray-600">{intel.targetRegion}</p>
                        </div>
                      </div>

                      <div className="mt-3 pt-3 border-t flex justify-between items-center text-xs text-gray-500">
                        <span>Last Seen: {intel.lastSeen.toLocaleString()}</span>
                        <Button size="sm" variant="outline" className="text-xs bg-transparent">
                          View Details
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

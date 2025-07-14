"use client"

import { useState } from "react"
import { Upload, AlertTriangle, CheckCircle, X, Shield, MessageSquare, Video, Mic } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export function ScamDetection() {
  const [messageText, setMessageText] = useState("")
  const [analysisResult, setAnalysisResult] = useState<any>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const analyzeMessage = async () => {
    setIsAnalyzing(true)
    // Simulate analysis
    setTimeout(() => {
      const suspiciousWords = ["urgent", "limited time", "act now", "verify account"]
      const foundSuspicious = suspiciousWords.some((word) => messageText.toLowerCase().includes(word.toLowerCase()))

      setAnalysisResult({
        riskLevel: foundSuspicious ? "high" : "low",
        flags: foundSuspicious ? ["Urgency tactics detected", "Suspicious language patterns"] : [],
        recommendation: foundSuspicious
          ? "This message shows signs of a scam. Do not respond or click any links."
          : "This message appears safe, but always verify sender identity.",
      })
      setIsAnalyzing(false)
    }, 2000)
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center py-4">
        <h2 className="text-3xl font-bold text-shield-blue mb-2">Real-Time Scam Detection</h2>
        <p className="text-lg text-gray-600">Analyze messages, calls, and media for potential scams</p>
      </div>

      {/* Detection Tabs */}
      <Tabs defaultValue="message" className="w-full">
        <TabsList className="grid w-full grid-cols-3 h-14 text-base">
          <TabsTrigger value="message" className="flex items-center space-x-2">
            <MessageSquare className="h-5 w-5" />
            <span>Text Messages</span>
          </TabsTrigger>
          <TabsTrigger value="voice" className="flex items-center space-x-2">
            <Mic className="h-5 w-5" />
            <span>Voice Calls</span>
          </TabsTrigger>
          <TabsTrigger value="video" className="flex items-center space-x-2">
            <Video className="h-5 w-5" />
            <span>Video/Images</span>
          </TabsTrigger>
        </TabsList>

        {/* Message Analysis */}
        <TabsContent value="message" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Message Scanner</CardTitle>
              <CardDescription className="text-base">
                Paste a suspicious message below to check for scam indicators
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Paste the message you want to check here..."
                value={messageText}
                onChange={(e) => setMessageText(e.target.value)}
                className="min-h-32 text-base"
              />
              <Button
                onClick={analyzeMessage}
                disabled={!messageText.trim() || isAnalyzing}
                className="w-full bg-shield-blue hover:bg-shield-blue/90 text-white text-lg py-3"
              >
                {isAnalyzing ? "Analyzing..." : "Analyze Message"}
              </Button>
            </CardContent>
          </Card>

          {/* Analysis Results */}
          {analysisResult && (
            <Card
              className={`border-2 ${analysisResult.riskLevel === "high" ? "border-shield-orange" : "border-shield-green"}`}
            >
              <CardHeader>
                <CardTitle className="flex items-center space-x-2">
                  {analysisResult.riskLevel === "high" ? (
                    <AlertTriangle className="h-6 w-6 text-shield-orange" />
                  ) : (
                    <CheckCircle className="h-6 w-6 text-shield-green" />
                  )}
                  <span className={analysisResult.riskLevel === "high" ? "text-shield-orange" : "text-shield-green"}>
                    {analysisResult.riskLevel === "high" ? "⚠️ High Risk Detected" : "✅ Low Risk"}
                  </span>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {analysisResult.flags.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-base mb-2">Warning Signs Found:</h4>
                    <div className="space-y-2">
                      {analysisResult.flags.map((flag: string, index: number) => (
                        <Badge key={index} variant="destructive" className="text-sm">
                          {flag}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                <Alert className={analysisResult.riskLevel === "high" ? "border-shield-orange" : "border-shield-green"}>
                  <Shield className="h-5 w-5" />
                  <AlertDescription className="text-base font-medium">{analysisResult.recommendation}</AlertDescription>
                </Alert>

                {/* Action Buttons */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-4">
                  <Button variant="destructive" className="text-base py-3">
                    <X className="h-5 w-5 mr-2" />
                    Block Sender
                  </Button>
                  <Button
                    variant="outline"
                    className="text-base py-3 border-shield-blue text-shield-blue bg-transparent"
                  >
                    <Shield className="h-5 w-5 mr-2" />
                    Verify Caller
                  </Button>
                  <Button variant="secondary" className="text-base py-3">
                    Learn More
                  </Button>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        {/* Voice Analysis */}
        <TabsContent value="voice" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Voice Call Analysis</CardTitle>
              <CardDescription className="text-base">Upload a recording or describe a suspicious call</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                <p className="text-lg text-gray-600 mb-4">Upload audio file or record call</p>
                <Button className="bg-shield-blue hover:bg-shield-blue/90 text-white">Choose File</Button>
              </div>

              <Alert>
                <Mic className="h-5 w-5" />
                <AlertDescription className="text-base">
                  <strong>Common voice scam signs:</strong> Robotic voice, background noise, pressure to act quickly,
                  requests for personal information
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Video/Image Analysis */}
        <TabsContent value="video" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Deepfake Detection</CardTitle>
              <CardDescription className="text-base">
                Upload suspicious videos or images for AI analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <Video className="h-12 w-12 mx-auto text-gray-400 mb-4" />
                <p className="text-lg text-gray-600 mb-4">Upload video or image file</p>
                <Button className="bg-shield-blue hover:bg-shield-blue/90 text-white">Choose File</Button>
              </div>

              <Alert>
                <AlertTriangle className="h-5 w-5" />
                <AlertDescription className="text-base">
                  <strong>Deepfake warning signs:</strong> Unnatural eye movements, inconsistent lighting, audio sync
                  issues, pixelated face edges
                </AlertDescription>
              </Alert>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

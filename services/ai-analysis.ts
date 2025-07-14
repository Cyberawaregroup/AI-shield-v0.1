"use client"

export interface AIAnalysisResult {
  riskScore: number
  riskLevel: "safe" | "low" | "medium" | "high" | "critical"
  confidence: number
  detectedPatterns: string[]
  threatType?: string
  recommendations: string[]
  technicalDetails: {
    nlpScore: number
    sentimentAnalysis: string
    linguisticPatterns: string[]
    behavioralIndicators: string[]
  }
}

export interface DeepfakeAnalysis {
  isDeepfake: boolean
  confidence: number
  anomalies: string[]
  technicalMarkers: string[]
  recommendation: string
}

export interface VoiceAnalysis {
  isAISynthetic: boolean
  confidence: number
  voiceprint: string
  emotionalManipulation: boolean
  backgroundAnalysis: string[]
  recommendation: string
}

export class AIAnalysisService {
  private static instance: AIAnalysisService

  static getInstance(): AIAnalysisService {
    if (!AIAnalysisService.instance) {
      AIAnalysisService.instance = new AIAnalysisService()
    }
    return AIAnalysisService.instance
  }

  async analyzeText(text: string): Promise<AIAnalysisResult> {
    // Simulate AI processing time
    await new Promise((resolve) => setTimeout(resolve, 1500))

    const suspiciousPatterns = [
      { pattern: /urgent|emergency|immediate/gi, weight: 0.3, type: "urgency" },
      { pattern: /verify|confirm|update.*account/gi, weight: 0.4, type: "verification_scam" },
      { pattern: /click.*link|download.*attachment/gi, weight: 0.5, type: "malicious_link" },
      { pattern: /limited.*time|expires.*soon|act.*now/gi, weight: 0.3, type: "pressure_tactics" },
      { pattern: /congratulations|winner|prize|lottery/gi, weight: 0.4, type: "lottery_scam" },
      { pattern: /investment|profit|guaranteed.*return/gi, weight: 0.4, type: "investment_fraud" },
      { pattern: /love|relationship|marry|soulmate/gi, weight: 0.2, type: "romance_scam" },
      { pattern: /bitcoin|cryptocurrency|crypto|wallet/gi, weight: 0.3, type: "crypto_scam" },
      { pattern: /social.*security|irs|tax|government/gi, weight: 0.4, type: "government_impersonation" },
      { pattern: /tech.*support|computer.*problem|virus.*detected/gi, weight: 0.4, type: "tech_support_scam" },
    ]

    let totalRisk = 0
    const detectedPatterns: string[] = []
    let primaryThreatType = ""
    let maxWeight = 0

    suspiciousPatterns.forEach(({ pattern, weight, type }) => {
      const matches = text.match(pattern)
      if (matches) {
        totalRisk += weight * matches.length
        detectedPatterns.push(`${type.replace(/_/g, " ")} indicators detected`)
        if (weight > maxWeight) {
          maxWeight = weight
          primaryThreatType = type.replace(/_/g, " ")
        }
      }
    })

    // Additional linguistic analysis
    const nlpScore = this.performNLPAnalysis(text)
    const sentimentAnalysis = this.analyzeSentiment(text)

    totalRisk = Math.min(totalRisk + nlpScore * 0.2, 1)
    const riskScore = Math.round(totalRisk * 100)

    const getRiskLevel = (score: number): AIAnalysisResult["riskLevel"] => {
      if (score >= 80) return "critical"
      if (score >= 60) return "high"
      if (score >= 40) return "medium"
      if (score >= 20) return "low"
      return "safe"
    }

    const riskLevel = getRiskLevel(riskScore)

    return {
      riskScore,
      riskLevel,
      confidence: Math.min(85 + Math.random() * 15, 99),
      detectedPatterns,
      threatType: primaryThreatType || undefined,
      recommendations: this.generateRecommendations(riskLevel, primaryThreatType),
      technicalDetails: {
        nlpScore: Math.round(nlpScore * 100),
        sentimentAnalysis,
        linguisticPatterns: this.detectLinguisticPatterns(text),
        behavioralIndicators: this.detectBehavioralIndicators(text),
      },
    }
  }

  async analyzeVoice(audioData: File): Promise<VoiceAnalysis> {
    // Simulate AI processing time
    await new Promise((resolve) => setTimeout(resolve, 3000))

    // Mock voice analysis results
    const isAISynthetic = Math.random() > 0.7
    const confidence = Math.round(75 + Math.random() * 20)

    return {
      isAISynthetic,
      confidence,
      voiceprint: `VP-${Math.random().toString(36).substr(2, 9).toUpperCase()}`,
      emotionalManipulation: Math.random() > 0.6,
      backgroundAnalysis: [
        "Call center environment detected",
        "Multiple voices in background",
        "Script reading patterns identified",
      ],
      recommendation: isAISynthetic
        ? "High probability of AI-generated voice. Verify caller identity through official channels."
        : "Voice appears authentic, but verify caller identity if requesting sensitive information.",
    }
  }

  async analyzeVideo(videoData: File): Promise<DeepfakeAnalysis> {
    // Simulate AI processing time
    await new Promise((resolve) => setTimeout(resolve, 4000))

    const isDeepfake = Math.random() > 0.8
    const confidence = Math.round(80 + Math.random() * 15)

    return {
      isDeepfake,
      confidence,
      anomalies: isDeepfake
        ? [
            "Inconsistent facial lighting",
            "Unnatural eye movement patterns",
            "Audio-visual synchronization issues",
            "Pixel-level artifacts detected",
          ]
        : [],
      technicalMarkers: [
        "Frame consistency analysis: PASS",
        "Facial landmark tracking: ANALYZED",
        "Compression artifact detection: COMPLETE",
        "Temporal coherence check: VERIFIED",
      ],
      recommendation: isDeepfake
        ? "CRITICAL: Deepfake technology detected. Do not trust this video content."
        : "Video appears authentic based on current analysis techniques.",
    }
  }

  private performNLPAnalysis(text: string): number {
    // Simulate NLP processing
    const wordCount = text.split(" ").length
    const avgWordLength = text.replace(/\s/g, "").length / wordCount
    const punctuationRatio = (text.match(/[!?]/g) || []).length / wordCount

    // Higher scores for suspicious patterns
    let score = 0
    if (avgWordLength < 4) score += 0.1 // Simple language often used in scams
    if (punctuationRatio > 0.1) score += 0.2 // Excessive punctuation
    if (wordCount < 50) score += 0.1 // Very short messages

    return Math.min(score, 1)
  }

  private analyzeSentiment(text: string): string {
    const positiveWords = ["great", "amazing", "wonderful", "fantastic", "excellent", "perfect"]
    const negativeWords = ["urgent", "problem", "issue", "error", "warning", "suspended"]
    const manipulativeWords = ["limited", "exclusive", "secret", "guaranteed", "free", "winner"]

    const lowerText = text.toLowerCase()
    const positiveCount = positiveWords.filter((word) => lowerText.includes(word)).length
    const negativeCount = negativeWords.filter((word) => lowerText.includes(word)).length
    const manipulativeCount = manipulativeWords.filter((word) => lowerText.includes(word)).length

    if (manipulativeCount > 2) return "Highly Manipulative"
    if (negativeCount > positiveCount) return "Fear-inducing"
    if (positiveCount > negativeCount) return "Overly Positive"
    return "Neutral"
  }

  private detectLinguisticPatterns(text: string): string[] {
    const patterns: string[] = []

    if (text.match(/[A-Z]{3,}/g)) patterns.push("Excessive capitalization")
    if (text.match(/!{2,}/g)) patterns.push("Multiple exclamation marks")
    if (text.match(/\d{4}-\d{4}-\d{4}-\d{4}/g)) patterns.push("Credit card number pattern")
    if (text.match(/\b\d{3}-\d{2}-\d{4}\b/g)) patterns.push("SSN pattern detected")
    if (text.match(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g)) patterns.push("Email address present")

    return patterns
  }

  private detectBehavioralIndicators(text: string): string[] {
    const indicators: string[] = []

    if (text.toLowerCase().includes("don't tell anyone")) indicators.push("Secrecy request")
    if (text.toLowerCase().includes("act now") || text.toLowerCase().includes("hurry")) indicators.push("Time pressure")
    if (text.toLowerCase().includes("verify") || text.toLowerCase().includes("confirm"))
      indicators.push("Information harvesting")
    if (text.toLowerCase().includes("click") || text.toLowerCase().includes("download"))
      indicators.push("Action request")

    return indicators
  }

  private generateRecommendations(riskLevel: string, threatType: string): string[] {
    const baseRecommendations = [
      "Do not respond to this message",
      "Verify sender identity through official channels",
      "Report this message to authorities",
    ]

    const specificRecommendations: Record<string, string[]> = {
      "romance scam": [
        "Never send money to someone you haven't met in person",
        "Be suspicious of quick declarations of love",
        "Verify photos using reverse image search",
      ],
      "investment fraud": [
        "Research investment opportunities independently",
        "Be wary of guaranteed high returns",
        "Consult with a financial advisor",
      ],
      "tech support scam": [
        "Never give remote access to your computer",
        "Contact tech support through official channels only",
        "Be suspicious of unsolicited tech support calls",
      ],
    }

    return riskLevel === "safe"
      ? ["Message appears safe, but always verify sender identity"]
      : [...baseRecommendations, ...(specificRecommendations[threatType] || [])]
  }
}

"use client"

export interface ThreatAlert {
  id: string
  type: string
  severity: "critical" | "high" | "medium" | "low"
  location: string
  coordinates: [number, number]
  description: string
  timestamp: Date
  source: "darkweb" | "social" | "financial" | "telecom" | "ai_detection"
  indicators: string[]
  affectedDemographics: string[]
  preventionTips: string[]
}

export interface DarkWebIntel {
  id: string
  threatType: string
  marketActivity: string
  priceRange: string
  targetRegion: string
  riskLevel: number
  lastSeen: Date
  description: string
}

export class ThreatIntelligenceService {
  private static instance: ThreatIntelligenceService
  private threats: ThreatAlert[] = []
  private darkWebIntel: DarkWebIntel[] = []

  static getInstance(): ThreatIntelligenceService {
    if (!ThreatIntelligenceService.instance) {
      ThreatIntelligenceService.instance = new ThreatIntelligenceService()
    }
    return ThreatIntelligenceService.instance
  }

  // Simulate real-time threat data
  generateMockThreats(): ThreatAlert[] {
    const threatTypes = [
      "Romance Scam",
      "Investment Fraud",
      "Tech Support Scam",
      "Cryptocurrency Scam",
      "Identity Theft",
      "Phishing Campaign",
      "Ransomware",
      "Social Engineering",
      "Online Shopping Fraud",
      "Bank Impersonation",
      "Government Impersonation",
      "Utility Scam",
      "Charity Fraud",
      "Lottery Scam",
      "Employment Scam",
    ]

    const locations = [
      { name: "Downtown", coords: [40.7128, -74.006] as [number, number] },
      { name: "Suburb North", coords: [40.7589, -73.9851] as [number, number] },
      { name: "City Center", coords: [40.7505, -73.9934] as [number, number] },
      { name: "East District", coords: [40.7282, -73.7949] as [number, number] },
      { name: "West Side", coords: [40.7614, -73.9776] as [number, number] },
    ]

    return Array.from({ length: 15 }, (_, i) => ({
      id: `threat-${i + 1}`,
      type: threatTypes[Math.floor(Math.random() * threatTypes.length)],
      severity: ["critical", "high", "medium", "low"][Math.floor(Math.random() * 4)] as any,
      location: locations[Math.floor(Math.random() * locations.length)].name,
      coordinates: locations[Math.floor(Math.random() * locations.length)].coords,
      description: this.generateThreatDescription(),
      timestamp: new Date(Date.now() - Math.random() * 86400000 * 7), // Last 7 days
      source: ["darkweb", "social", "financial", "telecom", "ai_detection"][Math.floor(Math.random() * 5)] as any,
      indicators: this.generateIndicators(),
      affectedDemographics: ["Seniors 65+", "Young Adults", "Small Business Owners", "Students"],
      preventionTips: this.generatePreventionTips(),
    }))
  }

  generateDarkWebIntel(): DarkWebIntel[] {
    const marketActivities = [
      "Stolen Credit Card Data",
      "Identity Documents",
      "Banking Credentials",
      "Social Media Accounts",
      "Email Lists",
      "Phone Number Databases",
      "Cryptocurrency Wallets",
      "Medical Records",
      "Educational Credentials",
    ]

    return Array.from({ length: 8 }, (_, i) => ({
      id: `intel-${i + 1}`,
      threatType: marketActivities[Math.floor(Math.random() * marketActivities.length)],
      marketActivity: "High trading volume detected",
      priceRange: `$${Math.floor(Math.random() * 500) + 50} - $${Math.floor(Math.random() * 2000) + 500}`,
      targetRegion: ["North America", "Europe", "Asia-Pacific", "Global"][Math.floor(Math.random() * 4)],
      riskLevel: Math.floor(Math.random() * 100) + 1,
      lastSeen: new Date(Date.now() - Math.random() * 86400000 * 3), // Last 3 days
      description: "Increased marketplace activity suggesting coordinated campaign targeting vulnerable populations",
    }))
  }

  private generateThreatDescription(): string {
    const descriptions = [
      "AI-generated voice cloning used to impersonate family members requesting emergency funds",
      "Sophisticated phishing campaign using deepfake video calls to verify identity",
      "Cryptocurrency investment scheme promoted through fake celebrity endorsements",
      "Romance scam network using AI-generated profile photos and chatbots",
      "Tech support scam using legitimate-looking pop-ups and remote access tools",
      "Government impersonation scam claiming tax issues or legal problems",
      "Online shopping fraud using fake websites that mirror legitimate retailers",
    ]
    return descriptions[Math.floor(Math.random() * descriptions.length)]
  }

  private generateIndicators(): string[] {
    const allIndicators = [
      "Urgency language detected",
      "Request for personal information",
      "Unusual payment methods",
      "Pressure to act quickly",
      "Too good to be true offers",
      "Unsolicited contact",
      "Grammar/spelling errors",
      "Suspicious links",
      "Emotional manipulation",
      "Request for remote access",
      "Cryptocurrency payments only",
      "No physical address",
    ]
    return allIndicators.slice(0, Math.floor(Math.random() * 4) + 2)
  }

  private generatePreventionTips(): string[] {
    const tips = [
      "Verify caller identity through official channels",
      "Never provide personal information over unsolicited calls",
      "Use two-factor authentication on all accounts",
      "Be skeptical of urgent requests for money or information",
      "Research investment opportunities independently",
      "Keep software and security systems updated",
    ]
    return tips.slice(0, Math.floor(Math.random() * 3) + 2)
  }

  getRecentThreats(): ThreatAlert[] {
    if (this.threats.length === 0) {
      this.threats = this.generateMockThreats()
    }
    return this.threats.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
  }

  getDarkWebIntelligence(): DarkWebIntel[] {
    if (this.darkWebIntel.length === 0) {
      this.darkWebIntel = this.generateDarkWebIntel()
    }
    return this.darkWebIntel.sort((a, b) => b.lastSeen.getTime() - a.lastSeen.getTime())
  }

  getThreatsByLocation(location?: string): ThreatAlert[] {
    const threats = this.getRecentThreats()
    return location ? threats.filter((t) => t.location === location) : threats
  }

  getThreatStatistics() {
    const threats = this.getRecentThreats()
    const severityCounts = threats.reduce(
      (acc, threat) => {
        acc[threat.severity] = (acc[threat.severity] || 0) + 1
        return acc
      },
      {} as Record<string, number>,
    )

    const typeCounts = threats.reduce(
      (acc, threat) => {
        acc[threat.type] = (acc[threat.type] || 0) + 1
        return acc
      },
      {} as Record<string, number>,
    )

    return {
      total: threats.length,
      severityCounts,
      typeCounts,
      last24Hours: threats.filter((t) => Date.now() - t.timestamp.getTime() < 86400000).length,
    }
  }
}

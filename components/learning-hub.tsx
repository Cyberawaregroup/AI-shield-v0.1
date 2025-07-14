"use client"

import { useState } from "react"
import { BookOpen, Play, CheckCircle, ArrowRight, Heart, Phone, CreditCard, Truck } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export function LearningHub() {
  const [currentTip, setCurrentTip] = useState(0)

  const weeklyTips = [
    "Never give personal information over the phone unless you initiated the call",
    "Real banks will never ask for passwords or PINs via email or text",
    "Be suspicious of urgent requests for money or personal information",
    "Verify caller identity by hanging up and calling the official number",
    "Romance scammers often avoid video calls or meeting in person",
  ]

  const learningModules = [
    {
      id: 1,
      title: "Romance Scams",
      description: "Learn to identify fake dating profiles and emotional manipulation",
      icon: Heart,
      duration: "15 min",
      completed: true,
      difficulty: "Beginner",
    },
    {
      id: 2,
      title: "Phone Scams",
      description: "Recognize fake tech support and robocall scams",
      icon: Phone,
      duration: "12 min",
      completed: true,
      difficulty: "Beginner",
    },
    {
      id: 3,
      title: "Financial Fraud",
      description: "Protect your bank accounts and credit cards",
      icon: CreditCard,
      duration: "18 min",
      completed: false,
      difficulty: "Intermediate",
    },
    {
      id: 4,
      title: "Courier Scams",
      description: "Avoid fake delivery and package scams",
      icon: Truck,
      duration: "10 min",
      completed: false,
      difficulty: "Beginner",
    },
  ]

  const faqs = [
    {
      question: "How do I know if a caller is really from my bank?",
      answer:
        "Hang up and call your bank directly using the number on your card or statement. Real banks will never mind you verifying their identity.",
    },
    {
      question: "What should I do if I think I'm being scammed?",
      answer:
        "Stop all communication immediately, don't send money or share personal information, and report it to authorities or use our Report Scam feature.",
    },
    {
      question: "Are online dating profiles always real?",
      answer:
        "No. Be cautious of profiles with limited photos, people who avoid video calls, or anyone who quickly professes love or asks for money.",
    },
  ]

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="text-center py-4">
        <h2 className="text-3xl font-bold text-shield-blue mb-2">Awareness & Learning Hub</h2>
        <p className="text-lg text-gray-600">Build your knowledge to stay protected</p>
      </div>

      {/* Weekly Tips Carousel */}
      <Card className="bg-gradient-to-r from-shield-green/10 to-shield-blue/10">
        <CardHeader>
          <CardTitle className="text-xl flex items-center">
            <BookOpen className="h-6 w-6 mr-2 text-shield-green" />
            Weekly Security Tip
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-lg font-medium text-shield-blue mb-4">💡 {weeklyTips[currentTip]}</div>
          <div className="flex justify-between items-center">
            <div className="flex space-x-2">
              {weeklyTips.map((_, index) => (
                <button
                  key={index}
                  className={`w-3 h-3 rounded-full ${index === currentTip ? "bg-shield-blue" : "bg-gray-300"}`}
                  onClick={() => setCurrentTip(index)}
                />
              ))}
            </div>
            <Button
              variant="outline"
              onClick={() => setCurrentTip((prev) => (prev + 1) % weeklyTips.length)}
              className="border-shield-blue text-shield-blue hover:bg-shield-blue hover:text-white"
            >
              Next Tip <ArrowRight className="h-4 w-4 ml-2" />
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Learning Content Tabs */}
      <Tabs defaultValue="modules" className="w-full">
        <TabsList className="grid w-full grid-cols-2 h-14 text-base">
          <TabsTrigger value="modules" className="text-lg">
            Learning Modules
          </TabsTrigger>
          <TabsTrigger value="faqs" className="text-lg">
            Common Questions
          </TabsTrigger>
        </TabsList>

        {/* Learning Modules */}
        <TabsContent value="modules" className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {learningModules.map((module) => (
              <Card key={module.id} className="hover:shadow-lg transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex items-center space-x-3">
                      <div
                        className={`p-3 rounded-full ${module.completed ? "bg-shield-green/10" : "bg-shield-blue/10"}`}
                      >
                        <module.icon
                          className={`h-6 w-6 ${module.completed ? "text-shield-green" : "text-shield-blue"}`}
                        />
                      </div>
                      <div>
                        <CardTitle className="text-lg">{module.title}</CardTitle>
                        <div className="flex items-center space-x-2 mt-1">
                          <Badge variant="secondary" className="text-xs">
                            {module.duration}
                          </Badge>
                          <Badge variant="outline" className="text-xs">
                            {module.difficulty}
                          </Badge>
                        </div>
                      </div>
                    </div>
                    {module.completed && <CheckCircle className="h-6 w-6 text-shield-green" />}
                  </div>
                  <CardDescription className="text-base mt-2">{module.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button
                    className={`w-full text-base py-3 ${
                      module.completed
                        ? "bg-shield-green hover:bg-shield-green/90"
                        : "bg-shield-blue hover:bg-shield-blue/90"
                    } text-white`}
                  >
                    <Play className="h-5 w-5 mr-2" />
                    {module.completed ? "Review Module" : "Start Learning"}
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Progress Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="text-xl">Your Learning Progress</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex justify-between text-base">
                  <span>Modules Completed</span>
                  <span className="font-semibold">2 of 4</span>
                </div>
                <Progress value={50} className="h-3" />
                <p className="text-sm text-gray-600">
                  Great progress! Complete 2 more modules to become a Scam Prevention Expert.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* FAQs */}
        <TabsContent value="faqs" className="space-y-4">
          {faqs.map((faq, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle className="text-lg text-shield-blue">{faq.question}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-base text-gray-700">{faq.answer}</p>
              </CardContent>
            </Card>
          ))}

          <Card className="bg-shield-blue/5">
            <CardContent className="pt-6">
              <div className="text-center">
                <p className="text-lg font-medium text-shield-blue mb-4">Have more questions?</p>
                <Button className="bg-shield-blue hover:bg-shield-blue/90 text-white text-base py-3 px-6">
                  Contact Support
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

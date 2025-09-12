import SecurityHeader from "@/components/shield/SecurityHeader";
import SecurityAdvisorSimple from "@/components/shield/SecurityAdvisorSimple";
import SecurityFeatures from "@/components/shield/SecurityFeatures";
import AdvancedAnalytics from "@/components/shield/AdvancedAnalytics";
import ThreatDashboard from "@/components/shield/ThreatDashboard";

const Index = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-950 via-purple-900 to-indigo-950">
      <SecurityHeader />
      
      <main className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - AI Security Advisor */}
          <div className="lg:col-span-2">
            <SecurityAdvisorSimple />
          </div>
          
          {/* Right Column - Security Features */}
          <div>
            <SecurityFeatures />
          </div>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
          {/* Advanced Analytics */}
          <div>
            <AdvancedAnalytics />
          </div>
          
          {/* Threat Dashboard - Takes remaining space */}
          <div className="lg:col-span-2">
            <ThreatDashboard />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Index;

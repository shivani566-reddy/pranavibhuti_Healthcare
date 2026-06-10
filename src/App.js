import {
  LayoutDashboard, User, Pill, TestTube, Lock, FileText,
  Bot, Video, Syringe, ShieldAlert, Search, Bell, Globe,
  Mic, Heart, Activity, Droplet, Thermometer, Calendar,
  ChevronRight, Phone, ShieldCheck, Fingerprint
} from 'lucide-react';

export default function App() {
  const [step, setStep] = useState('login'); // login, otp, dashboard
  const [currentPage, setCurrentPage] = useState('Dashboard');
  const [mobileNumber, setMobileNumber] = useState('');
  const [otp, setOtp] = useState(['', '', '', '', '', '']);

  // Authentication Handlers
  const handleLoginSubmit = (e) => {
    e.preventDefault();
    if (mobileNumber.length >= 10) setStep('otp');
  };

  const handleOtpChange = (index, value) => {
    if (isNaN(value)) return;
    const newOtp = [...otp];
    newOtp[index] = value.substring(value.length - 1);
    setOtp(newOtp);
    if (value && index < 5) {
      document.getElementById(`otp-${index + 1}`).focus();
    }
  };

  const handleOtpVerify = () => {
    setStep('dashboard');
  };

  // Render Component Layouts based on Step
  if (step === 'login') {
    return (
      <div className="min-h-screen bg-[#1e469a] flex flex-col justify-between items-center p-6 text-white font-sans relative overflow-hidden">
        <div className="flex flex-col items-center mt-12">
          <div className="bg-[#1b3b80] p-4 rounded-2xl border border-teal-400/30 shadow-lg mb-4">
            <Heart className="w-10 h-10 text-teal-400 fill-teal-400/20" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-wider">PRANAVIBHUTI</h1>
          <p className="text-xs tracking-widest text-teal-200 mt-1">प्राणविभूति • Your Complete Health Companion</p>
        </div>

        <div className="bg-white text-gray-800 p-8 rounded-[2.5rem] w-full max-w-md shadow-2xl border border-white/10">
          <h2 className="text-2xl font-bold text-[#111827]">Welcome Back</h2>
          <p className="text-gray-500 text-sm mt-1">Login with your mobile number</p>

          <form onSubmit={handleLoginSubmit} className="mt-6 space-y-5">
            <div>
              <label className="text-xs font-bold tracking-wide text-gray-500 uppercase">Mobile Number</label>
              <div className="flex mt-1.5 border-2 border-blue-50 bg-blue-50/50 rounded-xl overflow-hidden focus-within:border-blue-500 transition-all">
                <div className="flex items-center gap-1.5 px-4 bg-gray-50 border-r border-gray-200 text-sm font-semibold text-gray-700">
                  <span className="text-base">🇮🇳</span> +91
                </div>
                <input 
                  type="tel" 
                  required
                  placeholder="9876543210"
                  maxLength={10}
                  value={mobileNumber}
                  onChange={(e) => setMobileNumber(e.target.value)}
                  className="w-full px-4 py-3.5 bg-transparent outline-none text-gray-800 font-medium placeholder-gray-400 text-base tracking-wide"
                />
              </div>
            </div>

            <button type="button" className="flex items-center gap-2 text-sm font-bold text-[#2563eb] hover:underline mt-1">
              <FileText className="w-4 h-4" /> Login with Aadhaar / Health Card
            </button>

            <button type="submit" className="w-full bg-[#2563eb] hover:bg-[#1d4ed8] text-white py-4 rounded-xl font-semibold flex items-center justify-center gap-2 shadow-lg shadow-blue-600/20 active:scale-[0.99] transition-all text-base mt-4">
              Send OTP <ChevronRight className="w-5 h-5" />
            </button>
          </form>

          <div className="relative flex py-4 items-center my-2">
            <div className="flex-grow border-t border-gray-200"></div>
            <span className="flex-shrink mx-4 text-xs font-bold text-gray-400 uppercase tracking-wider">Or Continue With</span>
            <div className="flex-grow border-t border-gray-200"></div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <button onClick={() => setStep('dashboard')} className="flex items-center justify-center gap-2.5 py-3 border border-gray-200 rounded-xl hover:bg-gray-50 font-semibold text-gray-700 text-sm transition-all">
              <Fingerprint className="w-5 h-5 text-blue-600" /> Biometric
            </button>
            <button onClick={() => setStep('dashboard')} className="flex items-center justify-center gap-2.5 py-3 border border-gray-200 rounded-xl hover:bg-gray-50 font-semibold text-gray-700 text-sm transition-all">
              <Globe className="w-5 h-5 text-emerald-600" /> Digi Yatra
            </button>
          </div>

          <div className="mt-6 bg-emerald-50/70 border border-emerald-100 rounded-2xl p-4 flex gap-3">
            <ShieldCheck className="w-5 h-5 text-emerald-600 flex-shrink-0 mt-0.5" />
            <p className="text-xs leading-relaxed text-emerald-800 font-medium">
              Protected by 256-bit encryption & HIPAA-compliant security. Your health data is safe.
            </p>
          </div>
        </div>

        <p className="text-xs text-white/60 tracking-wide mb-4">
          By continuing, you agree to PRANAVIBHUTI's <span className="underline cursor-pointer">Terms of Service</span> & <span className="underline cursor-pointer">Privacy Policy</span>
        </p>
      </div>
    );
  }

  if (step === 'otp') {
    return (
      <div className="min-h-screen bg-[#1e469a] flex flex-col justify-between items-center p-6 text-white font-sans">
        <div className="flex flex-col items-center mt-12">
          <div className="bg-[#1b3b80] p-4 rounded-2xl border border-teal-400/30 shadow-lg mb-4">
            <Heart className="w-10 h-10 text-teal-400 fill-teal-400/20" />
          </div>
          <h1 className="text-3xl font-extrabold tracking-wider">PRANAVIBHUTI</h1>
        </div>

        <div className="bg-white text-gray-800 p-8 rounded-[2.5rem] w-full max-w-md shadow-2xl text-center">
          <div className="mx-auto w-14 h-14 bg-blue-50 text-blue-600 rounded-full flex items-center justify-center mb-4">
            <Phone className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-[#111827]">Verify OTP</h2>
          <p className="text-gray-500 text-sm mt-1">Sent to +91 {mobileNumber || '98765 43210'}</p>
          <p className="text-emerald-600 text-xs font-bold bg-emerald-50 py-1.5 px-3 rounded-full inline-block mt-2">Demo OTP: 1 2 3 4 5 6</p>

          <div className="flex justify-between gap-2 my-8">
            {otp.map((data, index) => (
              <input
                key={index}
                id={`otp-${index}`}
                type="text"
                maxLength={1}
                value={data}
                onChange={(e) => handleOtpChange(index, e.target.value)}
                className="w-12 h-14 border-2 border-blue-100 rounded-xl text-center text-xl font-bold bg-blue-50/30 text-[#1e469a] focus:border-blue-600 outline-none transition-all"
              />
            ))}
          </div>

          <button onClick={handleOtpVerify} className="w-full bg-[#2563eb] hover:bg-[#1d4ed8] text-white py-4 rounded-xl font-semibold shadow-lg shadow-blue-600/20 active:scale-[0.99] transition-all text-base">
            Verify & Continue
          </button>

          <p className="text-gray-400 text-sm mt-5 font-medium">
            Resend OTP in <span className="text-[#2563eb] font-bold">10s</span>
          </p>

          <div className="mt-6 bg-amber-50/70 border border-amber-100 rounded-2xl p-4 text-left">
            <p className="text-xs leading-relaxed text-amber-800 font-medium">
              ⚠️ Never share your OTP with anyone. PRANAVIBHUTI will never ask for your OTP.
            </p>
          </div>
        </div>
        <div className="h-10"></div>
      </div>
    );
  }

  // Application Shell Layout (Sidebar Navigation + Dynamic Dashboard Screens)
  const menuItems = [
    { name: 'Dashboard', icon: LayoutDashboard },
    { name: 'Doctors', icon: User },
    { name: 'Medicines', icon: Pill },
    { name: 'Lab Tests', icon: TestTube },
    { name: 'Health Locker', icon: Lock },
    { name: 'Prescriptions', icon: FileText },
    { name: 'AI Assistant', icon: Bot },
    { name: 'Video Call', icon: Video },
    { name: 'Vaccinations', icon: Syringe },
    { name: 'Health Plans', icon: FileText },
  ];

  return (
    <div className="min-h-screen bg-[#f3f4f6] font-sans flex text-gray-800">
      {/* Sidebar Panel */}
      <aside className="w-64 bg-[#0a1931] text-white flex flex-col justify-between p-4 flex-shrink-0">
        <div>
          <div className="flex items-center gap-3 px-2 py-4 mb-4 border-b border-white/10">
            <div className="bg-[#1b3b80] p-1.5 rounded-xl border border-teal-400/30">
              <Heart className="w-6 h-6 text-teal-400 fill-teal-400/20" />
            </div>
            <div>
              <h2 className="text-lg font-bold tracking-wide">PRANAVIBHUTI</h2>
              <span className="text-[10px] text-teal-300 block tracking-wider -mt-1">प्राणविभूति</span>
            </div>
          </div>

          <div className="bg-[#15305b] p-3 rounded-2xl mb-6 flex items-center justify-between border border-white/5">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-teal-600 rounded-full flex items-center justify-center font-bold text-sm text-white">RS</div>
              <div>
                <h4 className="text-sm font-bold leading-tight">Ravi Shankar</h4>
                <p className="text-[11px] text-gray-400">Premium Plan</p>
              </div>
            </div>
            <span className="bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">Pro</span>
          </div>

          <p className="text-[10px] uppercase tracking-widest text-gray-400 font-bold px-2 mb-2">Main Menu</p>
          <nav className="space-y-1.5">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentPage === item.name;
              return (
                <button
                  key={item.name}
                  onClick={() => setCurrentPage(item.name)}
                  className={`w-full flex items-center gap-3.5 px-4 py-3 rounded-xl font-medium text-sm transition-all ${
                    isActive 
                      ? 'bg-[#2563eb] text-white font-bold shadow-lg shadow-blue-600/10' 
                      : 'text-gray-400 hover:bg-[#15305b] hover:text-white'
                  }`}
                >
                  <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-gray-400'}`} />
                  {item.name}
                </button>
              );
            })}
          </nav>
        </div>

        <div className="bg-gradient-to-br from-red-950/40 to-red-900/20 border border-red-500/20 rounded-2xl p-4 mt-6">
          <p className="text-[11px] uppercase tracking-wider text-red-400 font-bold flex items-center gap-1.5 mb-1">
            <ShieldAlert className="w-3.5 h-3.5" /> Emergency Helpline
          </p>
          <h3 className="text-xl font-black text-red-400 tracking-wide">1800-200-4747</h3>
          <p className="text-[10px] text-gray-400 mt-0.5">Available 24/7 • Free for all users</p>
        </div>
      </aside>

      {/* Primary Workspace Window */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top Navbar */}
        <header className="bg-white border-b border-gray-200 h-20 px-8 flex items-center justify-between sticky top-0 z-40">
          <div className="w-full max-w-xl relative">
            <Search className="w-5 h-5 text-gray-400 absolute left-4 top-1/2 -translate-y-1/2" />
            <input 
              type="text" 
              placeholder="Search doctors, medicines, tests..." 
              className="w-full pl-12 pr-4 py-3 bg-[#f3f4f6] outline-none rounded-xl text-sm border border-transparent focus:border-gray-300 focus:bg-white transition-all"
            />
          </div>

          <div className="flex items-center gap-4">
            <button className="flex items-center gap-1.5 border border-gray-200 px-3 py-2 rounded-xl text-xs font-bold text-gray-600 hover:bg-gray-50">
              <Globe className="w-4 h-4 text-blue-600" /> EN
            </button>
            <button className="w-10 h-10 border border-gray-200 rounded-xl flex items-center justify-center text-gray-600 hover:bg-gray-50">
              <Mic className="w-4 h-4" />
            </button>
            <button className="w-10 h-10 border border-gray-200 rounded-xl flex items-center justify-center text-gray-600 hover:bg-gray-50 relative">
              <Bell className="w-4 h-4" />
              <span className="absolute -top-1 -right-1 bg-red-500 text-white font-bold text-[10px] w-5 h-5 rounded-full flex items-center justify-center border-2 border-white">3</span>
            </button>
            <div className="w-10 h-10 bg-[#1e469a] text-white rounded-xl flex items-center justify-center font-bold text-sm cursor-pointer" onClick={() => setStep('login')}>
              RS
            </div>
          </div>
        </header>

        {/* Dynamic Content View Router */}
        <main className="p-8 overflow-y-auto flex-1 max-w-[1600px] w-full mx-auto">
          {currentPage === 'Dashboard' && <DashboardView />}
          {currentPage === 'Doctors' && <DoctorsView />}
          {currentPage === 'Medicines' && <MedicinesView />}
          {currentPage === 'Lab Tests' && <LabTestsView />}
          {currentPage === 'Health Locker' && <HealthLockerView />}
          {currentPage === 'Prescriptions' && <PrescriptionsView />}
          {currentPage === 'AI Assistant' && <AIAssistantView />}
          {currentPage === 'Video Call' && <VideoCallView />}
          {currentPage === 'Vaccinations' && <VaccinationsView />}
          {currentPage === 'Health Plans' && <HealthPlansView />}
        </main>
      </div>
    </div>
  );
}

/* ==========================================
   PAGE VIEWS COMPONENTS
   ========================================== */

function DashboardView() {
  return (
    <div className="space-y-8">
      {/* Banner */}
      <div className="bg-gradient-to-r from-[#1e3c72] to-[#2a5298] text-white rounded-[2rem] p-8 relative overflow-hidden shadow-xl">
        <div className="relative z-10">
          <p className="text-sm font-medium tracking-wide text-blue-200 flex items-center gap-1">Good Morning, 🌅</p>
          <h2 className="text-3xl font-extrabold mt-1">Ravi Shankar</h2>
          <p className="text-sm text-blue-100 mt-2">Next appointment: <span className="font-semibold text-white underline decoration-teal-400">Dr. Priya Sharma — Today 3:00 PM</span></p>
          <div className="mt-5 flex gap-3 text-xs items-center">
            <span className="bg-emerald-500 text-white font-bold px-3 py-1.5 rounded-xl uppercase tracking-wider">Premium Plan</span>
            <span className="text-blue-200 font-medium">Active since Jan 2025</span>
          </div>
        </div>
        <div className="absolute top-1/2 -right-10 w-64 h-64 bg-white/5 rounded-full blur-3xl transform -translate-y-1/2"></div>
      </div>

      {/* Vitals Grid */}
      <div>
        <h3 className="text-xs uppercase tracking-widest font-bold text-gray-400 mb-4">Today's Vitals</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <VitalCard icon={Heart} title="Heart Rate" value="72" unit="bpm" status="Normal" color="red" />
          <VitalCard icon={Activity} title="Blood Pressure" value="118/78" unit="mmHg" status="Normal" color="blue" />
          <VitalCard icon={Droplet} title="SpO2" value="98" unit="%" status="Good" color="emerald" />
          <VitalCard icon={Thermometer} title="Blood Sugar" value="104" unit="mg/dL" status="Normal" color="amber" />
        </div>
      </div>

      {/* Quick Action Matrix */}
      <div>
        <h3 className="text-xs uppercase tracking-widest font-bold text-gray-400 mb-4">Quick Actions</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          <QuickActionBtn icon={Calendar} label="Book Doctor" bg="bg-blue-500" />
          <QuickActionBtn icon={Pill} label="Order Medicine" bg="bg-emerald-500" />
          <QuickActionBtn icon={TestTube} label="Book Lab Test" bg="bg-purple-500" />
          <QuickActionBtn icon={Bot} label="AI Assistant" bg="bg-orange-500" />
          <QuickActionBtn icon={Video} label="Video Call" bg="bg-cyan-500" />
          <QuickActionBtn icon={Lock} label="Health Locker" bg="bg-rose-500" />
        </div>
      </div>

      {/* Split Lists section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-bold text-gray-800">Upcoming Appointments</h3>
            <button className="text-xs font-bold text-blue-600 hover:underline">View All &rarr;</button>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3.5 bg-gray-50 rounded-2xl border border-gray-100">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 bg-blue-100 rounded-xl flex items-center justify-center text-blue-600 font-bold text-sm">DS</div>
                <div>
                  <h4 className="text-sm font-bold text-gray-800">Dr. Priya Sharma</h4>
                  <p className="text-xs text-gray-400">Cardiologist • Today 3:00 PM</p>
                </div>
              </div>
              <span className="text-[11px] font-bold bg-emerald-50 text-emerald-600 px-3 py-1 rounded-full">Today</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-bold text-gray-800">Recent Activity</h3>
            <button className="text-xs font-bold text-blue-600 hover:underline">View All &rarr;</button>
          </div>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3.5 bg-gray-50 rounded-2xl border border-gray-100">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 bg-emerald-50 rounded-xl flex items-center justify-center text-emerald-600"><Pill className="w-5 h-5"/></div>
                <div>
                  <h4 className="text-sm font-bold text-gray-800">Metformin order delivered</h4>
                  <p className="text-xs text-gray-400">Pharmacy Order #84729</p>
                </div>
              </div>
              <span className="text-xs text-gray-400 font-medium">2 hrs ago</span>
            </div>
            <div className="flex items-center justify-between p-3.5 bg-gray-50 rounded-2xl border border-gray-100">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 bg-purple-50 rounded-xl flex items-center justify-center text-purple-600"><TestTube className="w-5 h-5"/></div>
                <div>
                  <h4 className="text-sm font-bold text-gray-800">CBC report ready</h4>
                  <p className="text-xs text-gray-400">Apollo Diagnostics Labs</p>
                </div>
              </div>
              <span className="text-xs text-gray-400 font-medium">Yesterday</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Subcomponents Helpers
function VitalCard({ icon: Icon, title, value, unit, status, color }) {
  const themes = {
    red: 'text-red-500 bg-red-50 border-red-100/70',
    blue: 'text-blue-500 bg-blue-50 border-blue-100/70',
    emerald: 'text-emerald-500 bg-emerald-50 border-emerald-100/70',
    amber: 'text-amber-500 bg-amber-50 border-amber-100/70',
  };
  return (
    <div className={`bg-white p-5 rounded-3xl border border-gray-100 shadow-sm hover:shadow-md transition-all`}>
      <div className="flex items-center justify-between">
        <span className="text-sm font-bold text-gray-400">{title}</span>
        <div className={`p-2.5 rounded-xl border ${themes[color]}`}><Icon className="w-5 h-5" /></div>
      </div>
      <div className="mt-4 flex items-baseline gap-1">
        <span className="text-3xl font-black text-gray-800 tracking-tight">{value}</span>
        <span className="text-xs font-bold text-gray-400 uppercase">{unit}</span>
      </div>
      <span className={`inline-block text-[11px] font-bold px-2.5 py-0.5 rounded-full mt-2 uppercase tracking-wide ${status === 'Good' || status === 'Normal' ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'}`}>• {status}</span>
    </div>
  );
}

function QuickActionBtn({ icon: Icon, label, bg }) {
  return (
    <button className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-all flex flex-col items-center text-center group">
      <div className={`${bg} text-white p-3.5 rounded-xl mb-3 shadow-lg shadow-gray-200 group-hover:scale-110 transition-all`}>
        <Icon className="w-5 h-5" />
      </div>
      <span className="text-xs font-bold text-gray-700 tracking-wide">{label}</span>
    </button>
  );
}

/* ==========================================
   OTHER WORKSPACE VIEWS (PLACEHOLDERS)
   ========================================== */
function DoctorsView() {
  return (
    <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
      <h2 className="text-2xl font-bold mb-2">Find & Book Specialist Doctors</h2>
      <p className="text-gray-500 mb-6 text-sm">Consult top-rated verified doctors near your area across 24+ medical categories.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {['Dr. Priya Sharma (Cardiologist)', 'Dr. Anand Verma (Neurologist)'].map((doc, idx) => (
          <div key={idx} className="p-5 border border-gray-100 rounded-2xl bg-gray-50/50 flex justify-between items-center">
            <div>
              <h4 className="font-bold text-gray-800">{doc}</h4>
              <p className="text-xs text-gray-400 mt-1">12+ Years Experience • ⭐ 4.9 (120 reviews)</p>
            </div>
            <button className="bg-blue-600 text-white font-bold text-xs px-4 py-2 rounded-xl">Book Slot</button>
          </div>
        ))}
      </div>
    </div>
  );
}

function MedicinesView() {
  return (
    <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
      <h2 className="text-2xl font-bold mb-2">Pharmacy & Medicine Orders</h2>
      <p className="text-gray-500 mb-6 text-sm">Upload a digital healthcare prescription to automatically match items.</p>
      <div className="border-2 border-dashed border-gray-200 rounded-2xl p-8 text-center bg-gray-50/30">
        <Pill className="w-10 h-10 text-gray-300 mx-auto mb-3" />
        <p className="text-sm font-semibold text-gray-700">Drag & Drop prescription papers here</p>
        <button className="mt-3 bg-gray-800 text-white font-bold text-xs px-4 py-2 rounded-xl">Select File</button>
      </div>
    </div>
  );
}

function LabTestsView() {
  return (
    <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
      <h2 className="text-2xl font-bold mb-2">Diagnostic Lab Packages</h2>
      <p className="text-gray-500 mb-6 text-sm">Free home sample collections with certified digital lab reporting.</p>
      <div className="p-4 border border-blue-100 bg-blue-50/30 rounded-2xl flex justify-between items-center">
        <div>
          <span className="bg-blue-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full uppercase">Popular</span>
          <h4 className="font-bold text-gray-800 mt-1">Complete Full Body Health Checkup</h4>
          <p className="text-xs text-gray-400">Includes 84 fundamental health parameters tests</p>
        </div>
        <span className="text-xl font-black text-blue-600">₹1,499</span>
      </div>
    </div>
  );
}

function HealthLockerView() {
  return (
    <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
      <h2 className="text-2xl font-bold mb-2">Secure Health Locker Storage</h2>
      <p className="text-gray-500 mb-4 text-sm">Your medical records are fully protected under secure sandbox spaces.</p>
      <div className="bg-emerald-50 border border-emerald-100 p-4 rounded-xl text-emerald-800 text-xs font-semibold">
        🔒 Connected with Ayushman Bharat Digital Mission (ABDM) Account
      </div>
    </div>
  );
}

function PrescriptionsView() {
  return (
    <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
      <h2 className="text-2xl font-bold mb-2">Digital Medical Prescriptions</h2>
      <div className="mt-4 border border-gray-100 rounded-xl overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-gray-50 text-xs uppercase text-gray-400 font-bold border-b border-gray-100">
              <th className="p-4">Date</th>
              <th className="p-4">Doctor</th>
              <th className="p-4">Diagnosis</th>
              <th className="p-4">Action</th>
            </tr>
          </thead>
          <tbody className="text-sm font-medium text-gray-700">
            <tr className="border-b border-gray-100">
              <td className="p-4">10 Jun 2026</td>
              <td className="p-4">Dr. Priya Sharma</td>
              <td className="p-4">Hypertension follow-up</td>
              <td className="p-4 text-blue-600 cursor-pointer hover:underline">Download PDF</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

function AIAssistantView() {
  return (
    <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm h-[500px] flex flex-col justify-between">
      <div>
        <h2 className="text-2xl font-bold mb-1">Pranavibhuti AI Assistant</h2>
        <p className="text-gray-500 text-sm">Ask clinical or diagnostic safety queries about your vitals.</p>
        <div className="mt-6 bg-blue-50/50 border border-blue-100 p-4 rounded-2xl max-w-xl text-sm font-medium text-blue-900">
          🤖 Hello Ravi! Your SpO2 and Heart Rate are completely synchronized today. How can I assist you further?
        </div>
      </div>
      <input type="text" placeholder="Ask AI anything..." className="w-full p-4 border border-gray-200 rounded-2xl text-sm bg-gray-50 focus:bg-white outline-none" />
    </div>
  );
}

function VideoCallView() {
  return (
    <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm text-center py-16">
      <Video className="w-16 h-16 text-blue-500 mx-auto mb-4" />
      <h2 className="text-2xl font-bold">Telehealth Consultation Room</h2>
      <p className="text-gray-400 text-sm max-w-sm mx-auto mt-2">Your interactive high-definition encrypted consulting connection room will wake up 5 minutes prior scheduled appointments.</p>
    </div>
  );
}

function VaccinationsView() {
  return (
    <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
      <h2 className="text-2xl font-bold mb-4">Immunization & Vaccination Records</h2>
      <div className="space-y-3">
        {['Hepatitis B Shot', 'Influenza Vaccine Booster'].map((vax, index) => (
          <div key={index} className="p-4 bg-gray-50 border border-gray-100 rounded-2xl flex justify-between items-center">
            <span className="font-bold text-gray-700 text-sm">{vax}</span>
            <span className="text-xs bg-blue-50 text-blue-600 font-bold px-3 py-1 rounded-full">Completed ✓</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function HealthPlansView() {
  return (
    <div className="bg-white p-8 rounded-3xl border border-gray-100 shadow-sm">
      <h2 className="text-2xl font-bold mb-2">Active Care Premium Subscription</h2>
      <p className="text-gray-500 mb-6 text-sm">Your managed medical tier package coverage details.</p>
      <div className="bg-gradient-to-r from-emerald-600 to-teal-600 text-white p-6 rounded-2xl shadow-lg">
        <h3 className="text-xl font-bold">Family Elite Health Coverage</h3>
        <p className="text-xs text-emerald-100 mt-1">Renewal Due date: 15 Jan 2027</p>
      </div>
    </div>
  );
}

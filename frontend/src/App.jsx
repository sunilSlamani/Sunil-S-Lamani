import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Home from './pages/Home';
import Diagnosis from './pages/Diagnosis';
import History from './pages/History';
import CropLibrary from './pages/CropLibrary';
import { translations } from './lib/translations';

function App() {
  const [lang, setLang] = useState(localStorage.getItem('kisan-lang') || 'en');
  const [currentPage, setCurrentPage] = useState('home');
  const t = translations[lang];

  useEffect(() => {
    localStorage.setItem('kisan-lang', lang);
    document.documentElement.lang = lang;
  }, [lang]);

  const toggleLang = () => {
    setLang(prev => prev === 'en' ? 'kn' : 'en');
  };

  const renderPage = () => {
    switch(currentPage) {
      case 'home': return <Home setPage={setCurrentPage} lang={lang} t={t} />;
      case 'diagnosis': return <Diagnosis setPage={setCurrentPage} lang={lang} t={t} />;
      case 'history': return <History setPage={setCurrentPage} lang={lang} t={t} />;
      case 'library': return <CropLibrary setPage={setCurrentPage} lang={lang} t={t} />;
      default: return <Home setPage={setCurrentPage} lang={lang} t={t} />;
    }
  };

  return (
    <div className="max-w-md mx-auto min-h-screen flex flex-col bg-[#F9F8F4] font-sans selection:bg-green-100">
      <Header lang={lang} toggleLang={toggleLang} setPage={setCurrentPage} t={t} />
      
      <main className="flex-1 p-4 pb-24 overflow-y-auto">
        {renderPage()}
      </main>
      
      {/* Bottom Navigation */}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t-2 border-[#D7CCC8] flex justify-around p-2 max-w-md mx-auto shadow-[0_-4px_10px_rgba(0,0,0,0.05)] z-50">
        <button 
          onClick={() => setCurrentPage('home')} 
          className={`flex flex-col items-center justify-center py-2 px-4 rounded-xl transition-all ${currentPage === 'home' ? 'text-[#2E7D32] bg-green-50' : 'text-stone-400'}`}
        >
          <span className="text-2xl mb-1">🏠</span>
          <span className="text-[10px] font-extrabold uppercase tracking-tighter">{t.home}</span>
        </button>
        <button 
          onClick={() => setCurrentPage('diagnosis')} 
          className={`flex flex-col items-center justify-center py-2 px-4 rounded-xl transition-all ${currentPage === 'diagnosis' ? 'text-[#2E7D32] bg-green-50' : 'text-stone-400'}`}
        >
          <span className="text-2xl mb-1">📷</span>
          <span className="text-[10px] font-extrabold uppercase tracking-tighter">{t.diagnose}</span>
        </button>
        <button 
          onClick={() => setCurrentPage('history')} 
          className={`flex flex-col items-center justify-center py-2 px-4 rounded-xl transition-all ${currentPage === 'history' ? 'text-[#2E7D32] bg-green-50' : 'text-stone-400'}`}
        >
          <span className="text-2xl mb-1">📜</span>
          <span className="text-[10px] font-extrabold uppercase tracking-tighter">{t.history}</span>
        </button>
        <button 
          onClick={() => setCurrentPage('library')} 
          className={`flex flex-col items-center justify-center py-2 px-4 rounded-xl transition-all ${currentPage === 'library' ? 'text-[#2E7D32] bg-green-50' : 'text-stone-400'}`}
        >
          <span className="text-2xl mb-1">🌿</span>
          <span className="text-[10px] font-extrabold uppercase tracking-tighter">{t.crops}</span>
        </button>
      </nav>
    </div>
  );
}

export default App;

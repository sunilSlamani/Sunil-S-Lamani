import React, { useState, useEffect } from 'react';
import { getDiagnoses, getCrops } from '../api';

const Home = ({ setPage, lang, t }) => {
  const [recent, setRecent] = useState([]);
  const [crops, setCrops] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [historyData, cropsData] = await Promise.all([
        getDiagnoses(),
        getCrops()
      ]);
      setRecent(historyData.slice(0, 3));
      setCrops(cropsData.slice(0, 4));
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      {/* Hero Section */}
      <section className="bg-white border-2 border-[#D7CCC8] rounded-3xl p-6 shadow-sm space-y-4">
        <div className="flex justify-between items-start">
          <div className="space-y-1">
            <h2 className="text-3xl font-extrabold text-[#2E7D32] leading-tight">
              {t.heroTitle}
            </h2>
            <p className="text-stone-600 font-bold text-sm">
              {t.heroSubtitle}
            </p>
          </div>
          <span className="text-5xl">🌱</span>
        </div>
        
        <button 
          onClick={() => setPage('diagnosis')}
          className="w-full bg-[#E65100] text-white font-extrabold text-xl py-5 rounded-2xl border-b-4 border-orange-900 active:translate-y-1 active:border-b-0 transition-all shadow-lg flex items-center justify-center gap-3"
        >
          <span className="text-2xl">📷</span>
          {t.scanNow}
        </button>
      </section>

      {/* How it works */}
      <section className="space-y-4">
        <h3 className="text-xl font-extrabold text-[#2E7D32] px-2 flex items-center gap-2">
          <span>🛠️</span> {t.howItWorks}
        </h3>
        <div className="grid grid-cols-3 gap-3">
          <div className="bg-white p-3 rounded-2xl border border-[#D7CCC8] text-center space-y-2">
            <span className="text-2xl block">📸</span>
            <p className="text-[10px] font-extrabold text-stone-700 leading-tight uppercase">{t.step1Title}</p>
          </div>
          <div className="bg-white p-3 rounded-2xl border border-[#D7CCC8] text-center space-y-2">
            <span className="text-2xl block">🤖</span>
            <p className="text-[10px] font-extrabold text-stone-700 leading-tight uppercase">{t.step2Title}</p>
          </div>
          <div className="bg-white p-3 rounded-2xl border border-[#D7CCC8] text-center space-y-2">
            <span className="text-2xl block">✅</span>
            <p className="text-[10px] font-extrabold text-stone-700 leading-tight uppercase">{t.step3Title}</p>
          </div>
        </div>
      </section>

      {/* Recent Diagnoses */}
      <section className="space-y-4">
        <div className="flex justify-between items-center px-2">
          <h3 className="text-xl font-extrabold text-[#2E7D32] flex items-center gap-2">
            <span>📜</span> {t.recentDiagnoses}
          </h3>
          <button onClick={() => setPage('history')} className="text-stone-500 font-extrabold text-xs uppercase hover:text-[#2E7D32]">
            {t.viewAll} →
          </button>
        </div>
        
        <div className="space-y-3">
          {recent.length === 0 ? (
            <div className="bg-white/50 border-2 border-dashed border-[#D7CCC8] rounded-2xl p-8 text-center">
              <p className="text-stone-400 font-bold text-sm italic">{t.noDiagnoses}</p>
            </div>
          ) : (
            recent.map((item) => (
              <div key={item.id} className="bg-white p-3 rounded-2xl border border-[#D7CCC8] flex items-center gap-4 shadow-sm">
                <div className="h-14 w-14 rounded-xl overflow-hidden bg-stone-100 border border-stone-200 flex-shrink-0">
                  <img src={`data:image/jpeg;base64,${item.image_base64}`} alt="Crop" className="h-full w-full object-cover" />
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className={`font-extrabold truncate ${item.is_healthy ? 'text-green-700' : 'text-red-700'}`}>
                    {lang === 'en' ? item.disease_name : item.disease_name_kn}
                  </h4>
                  <p className="text-[10px] font-bold text-stone-500 uppercase tracking-tighter">
                    {lang === 'en' ? item.crop_name : item.crop_name_kn} • {new Date(item.timestamp).toLocaleDateString()}
                  </p>
                </div>
                <span className="text-stone-300">›</span>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
};

export default Home;

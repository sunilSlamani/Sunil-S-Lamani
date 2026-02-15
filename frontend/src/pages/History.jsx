import React, { useState, useEffect } from 'react';
import { getDiagnoses, deleteDiagnosis } from '../api';

const History = ({ lang, t }) => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const data = await getDiagnoses();
      setHistory(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm(t.deleteConfirm)) {
      try {
        await deleteDiagnosis(id);
        setHistory(prev => prev.filter(item => item.id !== id));
      } catch (error) {
        console.error(error);
      }
    }
  };

  if (loading) return (
    <div className="flex flex-col items-center justify-center py-20 space-y-4">
      <div className="h-10 w-10 border-4 border-stone-200 border-t-[#2E7D32] rounded-full animate-spin"></div>
      <p className="font-extrabold text-stone-400 uppercase text-xs tracking-widest">{t.loading}</p>
    </div>
  );

  return (
    <div className="space-y-6 animate-in slide-in-from-right duration-500">
      <div className="px-2">
        <h2 className="text-2xl font-extrabold text-[#2E7D32]">
          {t.historyTitle}
        </h2>
        <p className="text-stone-500 font-bold text-xs uppercase tracking-wider">
          {t.historyDesc}
        </p>
      </div>
      
      {history.length === 0 ? (
        <div className="bg-white border-2 border-dashed border-[#D7CCC8] rounded-3xl p-12 text-center space-y-4">
          <span className="text-5xl grayscale opacity-50 block">📜</span>
          <p className="font-bold text-stone-400 italic">
            {t.noHistory}
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {history.map((item) => (
            <div key={item.id} className="bg-white p-4 rounded-3xl border-2 border-[#D7CCC8] flex gap-4 items-center shadow-sm relative overflow-hidden group">
              <div className={`absolute top-0 left-0 h-full w-1.5 ${item.is_healthy ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <div className="h-20 w-20 rounded-2xl overflow-hidden flex-shrink-0 bg-stone-100 border border-stone-200 shadow-inner">
                <img src={`data:image/jpeg;base64,${item.image_base64}`} alt="Crop" className="h-full w-full object-cover" />
              </div>
              <div className="flex-1 min-w-0 space-y-1">
                <h3 className={`font-extrabold text-lg leading-tight truncate ${item.is_healthy ? 'text-green-800' : 'text-red-800'}`}>
                  {lang === 'en' ? item.disease_name : item.disease_name_kn}
                </h3>
                <p className="text-[10px] font-extrabold text-stone-500 uppercase tracking-tighter">
                  {lang === 'en' ? item.crop_name : item.crop_name_kn}
                </p>
                <p className="text-[10px] font-bold text-stone-400 uppercase">
                  {new Date(item.timestamp).toLocaleDateString()}
                </p>
              </div>
              <button 
                onClick={() => handleDelete(item.id)}
                className="p-3 bg-stone-50 text-stone-300 rounded-2xl hover:bg-red-50 hover:text-red-500 transition-all border border-transparent hover:border-red-100"
              >
                <span className="text-xl">🗑️</span>
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default History;

import React, { useState, useEffect } from 'react';
import { getCrops } from '../api';

const CropLibrary = ({ lang, t }) => {
  const [crops, setCrops] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCrops();
  }, []);

  const fetchCrops = async () => {
    try {
      const data = await getCrops();
      setCrops(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getIcon = (iconName) => {
    switch(iconName) {
      case 'tomato': return '🍅';
      case 'potato': return '🥔';
      case 'corn': return '🌽';
      case 'apple': return '🍎';
      case 'grape': return '🍇';
      case 'rice': return '🌾';
      case 'pepper': return '🫑';
      case 'cherry': return '🍒';
      case 'strawberry': return '🍓';
      case 'peach': return '🍑';
      default: return '🌿';
    }
  };

  if (loading) return (
    <div className="flex flex-col items-center justify-center py-20 space-y-4">
      <div className="h-10 w-10 border-4 border-stone-200 border-t-[#2E7D32] rounded-full animate-spin"></div>
      <p className="font-extrabold text-stone-400 uppercase text-xs tracking-widest">{t.loading}</p>
    </div>
  );

  return (
    <div className="space-y-6 animate-in slide-in-from-right duration-500 pb-10">
      <div className="px-2">
        <h2 className="text-2xl font-extrabold text-[#2E7D32]">
          {t.cropsTitle}
        </h2>
        <p className="text-stone-500 font-bold text-xs uppercase tracking-wider">
          {t.cropsDesc}
        </p>
      </div>
      
      <div className="grid grid-cols-1 gap-5">
        {crops.map((crop, index) => (
          <div key={index} className="bg-white p-6 rounded-3xl border-2 border-[#D7CCC8] space-y-4 shadow-sm active:scale-[0.98] transition-transform">
            <div className="flex items-center gap-4">
              <div className="bg-stone-50 h-16 w-16 rounded-2xl flex items-center justify-center text-4xl shadow-inner border border-stone-100">
                {getIcon(crop.icon)}
              </div>
              <div>
                <h3 className="text-2xl font-extrabold text-stone-800 leading-none mb-1">
                  {lang === 'en' ? crop.name : crop.name_kn}
                </h3>
                <p className="text-[10px] font-extrabold text-[#2E7D32] uppercase tracking-widest">
                  {crop.common_diseases.length} {lang === 'en' ? 'Diseases tracked' : 'ರೋಗಗಳು'}
                </p>
              </div>
            </div>
            
            <div className="space-y-2">
              <p className="text-[10px] font-extrabold text-stone-400 uppercase px-1 tracking-widest">
                {t.commonDiseases}
              </p>
              <div className="flex flex-wrap gap-2">
                {(lang === 'en' ? crop.common_diseases : crop.common_diseases_kn).map((disease, i) => (
                  <span key={i} className="bg-stone-50 text-stone-700 text-xs font-bold px-4 py-2 rounded-xl border border-stone-100 shadow-sm">
                    {disease}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CropLibrary;

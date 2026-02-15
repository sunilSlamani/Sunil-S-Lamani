import React, { useState, useRef } from 'react';
import { diagnoseImage, generateTTS } from '../api';

const Diagnosis = ({ lang, t }) => {
  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const fileInputRef = useRef(null);
  const audioRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
      };
      reader.readAsDataURL(selectedFile);
      setResult(null);
    }
  };

  const handleDiagnose = async () => {
    if (!file) return;
    setLoading(true);
    try {
      const data = await diagnoseImage(file, lang);
      setResult(data);
      // Auto-speak results
      setTimeout(() => speak(data), 500);
    } catch (error) {
      console.error(error);
      alert(t.error);
    } finally {
      setLoading(false);
    }
  };

  const speak = async (dataResult = result) => {
    if (!dataResult) return;
    if (isPlaying) {
      audioRef.current?.pause();
      setIsPlaying(false);
      return;
    }

    const text = lang === 'en' ? dataResult.description : dataResult.description_kn;
    try {
      setIsPlaying(true);
      const audioBase64 = await generateTTS(text, lang);
      const audio = new Audio(`data:audio/mp3;base64,${audioBase64}`);
      audioRef.current = audio;
      audio.onended = () => setIsPlaying(false);
      audio.play();
    } catch (error) {
      console.error('TTS failed', error);
      setIsPlaying(false);
    }
  };

  return (
    <div className="space-y-6 animate-in slide-in-from-right duration-500 pb-10">
      <section className="bg-white border-2 border-[#D7CCC8] rounded-3xl p-6 shadow-sm space-y-5">
        <div className="space-y-1">
          <h2 className="text-2xl font-extrabold text-[#2E7D32]">
            {t.uploadTitle}
          </h2>
          <p className="text-stone-500 font-bold text-xs uppercase tracking-wider">
            {t.uploadDesc}
          </p>
        </div>
        
        <div 
          onClick={() => fileInputRef.current.click()}
          className={`border-4 border-dashed rounded-3xl h-72 flex flex-col items-center justify-center cursor-pointer overflow-hidden transition-all bg-stone-50 ${image ? 'border-[#2E7D32]' : 'border-[#D7CCC8]'}`}
        >
          {image ? (
            <div className="relative h-full w-full group">
              <img src={image} alt="Selected" className="h-full w-full object-cover" />
              <div className="absolute inset-0 bg-black/20 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span className="bg-white px-4 py-2 rounded-xl font-bold text-stone-700">{t.uploadFile}</span>
              </div>
            </div>
          ) : (
            <div className="text-center p-6 space-y-4">
              <div className="bg-stone-200 w-20 h-20 rounded-full flex items-center justify-center mx-auto shadow-inner">
                <span className="text-4xl">📸</span>
              </div>
              <p className="font-extrabold text-stone-400 text-sm uppercase tracking-widest leading-relaxed">
                {t.takePhoto} <br/> <span className="text-xs text-stone-300">({t.orText})</span> <br/> {t.uploadFile}
              </p>
            </div>
          )}
        </div>

        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          accept="image/*" 
          capture="environment" 
          className="hidden" 
        />

        {!result && (
          <button 
            onClick={handleDiagnose}
            disabled={!file || loading}
            className={`w-full font-extrabold text-xl py-5 rounded-2xl border-b-4 transition-all shadow-lg flex items-center justify-center gap-3 ${!file || loading ? 'bg-stone-200 text-stone-400 border-stone-300' : 'bg-[#E65100] text-white border-orange-900 active:translate-y-1 active:border-b-0'}`}
          >
            {loading ? (
              <>
                <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                {t.analyzing}
              </>
            ) : (
              <>
                <span className="text-2xl">🔍</span>
                {t.analyzeBtn}
              </>
            )}
          </button>
        )}
      </section>

      {result && (
        <section className={`bg-white border-2 rounded-3xl p-6 shadow-md animate-in zoom-in-95 duration-500 ${result.is_healthy ? 'border-green-400 ring-4 ring-green-50' : 'border-red-400 ring-4 ring-red-50'}`}>
          <div className="flex justify-between items-start mb-6">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className={`h-3 w-3 rounded-full animate-pulse ${result.is_healthy ? 'bg-green-500' : 'bg-red-500'}`}></span>
                <span className={`font-extrabold text-xs uppercase tracking-widest ${result.is_healthy ? 'text-green-600' : 'text-red-600'}`}>
                  {result.is_healthy ? t.healthy : t.diseased}
                </span>
              </div>
              <h3 className={`text-2xl font-extrabold leading-tight ${result.is_healthy ? 'text-green-900' : 'text-red-900'}`}>
                {lang === 'en' ? result.disease_name : result.disease_name_kn}
              </h3>
              <p className="text-stone-500 font-bold uppercase text-[10px] tracking-tighter">
                {t.cropLabel}: {lang === 'en' ? result.crop_name : result.crop_name_kn} • {t.confidenceLabel}: {result.confidence}
              </p>
            </div>
            <button 
              onClick={() => speak()}
              className={`p-4 rounded-2xl shadow-lg border-2 active:scale-90 transition-all ${isPlaying ? 'bg-red-500 border-red-700 text-white animate-pulse' : 'bg-white border-stone-200 text-[#2E7D32]'}`}
            >
              <span className="text-2xl">{isPlaying ? '⏹️' : '🔊'}</span>
            </button>
          </div>

          <div className="space-y-6">
            <div className="bg-stone-50 p-4 rounded-2xl border border-stone-100 relative overflow-hidden">
              <div className={`absolute top-0 left-0 h-full w-1 ${result.is_healthy ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <p className="text-stone-400 text-[10px] font-extrabold uppercase mb-2 tracking-widest flex items-center gap-1">
                <span>💬</span> {t.descriptionLabel}
              </p>
              <p className="text-stone-800 font-bold leading-relaxed">
                {lang === 'en' ? result.description : result.description_kn}
              </p>
            </div>

            <div className="grid grid-cols-1 gap-4">
              <div className="space-y-2">
                <p className="text-stone-400 text-[10px] font-extrabold uppercase px-2 tracking-widest flex items-center gap-1">
                  <span>💡</span> {t.symptomsLabel}
                </p>
                <div className="flex flex-wrap gap-2">
                  {(lang === 'en' ? result.symptoms : result.symptoms_kn).map((s, i) => (
                    <span key={i} className="bg-white px-4 py-2 rounded-xl border border-stone-200 text-sm font-bold text-stone-700 shadow-sm">
                      {s}
                    </span>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <p className="text-stone-400 text-[10px] font-extrabold uppercase px-2 tracking-widest flex items-center gap-1">
                  <span>💊</span> {t.treatmentLabel}
                </p>
                <div className="space-y-2">
                  {(lang === 'en' ? result.treatment : result.treatment_kn).map((t_text, i) => (
                    <div key={i} className="bg-green-50 p-3 rounded-xl border border-green-100 text-sm font-bold text-green-800 flex items-start gap-2">
                      <span className="text-green-500 mt-0.5">✓</span>
                      {t_text}
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            <button 
              onClick={() => {
                setResult(null);
                setImage(null);
                setFile(null);
              }}
              className="w-full bg-stone-100 text-stone-600 font-extrabold py-4 rounded-2xl border-b-4 border-stone-300 active:translate-y-1 active:border-b-0 transition-all uppercase text-xs tracking-widest"
            >
              {t.newScan}
            </button>
          </div>
        </section>
      )}
    </div>
  );
};

export default Diagnosis;

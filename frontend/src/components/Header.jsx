import React from 'react';

const Header = ({ lang, toggleLang, setPage, t }) => {
  return (
    <header className="flex justify-between items-center p-4 bg-white border-b-2 border-[#D7CCC8] sticky top-0 z-40">
      <div onClick={() => setPage('home')} className="cursor-pointer active:opacity-70 transition-opacity">
        <h1 className="text-2xl font-extrabold text-[#2E7D32] tracking-tight leading-none">
          {t.appName}
        </h1>
        <p className="text-stone-500 font-bold text-[10px] uppercase tracking-widest mt-1">
          {t.appSubtitle}
        </p>
      </div>
      <button 
        onClick={toggleLang} 
        className="bg-[#2E7D32] text-white p-3 rounded-2xl font-extrabold text-lg min-w-[56px] h-14 border-b-4 border-green-900 flex items-center justify-center active:translate-y-1 active:border-b-0 transition-all shadow-md"
      >
        {t.languageToggle}
      </button>
    </header>
  );
};

export default Header;

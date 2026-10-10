import React, { createContext, useContext, useState } from 'react';
import { translations } from '../i18n/translations';
import type { LanguageCode } from '../i18n/translations';

interface LanguageContextType {
    language: LanguageCode;
    setLanguage: (lang: LanguageCode) => void;
    t: (key: string) => string;
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export const LanguageProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [language, setLanguageState] = useState<LanguageCode>(() => {
        const saved = localStorage.getItem('kisan_lang');
        return (saved as LanguageCode) || 'hi';
    });

    const setLanguage = (lang: LanguageCode) => {
        setLanguageState(lang);
        localStorage.setItem('kisan_lang', lang);
    };

    const t = (key: string): string => {
        const dictionary = translations[language] as any;
        return dictionary[key] || translations['en'][key as keyof typeof translations['en']] || key;
    };

    return (
        <LanguageContext.Provider value={{ language, setLanguage, t }}>
            {children}
        </LanguageContext.Provider>
    );
};

export const useLanguage = () => {
    const context = useContext(LanguageContext);
    if (!context) {
        throw new Error('useLanguage must be used within a LanguageProvider');
    }
    return context;
};

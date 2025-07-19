import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import HttpApi from 'i18next-http-backend';

i18n
  .use(HttpApi)
  .use(initReactI18next)
  .init({
    lng: localStorage.getItem('language') || 'de', // Default to German
    fallbackLng: 'de',
    debug: false,

    interpolation: {
      escapeValue: false, // React already does escaping
    },

    backend: {
      loadPath: '/locales/{{lng}}/translation.json',
    },

    react: {
      useSuspense: false,
    },
  });

export default i18n;


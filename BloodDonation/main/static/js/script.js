// ======================================
// ELEMENTS
// ======================================

const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.getElementById('themeIcon');

const langToggle = document.getElementById('langToggle');

// ======================================
// SAVED SETTINGS
// ======================================

let currentTheme =
  localStorage.getItem('ehyaa-theme') || 'light';

let currentLang =
  localStorage.getItem('ehyaa-lang') || 'ar';

// ======================================
// TRANSLATIONS
// ======================================

const translations = {

  ar: {
    nav_home: 'الرئيسية',
    nav_about: 'عن المنصة',
    nav_how: 'كيف يعمل',
    nav_faq: 'الأسئلة الشائعة',

    footer_desc:
      'منصة إحياء تربط المتبرعين بالدم مع المستشفيات في المملكة العربية السعودية.',

    quick_links: 'روابط سريعة',
    for_donors: 'للمتبرعين',
    contact_us: 'تواصل معنا',

    donor_register: 'تسجيل متبرع',
    donor_guide: 'دليل التبرع',
    eligibility: 'شروط التبرع',
    blood_info: 'فصائل الدم',
    hospitals_list: 'قائمة المستشفيات',

    addr: 'الرياض، المملكة العربية السعودية',

    rights: 'جميع الحقوق محفوظة',

    privacy: 'سياسة الخصوصية',
    terms: 'الشروط والأحكام',
  },

  en: {
    nav_home: 'Home',
    nav_about: 'About',
    nav_how: 'How It Works',
    nav_faq: 'FAQ',

    footer_desc:
      'Ehyaa connects blood donors with hospitals across Saudi Arabia.',

    quick_links: 'Quick Links',
    for_donors: 'For Donors',
    contact_us: 'Contact Us',

    donor_register: 'Donor Registration',
    donor_guide: 'Donation Guide',
    eligibility: 'Eligibility',
    blood_info: 'Blood Types',
    hospitals_list: 'Hospitals List',

    addr: 'Riyadh, Saudi Arabia',

    rights: 'All Rights Reserved',

    privacy: 'Privacy Policy',
    terms: 'Terms & Conditions',
  }
};

// ======================================
// APPLY THEME
// ======================================

function applyTheme(theme) {

  document.documentElement.setAttribute(
    'data-theme',
    theme
  );

  if (theme === 'dark') {
    themeIcon.textContent = '☀️';
  } else {
    themeIcon.textContent = '🌙';
  }

  localStorage.setItem('ehyaa-theme', theme);
}

// ======================================
// APPLY LANGUAGE
// ======================================

function applyLanguage(lang) {

  const html = document.documentElement;

  // RTL / LTR
  if (lang === 'ar') {

    html.lang = 'ar';
    html.dir = 'rtl';

    langToggle.textContent = 'EN';

  } else {

    html.lang = 'en';
    html.dir = 'ltr';

    langToggle.textContent = 'عربي';
  }

  // Translate all elements
  document.querySelectorAll('[data-t]')
    .forEach(el => {

      const key = el.getAttribute('data-t');

      if (translations[lang][key]) {
        el.textContent = translations[lang][key];
      }

    });

  localStorage.setItem('ehyaa-lang', lang);
}

// ======================================
// THEME TOGGLE
// ======================================

themeToggle.addEventListener('click', () => {

  currentTheme =
    currentTheme === 'light'
      ? 'dark'
      : 'light';

  applyTheme(currentTheme);
});

// ======================================
// LANGUAGE TOGGLE
// ======================================

langToggle.addEventListener('click', () => {

  currentLang =
    currentLang === 'ar'
      ? 'en'
      : 'ar';

  applyLanguage(currentLang);
});

// ======================================
// INITIAL LOAD
// ======================================

document.addEventListener('DOMContentLoaded', () => {

  applyTheme(currentTheme);

  applyLanguage(currentLang);

});
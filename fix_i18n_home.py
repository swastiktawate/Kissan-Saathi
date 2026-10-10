import json

with open('frontend/src/i18n/translations.ts', 'r', encoding='utf-8') as f:
    text = f.read()

en_add = """
        crop_tomato: "Tomato",
        crop_onion: "Onion",
        crop_potato: "Potato",
        crop_banana: "Banana",
        action_wait_3_days: "Wait 3 Days",
        reason_rain: "Arrivals are low due to rain. Prices may reach ₹2,400.",
        action_sell_now: "Sell Immediately",
        reason_export_ban: "Government has imposed an export ban. Prices may drop.",
        action_sell_today: "Sell Today",
        reason_aloo: "Prices are stable. Good time to sell before weekend.",
        reason_kela: "High demand in local markets. Prices are peaking.",
        today_price_for: "Today's Mandi Bhav",
        better_mandi_options: "Better Mandi Options",
        see_all: "See All",
        km_away: "km away",
        best_option: "Best Option",
"""

hi_add = """
        crop_tomato: "टमाटर",
        crop_onion: "प्याज़",
        crop_potato: "आलू",
        crop_banana: "केला",
        action_wait_3_days: "3 दिन रुकिए",
        reason_rain: "बारिश की वजह से आवक कम है। दाम ₹2,400 तक जा सकते हैं।",
        action_sell_now: "तुरंत बेचिए",
        reason_export_ban: "सरकार ने निर्यात पर रोक लगा दी है, आने वाले दिनों में दाम गिर सकते हैं।",
        action_sell_today: "अभी बेचिए",
        reason_aloo: "भाव स्थिर हैं। सप्ताहांत से पहले बेचना सही रहेगा।",
        reason_kela: "स्थानीय बाज़ार में अच्छी मांग है। दाम अच्छे हैं।",
        today_price_for: "आज का मंडी भाव",
        better_mandi_options: "बेहतर मंडी विकल्प",
        see_all: "सब देखें",
        km_away: "किमी दूर",
        best_option: "सबसे अच्छा विकल्प",
"""

mr_add = """
        crop_tomato: "टोमॅटो",
        crop_onion: "कांदा",
        crop_potato: "बटाटा",
        crop_banana: "केळी",
        action_wait_3_days: "3 दिवस थांबा",
        reason_rain: "पावसामुळे आवक कमी आहे. भाव ₹2,400 पर्यंत जाऊ शकतात.",
        action_sell_now: "लगेच विका",
        reason_export_ban: "सरकारने निर्यात बंदी लागू केली आहे, भाव पडण्याची शक्यता आहे.",
        action_sell_today: "आत्ता विका",
        reason_aloo: "दर स्थिर आहेत. आठवड्या अखेरीस आधी विकणे योग्य.",
        reason_kela: "स्थानिक बाजारात चांगली मागणी आहे. दर वाढले आहेत.",
        today_price_for: "आजचा बाजार भाव",
        better_mandi_options: "उत्तम बाजार पर्याय",
        see_all: "सर्व पहा",
        km_away: "किमी दूर",
        best_option: "उत्तम पर्याय",
"""

hr_add = """
        crop_tomato: "टमाटर",
        crop_onion: "कांदा",
        crop_potato: "आलू",
        crop_banana: "केला",
        action_wait_3_days: "3 दिन डट जा",
        reason_rain: "बारिश तै माल कम आवै सै। भाव ₹2,400 तक जा सकै सै।",
        action_sell_now: "झटपट बेच दे",
        reason_export_ban: "सरकार नै बाहर भेजन पे रोक ला दी, भाव गिर सकै सैं।",
        action_sell_today: "इब्बै बेच",
        reason_aloo: "भाव टिके होये सैं। ठीक टेम सै।",
        reason_kela: "लोकल मंडी म घणी मांग सै।",
        today_price_for: "आज का भाव",
        better_mandi_options: "बढ़िया मंडी",
        see_all: "सारै देख",
        km_away: "किमी दूर",
        best_option: "कसूता विकल्प",
"""

pa_add = """
        crop_tomato: "ਟਮਾਟਰ",
        crop_onion: "ਪਿਆਜ਼",
        crop_potato: "ਆਲੂ",
        crop_banana: "ਕੇਲਾ",
        action_wait_3_days: "3 ਦਿਨ ਉਡੀਕੋ",
        reason_rain: "ਮੀਂਹ ਕਾਰਨ ਫਸਲ ਘੱਟ ਆ ਰਹੀ ਹੈ। ਭਾਅ ₹2,400 ਤੱਕ ਜਾ ਸਕਦੇ ਹਨ।",
        action_sell_now: "ਹੁਣੇ ਵੇਚੋ",
        reason_export_ban: "ਸਰਕਾਰ ਨੇ ਨਿਰਯਾਤ 'ਤੇ ਪਾਬੰਦੀ ਲਗਾ ਦਿੱਤੀ ਹੈ, ਭਾਅ ਡਿੱਗ ਸਕਦੇ ਹਨ।",
        action_sell_today: "ਅੱਜ ਵੇਚੋ",
        reason_aloo: "ਕੀਮਤਾਂ ਸਥਿਰ ਹਨ। ਵੇਚਣ ਦਾ ਸਹੀ ਸਮਾਂ ਹੈ।",
        reason_kela: "ਮੰਡੀ ਵਿੱਚ ਚੰਗੀ ਮੰਗ ਹੈ।",
        today_price_for: "ਅੱਜ ਦਾ ਭਾਅ",
        better_mandi_options: "ਵਧੀਆ ਮੰਡੀ ਵਿਕਲਪ",
        see_all: "ਸਾਰੇ ਦੇਖੋ",
        km_away: "ਕਿਮੀ ਦੂਰ",
        best_option: "ਸਭ ਤੋਂ ਵਧੀਆ ਵਿਕਲਪ",
"""

text = text.replace('version: "Version v0.1.0-hackathon (Syrus 7.0)"\n    },', 'version: "Version v0.1.0-hackathon (Syrus 7.0)",\n' + en_add + '    },')
text = text.replace('version: "संस्करण v0.1.0-hackathon"\n    },', 'version: "संस्करण v0.1.0-hackathon",\n' + hi_add + '    },')
text = text.replace('version: "आवृत्ती v0.1.0-hackathon"\n    },', 'version: "आवृत्ती v0.1.0-hackathon",\n' + mr_add + '    },')
text = text.replace('version: "वर्जन v0.1.0-hackathon"\n    },', 'version: "वर्जन v0.1.0-hackathon",\n' + hr_add + '    },')
text = text.replace('version: "ਵਰਜਨ v0.1.0-hackathon"\n    }', 'version: "ਵਰਜਨ v0.1.0-hackathon",\n' + pa_add + '    }')

with open('frontend/src/i18n/translations.ts', 'w', encoding='utf-8') as f:
    f.write(text)

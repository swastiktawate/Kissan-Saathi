import re
with open('frontend/src/pages/Home.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('QUICK ACCESS\n', "{t('quick_access')}\n")
c = c.replace('>Cold Storage<', ">{t('cold_storage')}<")
c = c.replace('>Find nearby storage<', ">{t('find_nearby')}<")
c = c.replace('>Farmer Pooling<', ">{t('farmer_pooling')}<")
c = c.replace('>Sell together, save transport<', ">{t('sell_together')}<")
c = c.replace('>Meri Faslein<', ">{t('meri_faslein')}<")
c = c.replace('>Aaj ka Mandi Bhav<', ">{t('aaj_ka_bhav')}<")
c = c.replace('>Hamari Salah<', ">{t('hamari_salah')}<")
c = c.replace('>Kyun?<', ">{t('kyu')}<")

with open('frontend/src/pages/Home.tsx', 'w', encoding='utf-8') as f:
    f.write(c)

"""Generate report tables and numerical macros from executed notebook CSV exports."""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'report' / 'report_tables'
OUT.mkdir(parents=True, exist_ok=True)

def read(name):
    return pd.read_csv(ROOT / 'tables' / f'{name}.csv')

def table(name, data, digits=2):
    data = data.copy()
    for col in data:
        if pd.api.types.is_float_dtype(data[col]):
            data[col] = data[col].map(lambda x: f'{x:,.{digits}f}' if pd.notna(x) else '—')
        elif pd.api.types.is_integer_dtype(data[col]):
            data[col] = data[col].map(lambda x: f'{x:,}')
    latex = data.to_latex(index=False, escape=True).replace('≥', r'$\geq$').replace('–', '--').replace('—', '---')
    (OUT / f'{name}.tex').write_text(latex, encoding='utf-8')

def pvalue(x):
    return '< 1e-300*' if x == 0 else f'{x:.2e}'

macros = {}
def macro(name, value, digits=1):
    macros[name] = f'{value:,.{digits}f}' if not isinstance(value,str) else value

names = {'barcelona':'Barcelona','madrid':'Madrid','los_angeles':'Los Angeles','new_york':'New York','tokyo':'Tokyo','mexico_city':'Mexico City'}
a = read('data_audit')
a['City'] = a.city.map(names)
a['Dates'] = a.scraped_from.str[5:] + ' to ' + a.scraped_to.str[5:]
table('data_audit', a[['City','listings','Dates','missing_price_pct','missing_bedrooms']].rename(columns={'listings':'Listings','missing_price_pct':'Price missing (%)','missing_bedrooms':'Bedrooms missing'}),1)
macro('TotalListings',a.listings.sum(),0)
macro('TotalPriced',a.listings.sum()-a.missing_price.sum(),0)
macro('TotalSpain',a.loc[a.city.isin(['barcelona','madrid']),'listings'].sum(),0)

h=read('study02_host_shares').rename(columns={'city_name':'City'})
top=read('study02_top5')[['City','Top 5% Market Share (%)']]
table('host_shares',h.merge(top,on='City'),1)
w=read('study02_weighting')
macro('MegaPooled',w.loc[w.iloc[:,0].eq('Megahost (5+)'),'pooled_listing_share_pct'].iloc[0])
macro('MegaAverage',w.loc[w.iloc[:,0].eq('Megahost (5+)'),'equal_city_average_pct'].iloc[0])
macro('SinglePooled',w.loc[w.iloc[:,0].eq('Single-host (1)'),'pooled_listing_share_pct'].iloc[0])
r=read('study02_ratings')
r['Metric']=r.metric.str.replace('review_scores_','').str.title()
r['p']=r.p_value.map(pvalue)
table('host_ratings',r[['Metric','n_single','n_mega','median_single','median_mega','prob_superiority','p']].rename(columns={'n_single':'n (single)','n_mega':'n (5+)','median_single':'Median (1)','median_mega':'Median (5+)','prob_superiority':'U/(n1 n2)'}),3)
comp=read('study02_room_composition')
macro('MegaEntire',comp.loc[comp.iloc[:,0].eq('Megahost (5+)'),'Entire home/apt'].iloc[0])
macro('SingleEntire',comp.loc[comp.iloc[:,0].eq('Single-host (1)'),'Entire home/apt'].iloc[0])

p=read('study03_price_stats')
table('price_stats',p[['City','Currency','Offers','Mean','Median','IQR','Outliers (%)']])
table('price_shape',p[['City','Mean / Median','Rel IQR (%)','Skewness','Kurtosis']])
t=read('study03_price_test').iloc[0]
macro('PriceU',t.U,0);macro('PriceP',pvalue(t.p_value));macro('PriceSuperiority',t.prob_superiority,3)

r=read('study04_tests')
table('room_medians',r[['City','Currency','Median Entire','Median Private','Private Discount (%)']])
table('room_tests',r[['City','ANOVA F-stat','ANOVA p-val','Welch t-stat','Welch p-val','MWU p-val']])

r=read('study05_summary')
table('rental_summary',r[['city_name','short_stay_pct','monthly_pct','monthly_peak_nights','inactive_pct','switches_pct','implausible_pct_of_monthly']].rename(columns={'city_name':'City','short_stay_pct':'1–6 (%)','monthly_pct':'30+ (%)','monthly_peak_nights':'Peak (nights)','inactive_pct':'Zero/review (%)','switches_pct':'Spans (%)','implausible_pct_of_monthly':'Flag (%)'}),1)
r=read('study05_licence')
table('rental_licence',r.rename(columns={r.columns[0]:'Recorded licence text'}),1)
r=read('study05_reviews_by_model')
table('rental_reviews',r.pivot(index='city_name',columns='rental_model',values='median_reviews_ltm').reset_index().rename(columns={'city_name':'City'}),1)

s=read('study06_city_summary');s['City']=s.city.map(names)
table('short_city',s[['City','listings','short_entire','share_pct']].rename(columns={'listings':'All listings','short_entire':'Entire, 1–29','share_pct':'Share (%)'}),1)
for key, label in [('barcelona','Bcn'),('madrid','Mad')]:
    row=s[s.city.eq(key)].iloc[0]
    macro(label+'ShortN',row.short_entire,0);macro(label+'ShortPct',row.share_pct)
top=read('study06_top_neighbourhoods');top['City']=top.city.map(names)
table('short_top',top[['City','neighbourhood_cleansed','listings','short_entire','share_pct']].rename(columns={'neighbourhood_cleansed':'Neighbourhood','listings':'All','short_entire':'Segment','share_pct':'Share (%)'}),1)
j=read('study06_join_audit');j['City']=j.city.map(names)
table('join_audit',j[['City','listing_neighbourhoods','polygon_names','unmatched','small_sample','polygons_without_listings']].rename(columns={'listing_neighbourhoods':'With listings','polygon_names':'GeoJSON names','unmatched':'Unmatched','small_sample':'n < 20','polygons_without_listings':'No listings'}),0)

m=read('study07_monthly_cost')
table('monthly_cost',m.rename(columns={'city_name':'City','room_type':'Accommodation','n':'n','q1':'Q1 (EUR)','median':'Median (EUR)','q3':'Q3 (EUR)'}))
for city,label in [('Barcelona','Bcn'),('Madrid','Mad')]:
    for room,suffix in [('Entire home/apt','Entire'),('Private room','Private')]:
        row=m[m.city_name.eq(city)&m.room_type.eq(room)].iloc[0]
        macro(label+suffix+'Monthly',row['median'],0);macro(label+suffix+'MonthlyN',row.n,0)
d=read('study07_quote_dates')
for c in ['checkin_min','checkin_median','checkin_max']:d[c]=d[c].str[:10]
table('monthly_dates',d[['city_name','room_type','checkin_min','checkin_median','checkin_max']].rename(columns={'city_name':'City','room_type':'Accommodation','checkin_min':'First check-in','checkin_median':'Median check-in','checkin_max':'Last check-in'}))
f=read('study07_filter_audit');f['City']=f.city.map(names)
table('monthly_audit',f[['City','target_room_types','quote_28_35','positive_total','valid_quotes']].rename(columns={'target_room_types':'Target types','quote_28_35':'28–35 nights','positive_total':'Positive total','valid_quotes':'Valid EUR quote'}))
months=read('study07_quote_months').groupby(['city_name','checkin_month']).n.sum().unstack(fill_value=0).reset_index().rename(columns={'city_name':'City'})
table('monthly_months',months)

c=read('study08_coefficients')
labels={'Intercept':'Intercept','C(city)[T.madrid]':'Madrid (ref. Barcelona)','C(room_type)[T.Private room]':'Private room (ref. entire)','C(room_type)[T.Hotel room]':'Hotel room (ref. entire)','C(room_type)[T.Shared room]':'Shared room (ref. entire)','log_accommodates':'log(capacity)','bedrooms':'Bedrooms','log1p_minimum_nights':'log(1 + minimum nights)'}
c['Term']=c.term.map(labels).fillna(c.term)
c['p']=c.p_value.map(pvalue)
table('regression',c[['Term','coefficient','std_error_HC3','ci_low','ci_high','p']].rename(columns={'coefficient':'Estimate','std_error_HC3':'SE (HC3)','ci_low':'95% lower','ci_high':'95% upper'}),3)
fit=read('study08_fit').iloc[0]
macro('ModelN',fit.n,0);macro('ModelRSq',fit.r_squared,3);macro('ModelAdjRSq',fit.adjusted_r_squared,3)
macro('ModelRank',fit['rank'],0);macro('ModelCols',fit['columns'],0);macro('ModelCondition',fit.condition_number,1)
city=c[c.term.str.contains('madrid',case=False)].iloc[0]
macro('CityPct',100*np.expm1(city.coefficient));macro('CityLow',100*np.expm1(city.ci_low));macro('CityHigh',100*np.expm1(city.ci_high))
a=read('study08_filter_audit');a['City']=a.city.map(names)
table('regression_audit',a[['City','all_listings','missing_price','missing_bedrooms','complete_model','excluded']].rename(columns={'all_listings':'All','missing_price':'Missing price','missing_bedrooms':'Missing bedrooms','complete_model':'Model n','excluded':'Excluded'}))

r=read('study09_spearman');r['City']=r.city.map(names);r['p']=r.p_value.map(pvalue)
r['Sample']=r['sample'].replace({'First review at least one year earlier':'First review ≥ 1 year earlier'})
table('activity',r[['City','Sample','n','rho','p']],3)
for city,label in [('barcelona','Bcn'),('madrid','Mad')]:
    row=r[r.city.eq(city)&r['sample'].eq('All eligible')].iloc[0]
    macro(label+'Rho',row.rho,3);macro(label+'ActivityN',row.n,0)
    row=r[r.city.eq(city)&r['sample'].ne('All eligible')].iloc[0]
    macro(label+'EstablishedRho',row.rho,3)
a=read('study09_filter_audit');a['City']=a.city.map(names)
table('activity_audit',a[['City','short_entire','valid_price_and_reviews','established']].rename(columns={'short_entire':'Entire, 1–29 nights','valid_price_and_reviews':'Valid price/reviews','established':'First review ≥ 1 year earlier'}))

(ROOT/'report'/'results.tex').write_text('% Generated by scripts/build_report.py; do not edit numeric results manually.\n'+ '\n'.join('\\newcommand{\\'+k+'}{'+v.replace('%',r'\%')+'}' for k,v in macros.items())+'\n',encoding='utf-8')
print(f'Generated {len(list(OUT.glob("*.tex")))} tables and {len(macros)} numerical macros.')

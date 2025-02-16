from tqdm import tqdm
import pandas as pd
from pandas import json_normalize


def clean_data(data):
    df = json_normalize(data, sep='_')
    df = df.drop(columns=[
        'thumbnail', 'externalReference', 'numPhotos', 'priceInfo_price_amount',
        'priceInfo_price_currencySuffix', 'contactInfo_phone1_phoneNumber',
        'contactInfo_phone1_formattedPhone', 'contactInfo_phone1_prefix',
        'contactInfo_phone1_nationalNumber', 'url', 'suggestedTexts_subtitle',
        'suggestedTexts_title', 'priceDropValue', 'priceDropPercentage',
        'priceInfo_price_priceDropInfo_priceDropValue', 'priceInfo_price_priceDropInfo_priceDropPercentage',
        'labels', 'priceByArea'
    ])

    df = df.rename(columns={'priceInfo_price_priceDropInfo_formerPrice': 'formerPrice'})
    df['floor'] = df['floor'].replace({'en': 0.5, 'bj': 0, 'ss': -0.5, 'st': -1})
    df = df.drop_duplicates(subset=['propertyCode'], keep='first')
    df['firstActivationDate'] = pd.to_datetime(df['firstActivationDate'], unit='ms')
    df['dropDate'] = pd.to_datetime(df['dropDate'], unit='ms')

    location = df[['locationId', 'neighborhood', 'district', 'municipality', 'province', 'country']].copy()
    location = location.drop_duplicates(subset=['locationId'], keep='first')
    df = df.drop(columns=['neighborhood', 'district', 'municipality', 'province', 'country'])

    videos = pd.DataFrame()
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing videos"):
        multimedia_videos = row.get('multimedia_videos', None)
        if not isinstance(multimedia_videos, list) or not multimedia_videos:
            continue
        for video in multimedia_videos:
            _normalized = json_normalize(video)
            if 'id' in _normalized.columns:
                _normalized = _normalized.rename(columns={'id': 'multimediaId'})
            _normalized['propertyCode'] = row['propertyCode']
            videos = pd.concat([videos, _normalized], ignore_index=True)
    df.drop(columns=['multimedia_videos'], inplace=True)

    images = pd.DataFrame()
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing images"):
        multimedia_images = row.get('multimedia_images', None)
        if not isinstance(multimedia_images, list) or not multimedia_images:
            continue
        for image in multimedia_images:
            _normalized = json_normalize(image)
            if 'id' in _normalized.columns:
                _normalized = _normalized.rename(columns={'id': 'multimediaId'})
            _normalized['propertyCode'] = row['propertyCode']
            images = pd.concat([images, _normalized], ignore_index=True)
    df.drop(columns=['multimedia_images'], inplace=True)

    virtual3DTours = pd.DataFrame()
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing 3D Tours"):
        multimedia_virtual3DTours = row.get('multimedia_virtual3DTours', None)
        if not isinstance(multimedia_virtual3DTours, list) or not multimedia_virtual3DTours:
            continue
        for tour in multimedia_virtual3DTours:
            _normalized = json_normalize(tour)
            if 'id' in _normalized.columns:
                _normalized = _normalized.rename(columns={'id': 'multimediaId'})
            _normalized['propertyCode'] = row['propertyCode']
            virtual3DTours = pd.concat([virtual3DTours, _normalized], ignore_index=True)
    df.drop(columns=['multimedia_virtual3DTours'], inplace=True)

    df = pd.read_pickle('data.pkl')
    agencies = pd.DataFrame()
    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing agencies"):
        if row['contactInfo_userType'] != 'professional':
            continue
        agencies = pd.concat([agencies, pd.DataFrame([{
            'commercialName': row['contactInfo_commercialName'],
            'micrositeShortName': row['contactInfo_micrositeShortName'],
            'logo': row['contactInfo_agencyLogo'],
        }])], ignore_index=True)

    df.drop(columns=['contactInfo_agencyLogo', 'contactInfo_micrositeShortName'], inplace=True)
    agencies = agencies.drop_duplicates(subset=['micrositeShortName'])
    agencies = agencies.sort_values(by='commercialName', ascending=True, ignore_index=True)
    df = df.rename(columns={'contactInfo_commercialName': 'agencyName'})
    return {
        'properties': df,
        'location': location,
        'videos': videos,
        'images': images,
        'virtual3DTours': virtual3DTours,
        'agencies': agencies
    }
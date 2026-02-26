from fastapi import APIRouter, HTTPException
from models import GoogleAdsConfig, GoogleAdsConfigUpdate
from database import ads_config_collection
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/ads", tags=["ads"])

class ExtendedAdsConfig(BaseModel):
    enabled: bool = False
    headerAdCode: Optional[str] = None
    sidebarAdCode: Optional[str] = None
    betweenSnippetsAdCode: Optional[str] = None
    footerAdCode: Optional[str] = None
    googleAnalyticsId: Optional[str] = None
    googleTagManagerId: Optional[str] = None
    googleSearchConsoleVerification: Optional[str] = None
    bingVerification: Optional[str] = None
    facebookPixelId: Optional[str] = None
    customHeadCode: Optional[str] = None

@router.get("/config")
async def get_ads_config():
    """Get Google Ads and SEO configuration"""
    config = await ads_config_collection.find_one({})
    
    if not config:
        # Create default config if none exists
        default_config = {
            "enabled": False,
            "headerAdCode": None,
            "sidebarAdCode": None,
            "betweenSnippetsAdCode": None,
            "footerAdCode": None,
            "googleAnalyticsId": None,
            "googleTagManagerId": None,
            "googleSearchConsoleVerification": None,
            "bingVerification": None,
            "facebookPixelId": None,
            "customHeadCode": None
        }
        await ads_config_collection.insert_one(default_config)
        return default_config
    
    # Remove MongoDB _id from response
    config.pop('_id', None)
    return config

@router.post("/config")
async def update_ads_config(config: ExtendedAdsConfig):
    """Update Google Ads and SEO configuration"""
    existing_config = await ads_config_collection.find_one({})
    
    config_dict = config.dict()
    config_dict['updatedAt'] = datetime.utcnow()
    
    if existing_config:
        # Update existing config
        await ads_config_collection.update_one(
            {},
            {'$set': config_dict}
        )
    else:
        # Create new config
        await ads_config_collection.insert_one(config_dict)
    
    return {"message": "Configuration updated successfully"}
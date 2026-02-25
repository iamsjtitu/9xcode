from fastapi import APIRouter, HTTPException
from models import GoogleAdsConfig, GoogleAdsConfigUpdate
from database import ads_config_collection
from datetime import datetime

router = APIRouter(prefix="/ads", tags=["ads"])

@router.get("/config", response_model=GoogleAdsConfig)
async def get_ads_config():
    """Get Google Ads configuration"""
    config = await ads_config_collection.find_one({})
    
    if not config:
        # Create default config if none exists
        default_config = GoogleAdsConfig(
            enabled=False,
            headerAdCode=None,
            sidebarAdCode=None,
            betweenSnippetsAdCode=None,
            footerAdCode=None
        )
        await ads_config_collection.insert_one(default_config.dict())
        return default_config
    
    return GoogleAdsConfig(**config)

@router.put("/config", response_model=GoogleAdsConfig)
async def update_ads_config(config: GoogleAdsConfigUpdate):
    """Update Google Ads configuration"""
    existing_config = await ads_config_collection.find_one({})
    
    config_dict = config.dict()
    config_dict['updatedAt'] = datetime.utcnow()
    
    if existing_config:
        # Update existing config
        await ads_config_collection.update_one(
            {'id': existing_config['id']},
            {'$set': config_dict}
        )
        updated_config = await ads_config_collection.find_one({'id': existing_config['id']})
    else:
        # Create new config
        new_config = GoogleAdsConfig(**config_dict)
        await ads_config_collection.insert_one(new_config.dict())
        updated_config = new_config.dict()
    
    return GoogleAdsConfig(**updated_config)
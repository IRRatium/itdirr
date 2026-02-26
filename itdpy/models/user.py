from typing import Optional, Union, Dict, Any
from pydantic import Field
from .user_lite import UserLite

class User(UserLite):
    banner: Optional[str] = None
    bio: Optional[str] = None
    pinned_post_id: Optional[str] = Field(None, alias="pinnedPostId")
    wall_access: Optional[str] = Field(None, alias="wallAccess")
    likes_visibility: Optional[str] = Field(None, alias="likesVisibility")
    followers_count: int = Field(0, alias="followersCount")
    following_count: int = Field(0, alias="followingCount")
    posts_count: int = Field(0, alias="postsCount")
    is_followed_by: bool = Field(False, alias="isFollowedBy")
    created_at: Optional[str] = Field(None, alias="createdAt")
    online: bool = False
    last_seen: Optional[Union[str, Dict[str, Any]]] = Field(None, alias="lastSeen")

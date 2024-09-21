from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class ListCommunities:
    """https://join-lemmy.org/api/interfaces/ListCommunities.html"""

    type_: Optional[str] = None
    sort: Optional[str] = None
    show_nsfw: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            type_=data["type_"] if "type_" in data else None,
            sort=data["sort"] if "sort" in data else None,
            show_nsfw=data["show_nsfw"] if "show_nsfw" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None
        )


@dataclass
class RegistrationApplication:
    """https://join-lemmy.org/api/interfaces/RegistrationApplication.html"""

    id: int = None
    local_user_id: int = None
    answer: str = None
    admin_id: Optional[int] = None
    deny_reason: Optional[str] = None
    published: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            local_user_id=data["local_user_id"],
            answer=data["answer"],
            admin_id=data["admin_id"] if "admin_id" in data else None,
            deny_reason=data["deny_reason"] if "deny_reason" in data else None,
            published=data["published"]
        )


@dataclass
class AdminPurgeComment:
    """https://join-lemmy.org/api/interfaces/AdminPurgeComment.html"""

    id: int = None
    admin_person_id: int = None
    post_id: int = None
    reason: Optional[str] = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            admin_person_id=data["admin_person_id"],
            post_id=data["post_id"],
            reason=data["reason"] if "reason" in data else None,
            when_=data["when_"]
        )


@dataclass
class CreateSite:
    """https://join-lemmy.org/api/interfaces/CreateSite.html"""

    name: str = None
    sidebar: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    enable_downvotes: Optional[bool] = None
    enable_nsfw: Optional[bool] = None
    community_creation_admin_only: Optional[bool] = None
    require_email_verification: Optional[bool] = None
    application_question: Optional[str] = None
    private_instance: Optional[bool] = None
    default_theme: Optional[str] = None
    default_post_listing_type: Optional[str] = None
    default_sort_type: Optional[str] = None
    legal_information: Optional[str] = None
    application_email_admins: Optional[bool] = None
    hide_modlog_mod_names: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    slur_filter_regex: Optional[str] = None
    actor_name_max_length: Optional[int] = None
    rate_limit_message: Optional[int] = None
    rate_limit_message_per_second: Optional[int] = None
    rate_limit_post: Optional[int] = None
    rate_limit_post_per_second: Optional[int] = None
    rate_limit_register: Optional[int] = None
    rate_limit_register_per_second: Optional[int] = None
    rate_limit_image: Optional[int] = None
    rate_limit_image_per_second: Optional[int] = None
    rate_limit_comment: Optional[int] = None
    rate_limit_comment_per_second: Optional[int] = None
    rate_limit_search: Optional[int] = None
    rate_limit_search_per_second: Optional[int] = None
    federation_enabled: Optional[bool] = None
    federation_debug: Optional[bool] = None
    captcha_enabled: Optional[bool] = None
    captcha_difficulty: Optional[str] = None
    allowed_instances: Optional[list[str]] = None
    blocked_instances: Optional[list[str]] = None
    taglines: Optional[list[str]] = None
    registration_mode: Optional[str] = None
    content_warning: Optional[str] = None
    default_post_listing_mode: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            name=data["name"],
            sidebar=data["sidebar"] if "sidebar" in data else None,
            description=data["description"] if "description" in data else None,
            icon=data["icon"] if "icon" in data else None,
            banner=data["banner"] if "banner" in data else None,
            enable_downvotes=data["enable_downvotes"] if "enable_downvotes" in data else None,
            enable_nsfw=data["enable_nsfw"] if "enable_nsfw" in data else None,
            community_creation_admin_only=data["community_creation_admin_only"] if "community_creation_admin_only" in data else None,
            require_email_verification=data["require_email_verification"] if "require_email_verification" in data else None,
            application_question=data["application_question"] if "application_question" in data else None,
            private_instance=data["private_instance"] if "private_instance" in data else None,
            default_theme=data["default_theme"] if "default_theme" in data else None,
            default_post_listing_type=data["default_post_listing_type"] if "default_post_listing_type" in data else None,
            default_sort_type=data["default_sort_type"] if "default_sort_type" in data else None,
            legal_information=data["legal_information"] if "legal_information" in data else None,
            application_email_admins=data["application_email_admins"] if "application_email_admins" in data else None,
            hide_modlog_mod_names=data["hide_modlog_mod_names"] if "hide_modlog_mod_names" in data else None,
            discussion_languages=[e0 for e0 in data["discussion_languages"]] if "discussion_languages" in data else None,
            slur_filter_regex=data["slur_filter_regex"] if "slur_filter_regex" in data else None,
            actor_name_max_length=data["actor_name_max_length"] if "actor_name_max_length" in data else None,
            rate_limit_message=data["rate_limit_message"] if "rate_limit_message" in data else None,
            rate_limit_message_per_second=data["rate_limit_message_per_second"] if "rate_limit_message_per_second" in data else None,
            rate_limit_post=data["rate_limit_post"] if "rate_limit_post" in data else None,
            rate_limit_post_per_second=data["rate_limit_post_per_second"] if "rate_limit_post_per_second" in data else None,
            rate_limit_register=data["rate_limit_register"] if "rate_limit_register" in data else None,
            rate_limit_register_per_second=data["rate_limit_register_per_second"] if "rate_limit_register_per_second" in data else None,
            rate_limit_image=data["rate_limit_image"] if "rate_limit_image" in data else None,
            rate_limit_image_per_second=data["rate_limit_image_per_second"] if "rate_limit_image_per_second" in data else None,
            rate_limit_comment=data["rate_limit_comment"] if "rate_limit_comment" in data else None,
            rate_limit_comment_per_second=data["rate_limit_comment_per_second"] if "rate_limit_comment_per_second" in data else None,
            rate_limit_search=data["rate_limit_search"] if "rate_limit_search" in data else None,
            rate_limit_search_per_second=data["rate_limit_search_per_second"] if "rate_limit_search_per_second" in data else None,
            federation_enabled=data["federation_enabled"] if "federation_enabled" in data else None,
            federation_debug=data["federation_debug"] if "federation_debug" in data else None,
            captcha_enabled=data["captcha_enabled"] if "captcha_enabled" in data else None,
            captcha_difficulty=data["captcha_difficulty"] if "captcha_difficulty" in data else None,
            allowed_instances=[e0 for e0 in data["allowed_instances"]] if "allowed_instances" in data else None,
            blocked_instances=[e0 for e0 in data["blocked_instances"]] if "blocked_instances" in data else None,
            taglines=[e0 for e0 in data["taglines"]] if "taglines" in data else None,
            registration_mode=data["registration_mode"] if "registration_mode" in data else None,
            content_warning=data["content_warning"] if "content_warning" in data else None,
            default_post_listing_mode=data["default_post_listing_mode"] if "default_post_listing_mode" in data else None
        )


@dataclass
class DeleteComment:
    """https://join-lemmy.org/api/interfaces/DeleteComment.html"""

    comment_id: int = None
    deleted: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            deleted=data["deleted"]
        )


@dataclass
class CreateCommunity:
    """https://join-lemmy.org/api/interfaces/CreateCommunity.html"""

    name: str = None
    title: str = None
    description: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    nsfw: Optional[bool] = None
    posting_restricted_to_mods: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    visibility: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            name=data["name"],
            title=data["title"],
            description=data["description"] if "description" in data else None,
            icon=data["icon"] if "icon" in data else None,
            banner=data["banner"] if "banner" in data else None,
            nsfw=data["nsfw"] if "nsfw" in data else None,
            posting_restricted_to_mods=data["posting_restricted_to_mods"] if "posting_restricted_to_mods" in data else None,
            discussion_languages=[e0 for e0 in data["discussion_languages"]] if "discussion_languages" in data else None,
            visibility=data["visibility"] if "visibility" in data else None
        )


@dataclass
class AdminPurgeCommunity:
    """https://join-lemmy.org/api/interfaces/AdminPurgeCommunity.html"""

    id: int = None
    admin_person_id: int = None
    reason: Optional[str] = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            admin_person_id=data["admin_person_id"],
            reason=data["reason"] if "reason" in data else None,
            when_=data["when_"]
        )


@dataclass
class ModRemoveCommunity:
    """https://join-lemmy.org/api/interfaces/ModRemoveCommunity.html"""

    id: int = None
    mod_person_id: int = None
    community_id: int = None
    reason: Optional[str] = None
    removed: bool = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            community_id=data["community_id"],
            reason=data["reason"] if "reason" in data else None,
            removed=data["removed"],
            when_=data["when_"]
        )


@dataclass
class LocalSiteUrlBlocklist:
    """https://join-lemmy.org/api/interfaces/LocalSiteUrlBlocklist.html"""

    id: int = None
    url: str = None
    published: str = None
    updated: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            url=data["url"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None
        )


@dataclass
class PostReport:
    """https://join-lemmy.org/api/interfaces/PostReport.html"""

    id: int = None
    creator_id: int = None
    post_id: int = None
    original_post_name: str = None
    original_post_url: Optional[str] = None
    original_post_body: Optional[str] = None
    reason: str = None
    resolved: bool = None
    resolver_id: Optional[int] = None
    published: str = None
    updated: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            creator_id=data["creator_id"],
            post_id=data["post_id"],
            original_post_name=data["original_post_name"],
            original_post_url=data["original_post_url"] if "original_post_url" in data else None,
            original_post_body=data["original_post_body"] if "original_post_body" in data else None,
            reason=data["reason"],
            resolved=data["resolved"],
            resolver_id=data["resolver_id"] if "resolver_id" in data else None,
            published=data["published"],
            updated=data["updated"] if "updated" in data else None
        )


@dataclass
class CommentAggregates:
    """https://join-lemmy.org/api/interfaces/CommentAggregates.html"""

    comment_id: int = None
    score: int = None
    upvotes: int = None
    downvotes: int = None
    published: str = None
    child_count: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            score=data["score"],
            upvotes=data["upvotes"],
            downvotes=data["downvotes"],
            published=data["published"],
            child_count=data["child_count"]
        )


@dataclass
class FeaturePost:
    """https://join-lemmy.org/api/interfaces/FeaturePost.html"""

    post_id: int = None
    featured: bool = None
    feature_type: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            featured=data["featured"],
            feature_type=data["feature_type"]
        )


@dataclass
class GetSiteMetadata:
    """https://join-lemmy.org/api/interfaces/GetSiteMetadata.html"""

    url: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            url=data["url"]
        )


@dataclass
class ModLockPost:
    """https://join-lemmy.org/api/interfaces/ModLockPost.html"""

    id: int = None
    mod_person_id: int = None
    post_id: int = None
    locked: bool = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            post_id=data["post_id"],
            locked=data["locked"],
            when_=data["when_"]
        )


@dataclass
class ResolveCommentReport:
    """https://join-lemmy.org/api/interfaces/ResolveCommentReport.html"""

    report_id: int = None
    resolved: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            report_id=data["report_id"],
            resolved=data["resolved"]
        )


@dataclass
class DeleteCommunity:
    """https://join-lemmy.org/api/interfaces/DeleteCommunity.html"""

    community_id: int = None
    deleted: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            deleted=data["deleted"]
        )


@dataclass
class GetPersonMentions:
    """https://join-lemmy.org/api/interfaces/GetPersonMentions.html"""

    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    unread_only: Optional[bool] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            sort=data["sort"] if "sort" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            unread_only=data["unread_only"] if "unread_only" in data else None
        )


@dataclass
class ModHideCommunity:
    """https://join-lemmy.org/api/interfaces/ModHideCommunity.html"""

    id: int = None
    community_id: int = None
    mod_person_id: int = None
    when_: str = None
    reason: Optional[str] = None
    hidden: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            community_id=data["community_id"],
            mod_person_id=data["mod_person_id"],
            when_=data["when_"],
            reason=data["reason"] if "reason" in data else None,
            hidden=data["hidden"]
        )


@dataclass
class HideCommunity:
    """https://join-lemmy.org/api/interfaces/HideCommunity.html"""

    community_id: int = None
    hidden: bool = None
    reason: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            hidden=data["hidden"],
            reason=data["reason"] if "reason" in data else None
        )


@dataclass
class RemoveCommunity:
    """https://join-lemmy.org/api/interfaces/RemoveCommunity.html"""

    community_id: int = None
    removed: bool = None
    reason: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            removed=data["removed"],
            reason=data["reason"] if "reason" in data else None
        )


@dataclass
class EditComment:
    """https://join-lemmy.org/api/interfaces/EditComment.html"""

    comment_id: int = None
    content: Optional[str] = None
    language_id: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            content=data["content"] if "content" in data else None,
            language_id=data["language_id"] if "language_id" in data else None
        )


@dataclass
class EditCustomEmoji:
    """https://join-lemmy.org/api/interfaces/EditCustomEmoji.html"""

    id: int = None
    category: str = None
    image_url: str = None
    alt_text: str = None
    keywords: list[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            category=data["category"],
            image_url=data["image_url"],
            alt_text=data["alt_text"],
            keywords=[e0 for e0 in data["keywords"]]
        )


@dataclass
class PersonMention:
    """https://join-lemmy.org/api/interfaces/PersonMention.html"""

    id: int = None
    recipient_id: int = None
    comment_id: int = None
    read: bool = None
    published: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            recipient_id=data["recipient_id"],
            comment_id=data["comment_id"],
            read=data["read"],
            published=data["published"]
        )


@dataclass
class HidePost:
    """https://join-lemmy.org/api/interfaces/HidePost.html"""

    post_ids: list[int] = None
    hide: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_ids=[e0 for e0 in data["post_ids"]],
            hide=data["hide"]
        )


@dataclass
class CreatePrivateMessageReport:
    """https://join-lemmy.org/api/interfaces/CreatePrivateMessageReport.html"""

    private_message_id: int = None
    reason: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            private_message_id=data["private_message_id"],
            reason=data["reason"]
        )


@dataclass
class ReadableFederationState:
    """https://join-lemmy.org/api/interfaces/ReadableFederationState.html"""

    instance_id: int = None
    last_successful_id: Optional[int] = None
    last_successful_published_time: Optional[str] = None
    fail_count: int = None
    last_retry: Optional[str] = None
    next_retry: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            instance_id=data["instance_id"],
            last_successful_id=data["last_successful_id"] if "last_successful_id" in data else None,
            last_successful_published_time=data["last_successful_published_time"] if "last_successful_published_time" in data else None,
            fail_count=data["fail_count"],
            last_retry=data["last_retry"] if "last_retry" in data else None,
            next_retry=data["next_retry"] if "next_retry" in data else None
        )


@dataclass
class Login:
    """https://join-lemmy.org/api/interfaces/Login.html"""

    username_or_email: str = None
    password: str = None
    totp_2fa_token: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            username_or_email=data["username_or_email"],
            password=data["password"],
            totp_2fa_token=data["totp_2fa_token"] if "totp_2fa_token" in data else None
        )


@dataclass
class BlockInstance:
    """https://join-lemmy.org/api/interfaces/BlockInstance.html"""

    instance_id: int = None
    block: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            instance_id=data["instance_id"],
            block=data["block"]
        )


@dataclass
class LoginToken:
    """https://join-lemmy.org/api/interfaces/LoginToken.html"""

    user_id: int = None
    published: str = None
    ip: Optional[str] = None
    user_agent: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            user_id=data["user_id"],
            published=data["published"],
            ip=data["ip"] if "ip" in data else None,
            user_agent=data["user_agent"] if "user_agent" in data else None
        )


@dataclass
class PasswordChangeAfterReset:
    """https://join-lemmy.org/api/interfaces/PasswordChangeAfterReset.html"""

    token: str = None
    password: str = None
    password_verify: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            token=data["token"],
            password=data["password"],
            password_verify=data["password_verify"]
        )


@dataclass
class LocalUser:
    """https://join-lemmy.org/api/interfaces/LocalUser.html"""

    id: int = None
    person_id: int = None
    email: Optional[str] = None
    show_nsfw: bool = None
    theme: str = None
    default_sort_type: str = None
    default_listing_type: str = None
    interface_language: str = None
    show_avatars: bool = None
    send_notifications_to_email: bool = None
    show_scores: bool = None
    show_bot_accounts: bool = None
    show_read_posts: bool = None
    email_verified: bool = None
    accepted_application: bool = None
    open_links_in_new_tab: bool = None
    blur_nsfw: bool = None
    auto_expand: bool = None
    infinite_scroll_enabled: bool = None
    admin: bool = None
    post_listing_mode: str = None
    totp_2fa_enabled: bool = None
    enable_keyboard_navigation: bool = None
    enable_animated_images: bool = None
    collapse_bot_comments: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            person_id=data["person_id"],
            email=data["email"] if "email" in data else None,
            show_nsfw=data["show_nsfw"],
            theme=data["theme"],
            default_sort_type=data["default_sort_type"],
            default_listing_type=data["default_listing_type"],
            interface_language=data["interface_language"],
            show_avatars=data["show_avatars"],
            send_notifications_to_email=data["send_notifications_to_email"],
            show_scores=data["show_scores"],
            show_bot_accounts=data["show_bot_accounts"],
            show_read_posts=data["show_read_posts"],
            email_verified=data["email_verified"],
            accepted_application=data["accepted_application"],
            open_links_in_new_tab=data["open_links_in_new_tab"],
            blur_nsfw=data["blur_nsfw"],
            auto_expand=data["auto_expand"],
            infinite_scroll_enabled=data["infinite_scroll_enabled"],
            admin=data["admin"],
            post_listing_mode=data["post_listing_mode"],
            totp_2fa_enabled=data["totp_2fa_enabled"],
            enable_keyboard_navigation=data["enable_keyboard_navigation"],
            enable_animated_images=data["enable_animated_images"],
            collapse_bot_comments=data["collapse_bot_comments"]
        )


@dataclass
class PersonAggregates:
    """https://join-lemmy.org/api/interfaces/PersonAggregates.html"""

    person_id: int = None
    post_count: int = None
    comment_count: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person_id=data["person_id"],
            post_count=data["post_count"],
            comment_count=data["comment_count"]
        )


@dataclass
class MarkCommentReplyAsRead:
    """https://join-lemmy.org/api/interfaces/MarkCommentReplyAsRead.html"""

    comment_reply_id: int = None
    read: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_reply_id=data["comment_reply_id"],
            read=data["read"]
        )


@dataclass
class Search:
    """https://join-lemmy.org/api/interfaces/Search.html"""

    q: str = None
    community_id: Optional[int] = None
    community_name: Optional[str] = None
    creator_id: Optional[int] = None
    type_: Optional[str] = None
    sort: Optional[str] = None
    listing_type: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            q=data["q"],
            community_id=data["community_id"] if "community_id" in data else None,
            community_name=data["community_name"] if "community_name" in data else None,
            creator_id=data["creator_id"] if "creator_id" in data else None,
            type_=data["type_"] if "type_" in data else None,
            sort=data["sort"] if "sort" in data else None,
            listing_type=data["listing_type"] if "listing_type" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None
        )


@dataclass
class LocalUserVoteDisplayMode:
    """https://join-lemmy.org/api/interfaces/LocalUserVoteDisplayMode.html"""

    local_user_id: int = None
    score: bool = None
    upvotes: bool = None
    downvotes: bool = None
    upvote_percentage: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            local_user_id=data["local_user_id"],
            score=data["score"],
            upvotes=data["upvotes"],
            downvotes=data["downvotes"],
            upvote_percentage=data["upvote_percentage"]
        )


@dataclass
class LockPost:
    """https://join-lemmy.org/api/interfaces/LockPost.html"""

    post_id: int = None
    locked: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            locked=data["locked"]
        )


@dataclass
class ChangePassword:
    """https://join-lemmy.org/api/interfaces/ChangePassword.html"""

    new_password: str = None
    new_password_verify: str = None
    old_password: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            new_password=data["new_password"],
            new_password_verify=data["new_password_verify"],
            old_password=data["old_password"]
        )


@dataclass
class ResolveObject:
    """https://join-lemmy.org/api/interfaces/ResolveObject.html"""

    q: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            q=data["q"]
        )


@dataclass
class VerifyEmail:
    """https://join-lemmy.org/api/interfaces/VerifyEmail.html"""

    token: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            token=data["token"]
        )


@dataclass
class ModAddCommunity:
    """https://join-lemmy.org/api/interfaces/ModAddCommunity.html"""

    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    community_id: int = None
    removed: bool = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            other_person_id=data["other_person_id"],
            community_id=data["community_id"],
            removed=data["removed"],
            when_=data["when_"]
        )


@dataclass
class BlockPerson:
    """https://join-lemmy.org/api/interfaces/BlockPerson.html"""

    person_id: int = None
    block: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person_id=data["person_id"],
            block=data["block"]
        )


@dataclass
class ListPrivateMessageReports:
    """https://join-lemmy.org/api/interfaces/ListPrivateMessageReports.html"""

    page: Optional[int] = None
    limit: Optional[int] = None
    unresolved_only: Optional[bool] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            unresolved_only=data["unresolved_only"] if "unresolved_only" in data else None
        )


@dataclass
class SiteAggregates:
    """https://join-lemmy.org/api/interfaces/SiteAggregates.html"""

    site_id: int = None
    users: int = None
    posts: int = None
    comments: int = None
    communities: int = None
    users_active_day: int = None
    users_active_week: int = None
    users_active_month: int = None
    users_active_half_year: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            site_id=data["site_id"],
            users=data["users"],
            posts=data["posts"],
            comments=data["comments"],
            communities=data["communities"],
            users_active_day=data["users_active_day"],
            users_active_week=data["users_active_week"],
            users_active_month=data["users_active_month"],
            users_active_half_year=data["users_active_half_year"]
        )


@dataclass
class CreatePostReport:
    """https://join-lemmy.org/api/interfaces/CreatePostReport.html"""

    post_id: int = None
    reason: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            reason=data["reason"]
        )


@dataclass
class CustomEmoji:
    """https://join-lemmy.org/api/interfaces/CustomEmoji.html"""

    id: int = None
    local_site_id: int = None
    shortcode: str = None
    image_url: str = None
    alt_text: str = None
    category: str = None
    published: str = None
    updated: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            local_site_id=data["local_site_id"],
            shortcode=data["shortcode"],
            image_url=data["image_url"],
            alt_text=data["alt_text"],
            category=data["category"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None
        )


@dataclass
class PurgePost:
    """https://join-lemmy.org/api/interfaces/PurgePost.html"""

    post_id: int = None
    reason: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            reason=data["reason"] if "reason" in data else None
        )


@dataclass
class PostAggregates:
    """https://join-lemmy.org/api/interfaces/PostAggregates.html"""

    post_id: int = None
    comments: int = None
    score: int = None
    upvotes: int = None
    downvotes: int = None
    published: str = None
    newest_comment_time: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            comments=data["comments"],
            score=data["score"],
            upvotes=data["upvotes"],
            downvotes=data["downvotes"],
            published=data["published"],
            newest_comment_time=data["newest_comment_time"]
        )


@dataclass
class Language:
    """https://join-lemmy.org/api/interfaces/Language.html"""

    id: int = None
    code: str = None
    name: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            code=data["code"],
            name=data["name"]
        )


@dataclass
class GetReportCount:
    """https://join-lemmy.org/api/interfaces/GetReportCount.html"""

    community_id: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"] if "community_id" in data else None
        )


@dataclass
class DeletePrivateMessage:
    """https://join-lemmy.org/api/interfaces/DeletePrivateMessage.html"""

    private_message_id: int = None
    deleted: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            private_message_id=data["private_message_id"],
            deleted=data["deleted"]
        )


@dataclass
class Community:
    """https://join-lemmy.org/api/interfaces/Community.html"""

    id: int = None
    name: str = None
    title: str = None
    description: Optional[str] = None
    removed: bool = None
    published: str = None
    updated: Optional[str] = None
    deleted: bool = None
    nsfw: bool = None
    actor_id: str = None
    local: bool = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    hidden: bool = None
    posting_restricted_to_mods: bool = None
    instance_id: int = None
    visibility: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            name=data["name"],
            title=data["title"],
            description=data["description"] if "description" in data else None,
            removed=data["removed"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            deleted=data["deleted"],
            nsfw=data["nsfw"],
            actor_id=data["actor_id"],
            local=data["local"],
            icon=data["icon"] if "icon" in data else None,
            banner=data["banner"] if "banner" in data else None,
            hidden=data["hidden"],
            posting_restricted_to_mods=data["posting_restricted_to_mods"],
            instance_id=data["instance_id"],
            visibility=data["visibility"]
        )


@dataclass
class ListPostReports:
    """https://join-lemmy.org/api/interfaces/ListPostReports.html"""

    page: Optional[int] = None
    limit: Optional[int] = None
    unresolved_only: Optional[bool] = None
    community_id: Optional[int] = None
    post_id: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            unresolved_only=data["unresolved_only"] if "unresolved_only" in data else None,
            community_id=data["community_id"] if "community_id" in data else None,
            post_id=data["post_id"] if "post_id" in data else None
        )


@dataclass
class ModFeaturePost:
    """https://join-lemmy.org/api/interfaces/ModFeaturePost.html"""

    id: int = None
    mod_person_id: int = None
    post_id: int = None
    featured: bool = None
    when_: str = None
    is_featured_community: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            post_id=data["post_id"],
            featured=data["featured"],
            when_=data["when_"],
            is_featured_community=data["is_featured_community"]
        )


@dataclass
class GetPersonDetails:
    """https://join-lemmy.org/api/interfaces/GetPersonDetails.html"""

    person_id: Optional[int] = None
    username: Optional[str] = None
    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    community_id: Optional[int] = None
    saved_only: Optional[bool] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person_id=data["person_id"] if "person_id" in data else None,
            username=data["username"] if "username" in data else None,
            sort=data["sort"] if "sort" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            community_id=data["community_id"] if "community_id" in data else None,
            saved_only=data["saved_only"] if "saved_only" in data else None
        )


@dataclass
class AddModToCommunity:
    """https://join-lemmy.org/api/interfaces/AddModToCommunity.html"""

    community_id: int = None
    person_id: int = None
    added: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            person_id=data["person_id"],
            added=data["added"]
        )


@dataclass
class Site:
    """https://join-lemmy.org/api/interfaces/Site.html"""

    id: int = None
    name: str = None
    sidebar: Optional[str] = None
    published: str = None
    updated: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    description: Optional[str] = None
    actor_id: str = None
    last_refreshed_at: str = None
    inbox_url: str = None
    public_key: str = None
    instance_id: int = None
    content_warning: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            name=data["name"],
            sidebar=data["sidebar"] if "sidebar" in data else None,
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            icon=data["icon"] if "icon" in data else None,
            banner=data["banner"] if "banner" in data else None,
            description=data["description"] if "description" in data else None,
            actor_id=data["actor_id"],
            last_refreshed_at=data["last_refreshed_at"],
            inbox_url=data["inbox_url"],
            public_key=data["public_key"],
            instance_id=data["instance_id"],
            content_warning=data["content_warning"] if "content_warning" in data else None
        )


@dataclass
class ApproveRegistrationApplication:
    """https://join-lemmy.org/api/interfaces/ApproveRegistrationApplication.html"""

    id: int = None
    approve: bool = None
    deny_reason: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            approve=data["approve"],
            deny_reason=data["deny_reason"] if "deny_reason" in data else None
        )


@dataclass
class EditPost:
    """https://join-lemmy.org/api/interfaces/EditPost.html"""

    post_id: int = None
    name: Optional[str] = None
    url: Optional[str] = None
    body: Optional[str] = None
    alt_text: Optional[str] = None
    nsfw: Optional[bool] = None
    language_id: Optional[int] = None
    custom_thumbnail: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            name=data["name"] if "name" in data else None,
            url=data["url"] if "url" in data else None,
            body=data["body"] if "body" in data else None,
            alt_text=data["alt_text"] if "alt_text" in data else None,
            nsfw=data["nsfw"] if "nsfw" in data else None,
            language_id=data["language_id"] if "language_id" in data else None,
            custom_thumbnail=data["custom_thumbnail"] if "custom_thumbnail" in data else None
        )


@dataclass
class GetPost:
    """https://join-lemmy.org/api/interfaces/GetPost.html"""

    id: Optional[int] = None
    comment_id: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"] if "id" in data else None,
            comment_id=data["comment_id"] if "comment_id" in data else None
        )


@dataclass
class FollowCommunity:
    """https://join-lemmy.org/api/interfaces/FollowCommunity.html"""

    community_id: int = None
    follow: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            follow=data["follow"]
        )


@dataclass
class GetPrivateMessages:
    """https://join-lemmy.org/api/interfaces/GetPrivateMessages.html"""

    unread_only: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    creator_id: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            unread_only=data["unread_only"] if "unread_only" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            creator_id=data["creator_id"] if "creator_id" in data else None
        )


@dataclass
class ModBan:
    """https://join-lemmy.org/api/interfaces/ModBan.html"""

    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    reason: Optional[str] = None
    banned: bool = None
    expires: Optional[str] = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            other_person_id=data["other_person_id"],
            reason=data["reason"] if "reason" in data else None,
            banned=data["banned"],
            expires=data["expires"] if "expires" in data else None,
            when_=data["when_"]
        )


@dataclass
class Tagline:
    """https://join-lemmy.org/api/interfaces/Tagline.html"""

    id: int = None
    local_site_id: int = None
    content: str = None
    published: str = None
    updated: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            local_site_id=data["local_site_id"],
            content=data["content"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None
        )


@dataclass
class RemoveComment:
    """https://join-lemmy.org/api/interfaces/RemoveComment.html"""

    comment_id: int = None
    removed: bool = None
    reason: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            removed=data["removed"],
            reason=data["reason"] if "reason" in data else None
        )


@dataclass
class UpdateTotp:
    """https://join-lemmy.org/api/interfaces/UpdateTotp.html"""

    totp_token: str = None
    enabled: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            totp_token=data["totp_token"],
            enabled=data["enabled"]
        )


@dataclass
class MarkPostAsRead:
    """https://join-lemmy.org/api/interfaces/MarkPostAsRead.html"""

    post_ids: list[int] = None
    read: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_ids=[e0 for e0 in data["post_ids"]],
            read=data["read"]
        )


@dataclass
class ResolvePrivateMessageReport:
    """https://join-lemmy.org/api/interfaces/ResolvePrivateMessageReport.html"""

    report_id: int = None
    resolved: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            report_id=data["report_id"],
            resolved=data["resolved"]
        )


@dataclass
class LinkMetadata:
    """https://join-lemmy.org/api/interfaces/LinkMetadata.html"""

    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    embed_video_url: Optional[str] = None
    content_type: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            title=data["title"] if "title" in data else None,
            description=data["description"] if "description" in data else None,
            image=data["image"] if "image" in data else None,
            embed_video_url=data["embed_video_url"] if "embed_video_url" in data else None,
            content_type=data["content_type"] if "content_type" in data else None
        )


@dataclass
class PrivateMessage:
    """https://join-lemmy.org/api/interfaces/PrivateMessage.html"""

    id: int = None
    creator_id: int = None
    recipient_id: int = None
    content: str = None
    deleted: bool = None
    read: bool = None
    published: str = None
    updated: Optional[str] = None
    ap_id: str = None
    local: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            creator_id=data["creator_id"],
            recipient_id=data["recipient_id"],
            content=data["content"],
            deleted=data["deleted"],
            read=data["read"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            ap_id=data["ap_id"],
            local=data["local"]
        )


@dataclass
class DeletePost:
    """https://join-lemmy.org/api/interfaces/DeletePost.html"""

    post_id: int = None
    deleted: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            deleted=data["deleted"]
        )


@dataclass
class PurgeComment:
    """https://join-lemmy.org/api/interfaces/PurgeComment.html"""

    comment_id: int = None
    reason: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            reason=data["reason"] if "reason" in data else None
        )


@dataclass
class CreatePost:
    """https://join-lemmy.org/api/interfaces/CreatePost.html"""

    name: str = None
    community_id: int = None
    url: Optional[str] = None
    body: Optional[str] = None
    alt_text: Optional[str] = None
    honeypot: Optional[str] = None
    nsfw: Optional[bool] = None
    language_id: Optional[int] = None
    custom_thumbnail: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            name=data["name"],
            community_id=data["community_id"],
            url=data["url"] if "url" in data else None,
            body=data["body"] if "body" in data else None,
            alt_text=data["alt_text"] if "alt_text" in data else None,
            honeypot=data["honeypot"] if "honeypot" in data else None,
            nsfw=data["nsfw"] if "nsfw" in data else None,
            language_id=data["language_id"] if "language_id" in data else None,
            custom_thumbnail=data["custom_thumbnail"] if "custom_thumbnail" in data else None
        )


@dataclass
class CreateCustomEmoji:
    """https://join-lemmy.org/api/interfaces/CreateCustomEmoji.html"""

    category: str = None
    shortcode: str = None
    image_url: str = None
    alt_text: str = None
    keywords: list[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            category=data["category"],
            shortcode=data["shortcode"],
            image_url=data["image_url"],
            alt_text=data["alt_text"],
            keywords=[e0 for e0 in data["keywords"]]
        )


@dataclass
class InstanceWithFederationState:
    """https://join-lemmy.org/api/interfaces/InstanceWithFederationState.html"""

    id: int = None
    domain: str = None
    published: str = None
    updated: Optional[str] = None
    software: Optional[str] = None
    version: Optional[str] = None
    federation_state: Optional[ReadableFederationState] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            domain=data["domain"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            software=data["software"] if "software" in data else None,
            version=data["version"] if "version" in data else None,
            federation_state=ReadableFederationState.parse(data["federation_state"]) if "federation_state" in data else None
        )


@dataclass
class CommunityAggregates:
    """https://join-lemmy.org/api/interfaces/CommunityAggregates.html"""

    community_id: int = None
    subscribers: int = None
    posts: int = None
    comments: int = None
    published: str = None
    users_active_day: int = None
    users_active_week: int = None
    users_active_month: int = None
    users_active_half_year: int = None
    subscribers_local: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            subscribers=data["subscribers"],
            posts=data["posts"],
            comments=data["comments"],
            published=data["published"],
            users_active_day=data["users_active_day"],
            users_active_week=data["users_active_week"],
            users_active_month=data["users_active_month"],
            users_active_half_year=data["users_active_half_year"],
            subscribers_local=data["subscribers_local"]
        )


@dataclass
class LocalImage:
    """https://join-lemmy.org/api/interfaces/LocalImage.html"""

    local_user_id: Optional[int] = None
    pictrs_alias: str = None
    pictrs_delete_token: str = None
    published: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            local_user_id=data["local_user_id"] if "local_user_id" in data else None,
            pictrs_alias=data["pictrs_alias"],
            pictrs_delete_token=data["pictrs_delete_token"],
            published=data["published"]
        )


@dataclass
class EditCommunity:
    """https://join-lemmy.org/api/interfaces/EditCommunity.html"""

    community_id: int = None
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    nsfw: Optional[bool] = None
    posting_restricted_to_mods: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    visibility: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            title=data["title"] if "title" in data else None,
            description=data["description"] if "description" in data else None,
            icon=data["icon"] if "icon" in data else None,
            banner=data["banner"] if "banner" in data else None,
            nsfw=data["nsfw"] if "nsfw" in data else None,
            posting_restricted_to_mods=data["posting_restricted_to_mods"] if "posting_restricted_to_mods" in data else None,
            discussion_languages=[e0 for e0 in data["discussion_languages"]] if "discussion_languages" in data else None,
            visibility=data["visibility"] if "visibility" in data else None
        )


@dataclass
class ListPostLikes:
    """https://join-lemmy.org/api/interfaces/ListPostLikes.html"""

    post_id: int = None
    page: Optional[int] = None
    limit: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None
        )


@dataclass
class CommentReply:
    """https://join-lemmy.org/api/interfaces/CommentReply.html"""

    id: int = None
    recipient_id: int = None
    comment_id: int = None
    read: bool = None
    published: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            recipient_id=data["recipient_id"],
            comment_id=data["comment_id"],
            read=data["read"],
            published=data["published"]
        )


@dataclass
class ModRemovePost:
    """https://join-lemmy.org/api/interfaces/ModRemovePost.html"""

    id: int = None
    mod_person_id: int = None
    post_id: int = None
    reason: Optional[str] = None
    removed: bool = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            post_id=data["post_id"],
            reason=data["reason"] if "reason" in data else None,
            removed=data["removed"],
            when_=data["when_"]
        )


@dataclass
class BanFromCommunity:
    """https://join-lemmy.org/api/interfaces/BanFromCommunity.html"""

    community_id: int = None
    person_id: int = None
    ban: bool = None
    remove_data: Optional[bool] = None
    reason: Optional[str] = None
    expires: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            person_id=data["person_id"],
            ban=data["ban"],
            remove_data=data["remove_data"] if "remove_data" in data else None,
            reason=data["reason"] if "reason" in data else None,
            expires=data["expires"] if "expires" in data else None
        )


@dataclass
class CreatePostLike:
    """https://join-lemmy.org/api/interfaces/CreatePostLike.html"""

    post_id: int = None
    score: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            score=data["score"]
        )


@dataclass
class RemovePost:
    """https://join-lemmy.org/api/interfaces/RemovePost.html"""

    post_id: int = None
    removed: bool = None
    reason: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            removed=data["removed"],
            reason=data["reason"] if "reason" in data else None
        )


@dataclass
class EditPrivateMessage:
    """https://join-lemmy.org/api/interfaces/EditPrivateMessage.html"""

    private_message_id: int = None
    content: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            private_message_id=data["private_message_id"],
            content=data["content"]
        )


@dataclass
class ImageDetails:
    """https://join-lemmy.org/api/interfaces/ImageDetails.html"""

    link: str = None
    width: int = None
    height: int = None
    content_type: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            link=data["link"],
            width=data["width"],
            height=data["height"],
            content_type=data["content_type"]
        )


@dataclass
class GetModlog:
    """https://join-lemmy.org/api/interfaces/GetModlog.html"""

    mod_person_id: Optional[int] = None
    community_id: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    type_: Optional[str] = None
    other_person_id: Optional[int] = None
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_person_id=data["mod_person_id"] if "mod_person_id" in data else None,
            community_id=data["community_id"] if "community_id" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            type_=data["type_"] if "type_" in data else None,
            other_person_id=data["other_person_id"] if "other_person_id" in data else None,
            post_id=data["post_id"] if "post_id" in data else None,
            comment_id=data["comment_id"] if "comment_id" in data else None
        )


@dataclass
class SaveUserSettings:
    """https://join-lemmy.org/api/interfaces/SaveUserSettings.html"""

    show_nsfw: Optional[bool] = None
    blur_nsfw: Optional[bool] = None
    auto_expand: Optional[bool] = None
    theme: Optional[str] = None
    default_sort_type: Optional[str] = None
    default_listing_type: Optional[str] = None
    interface_language: Optional[str] = None
    avatar: Optional[str] = None
    banner: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    matrix_user_id: Optional[str] = None
    show_avatars: Optional[bool] = None
    send_notifications_to_email: Optional[bool] = None
    bot_account: Optional[bool] = None
    show_bot_accounts: Optional[bool] = None
    show_read_posts: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    open_links_in_new_tab: Optional[bool] = None
    infinite_scroll_enabled: Optional[bool] = None
    post_listing_mode: Optional[str] = None
    enable_keyboard_navigation: Optional[bool] = None
    enable_animated_images: Optional[bool] = None
    collapse_bot_comments: Optional[bool] = None
    show_scores: Optional[bool] = None
    show_upvotes: Optional[bool] = None
    show_downvotes: Optional[bool] = None
    show_upvote_percentage: Optional[bool] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            show_nsfw=data["show_nsfw"] if "show_nsfw" in data else None,
            blur_nsfw=data["blur_nsfw"] if "blur_nsfw" in data else None,
            auto_expand=data["auto_expand"] if "auto_expand" in data else None,
            theme=data["theme"] if "theme" in data else None,
            default_sort_type=data["default_sort_type"] if "default_sort_type" in data else None,
            default_listing_type=data["default_listing_type"] if "default_listing_type" in data else None,
            interface_language=data["interface_language"] if "interface_language" in data else None,
            avatar=data["avatar"] if "avatar" in data else None,
            banner=data["banner"] if "banner" in data else None,
            display_name=data["display_name"] if "display_name" in data else None,
            email=data["email"] if "email" in data else None,
            bio=data["bio"] if "bio" in data else None,
            matrix_user_id=data["matrix_user_id"] if "matrix_user_id" in data else None,
            show_avatars=data["show_avatars"] if "show_avatars" in data else None,
            send_notifications_to_email=data["send_notifications_to_email"] if "send_notifications_to_email" in data else None,
            bot_account=data["bot_account"] if "bot_account" in data else None,
            show_bot_accounts=data["show_bot_accounts"] if "show_bot_accounts" in data else None,
            show_read_posts=data["show_read_posts"] if "show_read_posts" in data else None,
            discussion_languages=[e0 for e0 in data["discussion_languages"]] if "discussion_languages" in data else None,
            open_links_in_new_tab=data["open_links_in_new_tab"] if "open_links_in_new_tab" in data else None,
            infinite_scroll_enabled=data["infinite_scroll_enabled"] if "infinite_scroll_enabled" in data else None,
            post_listing_mode=data["post_listing_mode"] if "post_listing_mode" in data else None,
            enable_keyboard_navigation=data["enable_keyboard_navigation"] if "enable_keyboard_navigation" in data else None,
            enable_animated_images=data["enable_animated_images"] if "enable_animated_images" in data else None,
            collapse_bot_comments=data["collapse_bot_comments"] if "collapse_bot_comments" in data else None,
            show_scores=data["show_scores"] if "show_scores" in data else None,
            show_upvotes=data["show_upvotes"] if "show_upvotes" in data else None,
            show_downvotes=data["show_downvotes"] if "show_downvotes" in data else None,
            show_upvote_percentage=data["show_upvote_percentage"] if "show_upvote_percentage" in data else None
        )


@dataclass
class CreatePrivateMessage:
    """https://join-lemmy.org/api/interfaces/CreatePrivateMessage.html"""

    content: str = None
    recipient_id: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            content=data["content"],
            recipient_id=data["recipient_id"]
        )


@dataclass
class LocalSiteRateLimit:
    """https://join-lemmy.org/api/interfaces/LocalSiteRateLimit.html"""

    local_site_id: int = None
    message: int = None
    message_per_second: int = None
    post: int = None
    post_per_second: int = None
    register: int = None
    register_per_second: int = None
    image: int = None
    image_per_second: int = None
    comment: int = None
    comment_per_second: int = None
    search: int = None
    search_per_second: int = None
    published: str = None
    updated: Optional[str] = None
    import_user_settings: int = None
    import_user_settings_per_second: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            local_site_id=data["local_site_id"],
            message=data["message"],
            message_per_second=data["message_per_second"],
            post=data["post"],
            post_per_second=data["post_per_second"],
            register=data["register"],
            register_per_second=data["register_per_second"],
            image=data["image"],
            image_per_second=data["image_per_second"],
            comment=data["comment"],
            comment_per_second=data["comment_per_second"],
            search=data["search"],
            search_per_second=data["search_per_second"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            import_user_settings=data["import_user_settings"],
            import_user_settings_per_second=data["import_user_settings_per_second"]
        )


@dataclass
class ListCommentLikes:
    """https://join-lemmy.org/api/interfaces/ListCommentLikes.html"""

    comment_id: int = None
    page: Optional[int] = None
    limit: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None
        )


@dataclass
class SaveComment:
    """https://join-lemmy.org/api/interfaces/SaveComment.html"""

    comment_id: int = None
    save: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            save=data["save"]
        )


@dataclass
class ListMedia:
    """https://join-lemmy.org/api/interfaces/ListMedia.html"""

    page: Optional[int] = None
    limit: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None
        )


@dataclass
class LocalSite:
    """https://join-lemmy.org/api/interfaces/LocalSite.html"""

    id: int = None
    site_id: int = None
    site_setup: bool = None
    enable_downvotes: bool = None
    enable_nsfw: bool = None
    community_creation_admin_only: bool = None
    require_email_verification: bool = None
    application_question: Optional[str] = None
    private_instance: bool = None
    default_theme: str = None
    default_post_listing_type: str = None
    legal_information: Optional[str] = None
    hide_modlog_mod_names: bool = None
    application_email_admins: bool = None
    slur_filter_regex: Optional[str] = None
    actor_name_max_length: int = None
    federation_enabled: bool = None
    captcha_enabled: bool = None
    captcha_difficulty: str = None
    published: str = None
    updated: Optional[str] = None
    registration_mode: str = None
    reports_email_admins: bool = None
    federation_signed_fetch: bool = None
    default_post_listing_mode: str = None
    default_sort_type: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            site_id=data["site_id"],
            site_setup=data["site_setup"],
            enable_downvotes=data["enable_downvotes"],
            enable_nsfw=data["enable_nsfw"],
            community_creation_admin_only=data["community_creation_admin_only"],
            require_email_verification=data["require_email_verification"],
            application_question=data["application_question"] if "application_question" in data else None,
            private_instance=data["private_instance"],
            default_theme=data["default_theme"],
            default_post_listing_type=data["default_post_listing_type"],
            legal_information=data["legal_information"] if "legal_information" in data else None,
            hide_modlog_mod_names=data["hide_modlog_mod_names"],
            application_email_admins=data["application_email_admins"],
            slur_filter_regex=data["slur_filter_regex"] if "slur_filter_regex" in data else None,
            actor_name_max_length=data["actor_name_max_length"],
            federation_enabled=data["federation_enabled"],
            captcha_enabled=data["captcha_enabled"],
            captcha_difficulty=data["captcha_difficulty"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            registration_mode=data["registration_mode"],
            reports_email_admins=data["reports_email_admins"],
            federation_signed_fetch=data["federation_signed_fetch"],
            default_post_listing_mode=data["default_post_listing_mode"],
            default_sort_type=data["default_sort_type"]
        )


@dataclass
class CustomEmojiKeyword:
    """https://join-lemmy.org/api/interfaces/CustomEmojiKeyword.html"""

    custom_emoji_id: int = None
    keyword: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            custom_emoji_id=data["custom_emoji_id"],
            keyword=data["keyword"]
        )


@dataclass
class ModlogListParams:
    """https://join-lemmy.org/api/interfaces/ModlogListParams.html"""

    community_id: Optional[int] = None
    mod_person_id: Optional[int] = None
    other_person_id: Optional[int] = None
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    hide_modlog_names: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"] if "community_id" in data else None,
            mod_person_id=data["mod_person_id"] if "mod_person_id" in data else None,
            other_person_id=data["other_person_id"] if "other_person_id" in data else None,
            post_id=data["post_id"] if "post_id" in data else None,
            comment_id=data["comment_id"] if "comment_id" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            hide_modlog_names=data["hide_modlog_names"]
        )


@dataclass
class ModRemoveComment:
    """https://join-lemmy.org/api/interfaces/ModRemoveComment.html"""

    id: int = None
    mod_person_id: int = None
    comment_id: int = None
    reason: Optional[str] = None
    removed: bool = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            comment_id=data["comment_id"],
            reason=data["reason"] if "reason" in data else None,
            removed=data["removed"],
            when_=data["when_"]
        )


@dataclass
class GetComments:
    """https://join-lemmy.org/api/interfaces/GetComments.html"""

    type_: Optional[str] = None
    sort: Optional[str] = None
    max_depth: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    community_id: Optional[int] = None
    community_name: Optional[str] = None
    post_id: Optional[int] = None
    parent_id: Optional[int] = None
    saved_only: Optional[bool] = None
    liked_only: Optional[bool] = None
    disliked_only: Optional[bool] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            type_=data["type_"] if "type_" in data else None,
            sort=data["sort"] if "sort" in data else None,
            max_depth=data["max_depth"] if "max_depth" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            community_id=data["community_id"] if "community_id" in data else None,
            community_name=data["community_name"] if "community_name" in data else None,
            post_id=data["post_id"] if "post_id" in data else None,
            parent_id=data["parent_id"] if "parent_id" in data else None,
            saved_only=data["saved_only"] if "saved_only" in data else None,
            liked_only=data["liked_only"] if "liked_only" in data else None,
            disliked_only=data["disliked_only"] if "disliked_only" in data else None
        )


@dataclass
class ModBanFromCommunity:
    """https://join-lemmy.org/api/interfaces/ModBanFromCommunity.html"""

    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    community_id: int = None
    reason: Optional[str] = None
    banned: bool = None
    expires: Optional[str] = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            other_person_id=data["other_person_id"],
            community_id=data["community_id"],
            reason=data["reason"] if "reason" in data else None,
            banned=data["banned"],
            expires=data["expires"] if "expires" in data else None,
            when_=data["when_"]
        )


@dataclass
class MarkPersonMentionAsRead:
    """https://join-lemmy.org/api/interfaces/MarkPersonMentionAsRead.html"""

    person_mention_id: int = None
    read: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person_mention_id=data["person_mention_id"],
            read=data["read"]
        )


@dataclass
class GetCommunity:
    """https://join-lemmy.org/api/interfaces/GetCommunity.html"""

    id: Optional[int] = None
    name: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"] if "id" in data else None,
            name=data["name"] if "name" in data else None
        )


@dataclass
class PrivateMessageReport:
    """https://join-lemmy.org/api/interfaces/PrivateMessageReport.html"""

    id: int = None
    creator_id: int = None
    private_message_id: int = None
    original_pm_text: str = None
    reason: str = None
    resolved: bool = None
    resolver_id: Optional[int] = None
    published: str = None
    updated: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            creator_id=data["creator_id"],
            private_message_id=data["private_message_id"],
            original_pm_text=data["original_pm_text"],
            reason=data["reason"],
            resolved=data["resolved"],
            resolver_id=data["resolver_id"] if "resolver_id" in data else None,
            published=data["published"],
            updated=data["updated"] if "updated" in data else None
        )


@dataclass
class SavePost:
    """https://join-lemmy.org/api/interfaces/SavePost.html"""

    post_id: int = None
    save: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_id=data["post_id"],
            save=data["save"]
        )


@dataclass
class PasswordReset:
    """https://join-lemmy.org/api/interfaces/PasswordReset.html"""

    email: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            email=data["email"]
        )


@dataclass
class CreateCommentReport:
    """https://join-lemmy.org/api/interfaces/CreateCommentReport.html"""

    comment_id: int = None
    reason: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            reason=data["reason"]
        )


@dataclass
class CreateCommentLike:
    """https://join-lemmy.org/api/interfaces/CreateCommentLike.html"""

    comment_id: int = None
    score: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            score=data["score"]
        )


@dataclass
class Register:
    """https://join-lemmy.org/api/interfaces/Register.html"""

    username: str = None
    password: str = None
    password_verify: str = None
    show_nsfw: Optional[bool] = None
    email: Optional[str] = None
    captcha_uuid: Optional[str] = None
    captcha_answer: Optional[str] = None
    honeypot: Optional[str] = None
    answer: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            username=data["username"],
            password=data["password"],
            password_verify=data["password_verify"],
            show_nsfw=data["show_nsfw"] if "show_nsfw" in data else None,
            email=data["email"] if "email" in data else None,
            captcha_uuid=data["captcha_uuid"] if "captcha_uuid" in data else None,
            captcha_answer=data["captcha_answer"] if "captcha_answer" in data else None,
            honeypot=data["honeypot"] if "honeypot" in data else None,
            answer=data["answer"] if "answer" in data else None
        )


@dataclass
class FederatedInstances:
    """https://join-lemmy.org/api/interfaces/FederatedInstances.html"""

    linked: list[InstanceWithFederationState] = None
    allowed: list[InstanceWithFederationState] = None
    blocked: list[InstanceWithFederationState] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            linked=[InstanceWithFederationState.parse(e0) for e0 in data["linked"]],
            allowed=[InstanceWithFederationState.parse(e0) for e0 in data["allowed"]],
            blocked=[InstanceWithFederationState.parse(e0) for e0 in data["blocked"]]
        )


@dataclass
class DeleteAccount:
    """https://join-lemmy.org/api/interfaces/DeleteAccount.html"""

    password: str = None
    delete_content: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            password=data["password"],
            delete_content=data["delete_content"]
        )


@dataclass
class MarkPrivateMessageAsRead:
    """https://join-lemmy.org/api/interfaces/MarkPrivateMessageAsRead.html"""

    private_message_id: int = None
    read: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            private_message_id=data["private_message_id"],
            read=data["read"]
        )


@dataclass
class GetComment:
    """https://join-lemmy.org/api/interfaces/GetComment.html"""

    id: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"]
        )


@dataclass
class PurgeCommunity:
    """https://join-lemmy.org/api/interfaces/PurgeCommunity.html"""

    community_id: int = None
    reason: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            reason=data["reason"] if "reason" in data else None
        )


@dataclass
class AddAdmin:
    """https://join-lemmy.org/api/interfaces/AddAdmin.html"""

    person_id: int = None
    added: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person_id=data["person_id"],
            added=data["added"]
        )


@dataclass
class ModTransferCommunity:
    """https://join-lemmy.org/api/interfaces/ModTransferCommunity.html"""

    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    community_id: int = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            other_person_id=data["other_person_id"],
            community_id=data["community_id"],
            when_=data["when_"]
        )


@dataclass
class Person:
    """https://join-lemmy.org/api/interfaces/Person.html"""

    id: int = None
    name: str = None
    display_name: Optional[str] = None
    avatar: Optional[str] = None
    banned: bool = None
    published: str = None
    updated: Optional[str] = None
    actor_id: str = None
    bio: Optional[str] = None
    local: bool = None
    banner: Optional[str] = None
    deleted: bool = None
    matrix_user_id: Optional[str] = None
    bot_account: bool = None
    ban_expires: Optional[str] = None
    instance_id: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            name=data["name"],
            display_name=data["display_name"] if "display_name" in data else None,
            avatar=data["avatar"] if "avatar" in data else None,
            banned=data["banned"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            actor_id=data["actor_id"],
            bio=data["bio"] if "bio" in data else None,
            local=data["local"],
            banner=data["banner"] if "banner" in data else None,
            deleted=data["deleted"],
            matrix_user_id=data["matrix_user_id"] if "matrix_user_id" in data else None,
            bot_account=data["bot_account"],
            ban_expires=data["ban_expires"] if "ban_expires" in data else None,
            instance_id=data["instance_id"]
        )


@dataclass
class Comment:
    """https://join-lemmy.org/api/interfaces/Comment.html"""

    id: int = None
    creator_id: int = None
    post_id: int = None
    content: str = None
    removed: bool = None
    published: str = None
    updated: Optional[str] = None
    deleted: bool = None
    ap_id: str = None
    local: bool = None
    path: str = None
    distinguished: bool = None
    language_id: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            creator_id=data["creator_id"],
            post_id=data["post_id"],
            content=data["content"],
            removed=data["removed"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            deleted=data["deleted"],
            ap_id=data["ap_id"],
            local=data["local"],
            path=data["path"],
            distinguished=data["distinguished"],
            language_id=data["language_id"]
        )


@dataclass
class OpenGraphData:
    """https://join-lemmy.org/api/interfaces/OpenGraphData.html"""

    title: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    embed_video_url: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            title=data["title"] if "title" in data else None,
            description=data["description"] if "description" in data else None,
            image=data["image"] if "image" in data else None,
            embed_video_url=data["embed_video_url"] if "embed_video_url" in data else None
        )


@dataclass
class PurgePerson:
    """https://join-lemmy.org/api/interfaces/PurgePerson.html"""

    person_id: int = None
    reason: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person_id=data["person_id"],
            reason=data["reason"] if "reason" in data else None
        )


@dataclass
class BlockCommunity:
    """https://join-lemmy.org/api/interfaces/BlockCommunity.html"""

    community_id: int = None
    block: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            block=data["block"]
        )


@dataclass
class AdminPurgePost:
    """https://join-lemmy.org/api/interfaces/AdminPurgePost.html"""

    id: int = None
    admin_person_id: int = None
    community_id: int = None
    reason: Optional[str] = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            admin_person_id=data["admin_person_id"],
            community_id=data["community_id"],
            reason=data["reason"] if "reason" in data else None,
            when_=data["when_"]
        )


@dataclass
class ResolvePostReport:
    """https://join-lemmy.org/api/interfaces/ResolvePostReport.html"""

    report_id: int = None
    resolved: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            report_id=data["report_id"],
            resolved=data["resolved"]
        )


@dataclass
class CreateComment:
    """https://join-lemmy.org/api/interfaces/CreateComment.html"""

    content: str = None
    post_id: int = None
    parent_id: Optional[int] = None
    language_id: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            content=data["content"],
            post_id=data["post_id"],
            parent_id=data["parent_id"] if "parent_id" in data else None,
            language_id=data["language_id"] if "language_id" in data else None
        )


@dataclass
class ListRegistrationApplications:
    """https://join-lemmy.org/api/interfaces/ListRegistrationApplications.html"""

    unread_only: Optional[bool] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            unread_only=data["unread_only"] if "unread_only" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None
        )


@dataclass
class DistinguishComment:
    """https://join-lemmy.org/api/interfaces/DistinguishComment.html"""

    comment_id: int = None
    distinguished: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"],
            distinguished=data["distinguished"]
        )


@dataclass
class CommentReport:
    """https://join-lemmy.org/api/interfaces/CommentReport.html"""

    id: int = None
    creator_id: int = None
    comment_id: int = None
    original_comment_text: str = None
    reason: str = None
    resolved: bool = None
    resolver_id: Optional[int] = None
    published: str = None
    updated: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            creator_id=data["creator_id"],
            comment_id=data["comment_id"],
            original_comment_text=data["original_comment_text"],
            reason=data["reason"],
            resolved=data["resolved"],
            resolver_id=data["resolver_id"] if "resolver_id" in data else None,
            published=data["published"],
            updated=data["updated"] if "updated" in data else None
        )


@dataclass
class DeleteCustomEmoji:
    """https://join-lemmy.org/api/interfaces/DeleteCustomEmoji.html"""

    id: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"]
        )


@dataclass
class BanPerson:
    """https://join-lemmy.org/api/interfaces/BanPerson.html"""

    person_id: int = None
    ban: bool = None
    remove_data: Optional[bool] = None
    reason: Optional[str] = None
    expires: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person_id=data["person_id"],
            ban=data["ban"],
            remove_data=data["remove_data"] if "remove_data" in data else None,
            reason=data["reason"] if "reason" in data else None,
            expires=data["expires"] if "expires" in data else None
        )


@dataclass
class ListCommentReports:
    """https://join-lemmy.org/api/interfaces/ListCommentReports.html"""

    comment_id: Optional[int] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    unresolved_only: Optional[bool] = None
    community_id: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_id=data["comment_id"] if "comment_id" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            unresolved_only=data["unresolved_only"] if "unresolved_only" in data else None,
            community_id=data["community_id"] if "community_id" in data else None
        )


@dataclass
class ModAdd:
    """https://join-lemmy.org/api/interfaces/ModAdd.html"""

    id: int = None
    mod_person_id: int = None
    other_person_id: int = None
    removed: bool = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            mod_person_id=data["mod_person_id"],
            other_person_id=data["other_person_id"],
            removed=data["removed"],
            when_=data["when_"]
        )


@dataclass
class EditSite:
    """https://join-lemmy.org/api/interfaces/EditSite.html"""

    name: Optional[str] = None
    sidebar: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    banner: Optional[str] = None
    enable_downvotes: Optional[bool] = None
    enable_nsfw: Optional[bool] = None
    community_creation_admin_only: Optional[bool] = None
    require_email_verification: Optional[bool] = None
    application_question: Optional[str] = None
    private_instance: Optional[bool] = None
    default_theme: Optional[str] = None
    default_post_listing_type: Optional[str] = None
    default_sort_type: Optional[str] = None
    legal_information: Optional[str] = None
    application_email_admins: Optional[bool] = None
    hide_modlog_mod_names: Optional[bool] = None
    discussion_languages: Optional[list[int]] = None
    slur_filter_regex: Optional[str] = None
    actor_name_max_length: Optional[int] = None
    rate_limit_message: Optional[int] = None
    rate_limit_message_per_second: Optional[int] = None
    rate_limit_post: Optional[int] = None
    rate_limit_post_per_second: Optional[int] = None
    rate_limit_register: Optional[int] = None
    rate_limit_register_per_second: Optional[int] = None
    rate_limit_image: Optional[int] = None
    rate_limit_image_per_second: Optional[int] = None
    rate_limit_comment: Optional[int] = None
    rate_limit_comment_per_second: Optional[int] = None
    rate_limit_search: Optional[int] = None
    rate_limit_search_per_second: Optional[int] = None
    federation_enabled: Optional[bool] = None
    federation_debug: Optional[bool] = None
    captcha_enabled: Optional[bool] = None
    captcha_difficulty: Optional[str] = None
    allowed_instances: Optional[list[str]] = None
    blocked_instances: Optional[list[str]] = None
    blocked_urls: Optional[list[str]] = None
    taglines: Optional[list[str]] = None
    registration_mode: Optional[str] = None
    reports_email_admins: Optional[bool] = None
    content_warning: Optional[str] = None
    default_post_listing_mode: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            name=data["name"] if "name" in data else None,
            sidebar=data["sidebar"] if "sidebar" in data else None,
            description=data["description"] if "description" in data else None,
            icon=data["icon"] if "icon" in data else None,
            banner=data["banner"] if "banner" in data else None,
            enable_downvotes=data["enable_downvotes"] if "enable_downvotes" in data else None,
            enable_nsfw=data["enable_nsfw"] if "enable_nsfw" in data else None,
            community_creation_admin_only=data["community_creation_admin_only"] if "community_creation_admin_only" in data else None,
            require_email_verification=data["require_email_verification"] if "require_email_verification" in data else None,
            application_question=data["application_question"] if "application_question" in data else None,
            private_instance=data["private_instance"] if "private_instance" in data else None,
            default_theme=data["default_theme"] if "default_theme" in data else None,
            default_post_listing_type=data["default_post_listing_type"] if "default_post_listing_type" in data else None,
            default_sort_type=data["default_sort_type"] if "default_sort_type" in data else None,
            legal_information=data["legal_information"] if "legal_information" in data else None,
            application_email_admins=data["application_email_admins"] if "application_email_admins" in data else None,
            hide_modlog_mod_names=data["hide_modlog_mod_names"] if "hide_modlog_mod_names" in data else None,
            discussion_languages=[e0 for e0 in data["discussion_languages"]] if "discussion_languages" in data else None,
            slur_filter_regex=data["slur_filter_regex"] if "slur_filter_regex" in data else None,
            actor_name_max_length=data["actor_name_max_length"] if "actor_name_max_length" in data else None,
            rate_limit_message=data["rate_limit_message"] if "rate_limit_message" in data else None,
            rate_limit_message_per_second=data["rate_limit_message_per_second"] if "rate_limit_message_per_second" in data else None,
            rate_limit_post=data["rate_limit_post"] if "rate_limit_post" in data else None,
            rate_limit_post_per_second=data["rate_limit_post_per_second"] if "rate_limit_post_per_second" in data else None,
            rate_limit_register=data["rate_limit_register"] if "rate_limit_register" in data else None,
            rate_limit_register_per_second=data["rate_limit_register_per_second"] if "rate_limit_register_per_second" in data else None,
            rate_limit_image=data["rate_limit_image"] if "rate_limit_image" in data else None,
            rate_limit_image_per_second=data["rate_limit_image_per_second"] if "rate_limit_image_per_second" in data else None,
            rate_limit_comment=data["rate_limit_comment"] if "rate_limit_comment" in data else None,
            rate_limit_comment_per_second=data["rate_limit_comment_per_second"] if "rate_limit_comment_per_second" in data else None,
            rate_limit_search=data["rate_limit_search"] if "rate_limit_search" in data else None,
            rate_limit_search_per_second=data["rate_limit_search_per_second"] if "rate_limit_search_per_second" in data else None,
            federation_enabled=data["federation_enabled"] if "federation_enabled" in data else None,
            federation_debug=data["federation_debug"] if "federation_debug" in data else None,
            captcha_enabled=data["captcha_enabled"] if "captcha_enabled" in data else None,
            captcha_difficulty=data["captcha_difficulty"] if "captcha_difficulty" in data else None,
            allowed_instances=[e0 for e0 in data["allowed_instances"]] if "allowed_instances" in data else None,
            blocked_instances=[e0 for e0 in data["blocked_instances"]] if "blocked_instances" in data else None,
            blocked_urls=[e0 for e0 in data["blocked_urls"]] if "blocked_urls" in data else None,
            taglines=[e0 for e0 in data["taglines"]] if "taglines" in data else None,
            registration_mode=data["registration_mode"] if "registration_mode" in data else None,
            reports_email_admins=data["reports_email_admins"] if "reports_email_admins" in data else None,
            content_warning=data["content_warning"] if "content_warning" in data else None,
            default_post_listing_mode=data["default_post_listing_mode"] if "default_post_listing_mode" in data else None
        )


@dataclass
class Instance:
    """https://join-lemmy.org/api/interfaces/Instance.html"""

    id: int = None
    domain: str = None
    published: str = None
    updated: Optional[str] = None
    software: Optional[str] = None
    version: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            domain=data["domain"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            software=data["software"] if "software" in data else None,
            version=data["version"] if "version" in data else None
        )


@dataclass
class Post:
    """https://join-lemmy.org/api/interfaces/Post.html"""

    id: int = None
    name: str = None
    url: Optional[str] = None
    body: Optional[str] = None
    creator_id: int = None
    community_id: int = None
    removed: bool = None
    locked: bool = None
    published: str = None
    updated: Optional[str] = None
    deleted: bool = None
    nsfw: bool = None
    embed_title: Optional[str] = None
    embed_description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    ap_id: str = None
    local: bool = None
    embed_video_url: Optional[str] = None
    language_id: int = None
    featured_community: bool = None
    featured_local: bool = None
    url_content_type: Optional[str] = None
    alt_text: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            name=data["name"],
            url=data["url"] if "url" in data else None,
            body=data["body"] if "body" in data else None,
            creator_id=data["creator_id"],
            community_id=data["community_id"],
            removed=data["removed"],
            locked=data["locked"],
            published=data["published"],
            updated=data["updated"] if "updated" in data else None,
            deleted=data["deleted"],
            nsfw=data["nsfw"],
            embed_title=data["embed_title"] if "embed_title" in data else None,
            embed_description=data["embed_description"] if "embed_description" in data else None,
            thumbnail_url=data["thumbnail_url"] if "thumbnail_url" in data else None,
            ap_id=data["ap_id"],
            local=data["local"],
            embed_video_url=data["embed_video_url"] if "embed_video_url" in data else None,
            language_id=data["language_id"],
            featured_community=data["featured_community"],
            featured_local=data["featured_local"],
            url_content_type=data["url_content_type"] if "url_content_type" in data else None,
            alt_text=data["alt_text"] if "alt_text" in data else None
        )


@dataclass
class GetPosts:
    """https://join-lemmy.org/api/interfaces/GetPosts.html"""

    type_: Optional[str] = None
    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    community_id: Optional[int] = None
    community_name: Optional[str] = None
    saved_only: Optional[bool] = None
    liked_only: Optional[bool] = None
    disliked_only: Optional[bool] = None
    show_hidden: Optional[bool] = None
    show_read: Optional[bool] = None
    show_nsfw: Optional[bool] = None
    page_cursor: Optional[str] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            type_=data["type_"] if "type_" in data else None,
            sort=data["sort"] if "sort" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            community_id=data["community_id"] if "community_id" in data else None,
            community_name=data["community_name"] if "community_name" in data else None,
            saved_only=data["saved_only"] if "saved_only" in data else None,
            liked_only=data["liked_only"] if "liked_only" in data else None,
            disliked_only=data["disliked_only"] if "disliked_only" in data else None,
            show_hidden=data["show_hidden"] if "show_hidden" in data else None,
            show_read=data["show_read"] if "show_read" in data else None,
            show_nsfw=data["show_nsfw"] if "show_nsfw" in data else None,
            page_cursor=data["page_cursor"] if "page_cursor" in data else None
        )


@dataclass
class GetRegistrationApplication:
    """https://join-lemmy.org/api/interfaces/GetRegistrationApplication.html"""

    person_id: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person_id=data["person_id"]
        )


@dataclass
class GetReplies:
    """https://join-lemmy.org/api/interfaces/GetReplies.html"""

    sort: Optional[str] = None
    page: Optional[int] = None
    limit: Optional[int] = None
    unread_only: Optional[bool] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            sort=data["sort"] if "sort" in data else None,
            page=data["page"] if "page" in data else None,
            limit=data["limit"] if "limit" in data else None,
            unread_only=data["unread_only"] if "unread_only" in data else None
        )


@dataclass
class AdminPurgePerson:
    """https://join-lemmy.org/api/interfaces/AdminPurgePerson.html"""

    id: int = None
    admin_person_id: int = None
    reason: Optional[str] = None
    when_: str = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            id=data["id"],
            admin_person_id=data["admin_person_id"],
            reason=data["reason"] if "reason" in data else None,
            when_=data["when_"]
        )


@dataclass
class TransferCommunity:
    """https://join-lemmy.org/api/interfaces/TransferCommunity.html"""

    community_id: int = None
    person_id: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community_id=data["community_id"],
            person_id=data["person_id"]
        )

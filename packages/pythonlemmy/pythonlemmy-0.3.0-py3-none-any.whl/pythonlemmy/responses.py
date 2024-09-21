from dataclasses import dataclass
from typing import Optional, Any
import requests

from .views import *
from .objects import *
from .types import ResponseWrapper


class CaptchaResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/CaptchaResponse.html"""

    png: str = None
    wav: str = None
    uuid: str = None
    
    def parse(self, data: dict[str, Any]):
        self.png = data["png"]
        self.wav = data["wav"]
        self.uuid = data["uuid"]

    @classmethod
    def data(
        cls, 
        png: str = None,
        wav: str = None,
        uuid: str = None
    ):
        obj = cls.__new__(cls)
        obj.png = png
        obj.wav = wav
        obj.uuid = uuid
        return obj


class BannedPersonsResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/BannedPersonsResponse.html"""

    banned: list[PersonView] = None
    
    def parse(self, data: dict[str, Any]):
        self.banned = [PersonView.parse(e0) for e0 in data["banned"]]

    @classmethod
    def data(
        cls, 
        banned: list[PersonView] = None
    ):
        obj = cls.__new__(cls)
        obj.banned = banned
        return obj


class ListMediaResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/ListMediaResponse.html"""

    images: list[LocalImageView] = None
    
    def parse(self, data: dict[str, Any]):
        self.images = [LocalImageView.parse(e0) for e0 in data["images"]]

    @classmethod
    def data(
        cls, 
        images: list[LocalImageView] = None
    ):
        obj = cls.__new__(cls)
        obj.images = images
        return obj


class UpdateTotpResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/UpdateTotpResponse.html"""

    enabled: bool = None
    
    def parse(self, data: dict[str, Any]):
        self.enabled = data["enabled"]

    @classmethod
    def data(
        cls, 
        enabled: bool = None
    ):
        obj = cls.__new__(cls)
        obj.enabled = enabled
        return obj


class CommentReportResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/CommentReportResponse.html"""

    comment_report_view: CommentReportView = None
    
    def parse(self, data: dict[str, Any]):
        self.comment_report_view = CommentReportView.parse(data["comment_report_view"])

    @classmethod
    def data(
        cls, 
        comment_report_view: CommentReportView = None
    ):
        obj = cls.__new__(cls)
        obj.comment_report_view = comment_report_view
        return obj


class GetCommunityResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetCommunityResponse.html"""

    community_view: CommunityView = None
    site: Optional[Site] = None
    moderators: list[CommunityModeratorView] = None
    discussion_languages: list[int] = None
    
    def parse(self, data: dict[str, Any]):
        self.community_view = CommunityView.parse(data["community_view"])
        self.site = Site.parse(data["site"]) if "site" in data else None
        self.moderators = [CommunityModeratorView.parse(e0) for e0 in data["moderators"]]
        self.discussion_languages = [e0 for e0 in data["discussion_languages"]]

    @classmethod
    def data(
        cls, 
        community_view: CommunityView = None,
        site: Optional[Site] = None,
        moderators: list[CommunityModeratorView] = None,
        discussion_languages: list[int] = None
    ):
        obj = cls.__new__(cls)
        obj.community_view = community_view
        obj.site = site
        obj.moderators = moderators
        obj.discussion_languages = discussion_languages
        return obj


class GetPostsResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetPostsResponse.html"""

    posts: list[PostView] = None
    next_page: Optional[str] = None
    
    def parse(self, data: dict[str, Any]):
        self.posts = [PostView.parse(e0) for e0 in data["posts"]]
        self.next_page = data["next_page"] if "next_page" in data else None

    @classmethod
    def data(
        cls, 
        posts: list[PostView] = None,
        next_page: Optional[str] = None
    ):
        obj = cls.__new__(cls)
        obj.posts = posts
        obj.next_page = next_page
        return obj


class CommunityResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/CommunityResponse.html"""

    community_view: CommunityView = None
    discussion_languages: list[int] = None
    
    def parse(self, data: dict[str, Any]):
        self.community_view = CommunityView.parse(data["community_view"])
        self.discussion_languages = [e0 for e0 in data["discussion_languages"]]

    @classmethod
    def data(
        cls, 
        community_view: CommunityView = None,
        discussion_languages: list[int] = None
    ):
        obj = cls.__new__(cls)
        obj.community_view = community_view
        obj.discussion_languages = discussion_languages
        return obj


class GetCommentsResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetCommentsResponse.html"""

    comments: list[CommentView] = None
    
    def parse(self, data: dict[str, Any]):
        self.comments = [CommentView.parse(e0) for e0 in data["comments"]]

    @classmethod
    def data(
        cls, 
        comments: list[CommentView] = None
    ):
        obj = cls.__new__(cls)
        obj.comments = comments
        return obj


class SearchResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/SearchResponse.html"""

    type_: str = None
    comments: list[CommentView] = None
    posts: list[PostView] = None
    communities: list[CommunityView] = None
    users: list[PersonView] = None
    
    def parse(self, data: dict[str, Any]):
        self.type_ = data["type_"]
        self.comments = [CommentView.parse(e0) for e0 in data["comments"]]
        self.posts = [PostView.parse(e0) for e0 in data["posts"]]
        self.communities = [CommunityView.parse(e0) for e0 in data["communities"]]
        self.users = [PersonView.parse(e0) for e0 in data["users"]]

    @classmethod
    def data(
        cls, 
        type_: str = None,
        comments: list[CommentView] = None,
        posts: list[PostView] = None,
        communities: list[CommunityView] = None,
        users: list[PersonView] = None
    ):
        obj = cls.__new__(cls)
        obj.type_ = type_
        obj.comments = comments
        obj.posts = posts
        obj.communities = communities
        obj.users = users
        return obj


class PrivateMessageResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/PrivateMessageResponse.html"""

    private_message_view: PrivateMessageView = None
    
    def parse(self, data: dict[str, Any]):
        self.private_message_view = PrivateMessageView.parse(data["private_message_view"])

    @classmethod
    def data(
        cls, 
        private_message_view: PrivateMessageView = None
    ):
        obj = cls.__new__(cls)
        obj.private_message_view = private_message_view
        return obj


class AddModToCommunityResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/AddModToCommunityResponse.html"""

    moderators: list[CommunityModeratorView] = None
    
    def parse(self, data: dict[str, Any]):
        self.moderators = [CommunityModeratorView.parse(e0) for e0 in data["moderators"]]

    @classmethod
    def data(
        cls, 
        moderators: list[CommunityModeratorView] = None
    ):
        obj = cls.__new__(cls)
        obj.moderators = moderators
        return obj


class GetReportCountResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetReportCountResponse.html"""

    community_id: Optional[int] = None
    comment_reports: int = None
    post_reports: int = None
    private_message_reports: Optional[int] = None
    
    def parse(self, data: dict[str, Any]):
        self.community_id = data["community_id"] if "community_id" in data else None
        self.comment_reports = data["comment_reports"]
        self.post_reports = data["post_reports"]
        self.private_message_reports = data["private_message_reports"] if "private_message_reports" in data else None

    @classmethod
    def data(
        cls, 
        community_id: Optional[int] = None,
        comment_reports: int = None,
        post_reports: int = None,
        private_message_reports: Optional[int] = None
    ):
        obj = cls.__new__(cls)
        obj.community_id = community_id
        obj.comment_reports = comment_reports
        obj.post_reports = post_reports
        obj.private_message_reports = private_message_reports
        return obj


class PostReportResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/PostReportResponse.html"""

    post_report_view: PostReportView = None
    
    def parse(self, data: dict[str, Any]):
        self.post_report_view = PostReportView.parse(data["post_report_view"])

    @classmethod
    def data(
        cls, 
        post_report_view: PostReportView = None
    ):
        obj = cls.__new__(cls)
        obj.post_report_view = post_report_view
        return obj


class RegistrationApplicationResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/RegistrationApplicationResponse.html"""

    registration_application: RegistrationApplicationView = None
    
    def parse(self, data: dict[str, Any]):
        self.registration_application = RegistrationApplicationView.parse(data["registration_application"])

    @classmethod
    def data(
        cls, 
        registration_application: RegistrationApplicationView = None
    ):
        obj = cls.__new__(cls)
        obj.registration_application = registration_application
        return obj


class GetSiteResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetSiteResponse.html"""

    site_view: SiteView = None
    admins: list[PersonView] = None
    version: str = None
    my_user: Optional[MyUserInfo] = None
    all_languages: list[Language] = None
    discussion_languages: list[int] = None
    taglines: list[Tagline] = None
    custom_emojis: list[CustomEmojiView] = None
    blocked_urls: list[LocalSiteUrlBlocklist] = None
    
    def parse(self, data: dict[str, Any]):
        self.site_view = SiteView.parse(data["site_view"])
        self.admins = [PersonView.parse(e0) for e0 in data["admins"]]
        self.version = data["version"]
        self.my_user = MyUserInfo.parse(data["my_user"]) if "my_user" in data else None
        self.all_languages = [Language.parse(e0) for e0 in data["all_languages"]]
        self.discussion_languages = [e0 for e0 in data["discussion_languages"]]
        self.taglines = [Tagline.parse(e0) for e0 in data["taglines"]]
        self.custom_emojis = [CustomEmojiView.parse(e0) for e0 in data["custom_emojis"]]
        self.blocked_urls = [LocalSiteUrlBlocklist.parse(e0) for e0 in data["blocked_urls"]]

    @classmethod
    def data(
        cls, 
        site_view: SiteView = None,
        admins: list[PersonView] = None,
        version: str = None,
        my_user: Optional[MyUserInfo] = None,
        all_languages: list[Language] = None,
        discussion_languages: list[int] = None,
        taglines: list[Tagline] = None,
        custom_emojis: list[CustomEmojiView] = None,
        blocked_urls: list[LocalSiteUrlBlocklist] = None
    ):
        obj = cls.__new__(cls)
        obj.site_view = site_view
        obj.admins = admins
        obj.version = version
        obj.my_user = my_user
        obj.all_languages = all_languages
        obj.discussion_languages = discussion_languages
        obj.taglines = taglines
        obj.custom_emojis = custom_emojis
        obj.blocked_urls = blocked_urls
        return obj


class GetCaptchaResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetCaptchaResponse.html"""

    ok: Optional[CaptchaResponse] = None
    
    def parse(self, data: dict[str, Any]):
        self.ok = CaptchaResponse.parse(data["ok"]) if "ok" in data else None

    @classmethod
    def data(
        cls, 
        ok: Optional[CaptchaResponse] = None
    ):
        obj = cls.__new__(cls)
        obj.ok = ok
        return obj


class PersonMentionResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/PersonMentionResponse.html"""

    person_mention_view: PersonMentionView = None
    
    def parse(self, data: dict[str, Any]):
        self.person_mention_view = PersonMentionView.parse(data["person_mention_view"])

    @classmethod
    def data(
        cls, 
        person_mention_view: PersonMentionView = None
    ):
        obj = cls.__new__(cls)
        obj.person_mention_view = person_mention_view
        return obj


class GetModlogResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetModlogResponse.html"""

    removed_posts: list[ModRemovePostView] = None
    locked_posts: list[ModLockPostView] = None
    featured_posts: list[ModFeaturePostView] = None
    removed_comments: list[ModRemoveCommentView] = None
    removed_communities: list[ModRemoveCommunityView] = None
    banned_from_community: list[ModBanFromCommunityView] = None
    banned: list[ModBanView] = None
    added_to_community: list[ModAddCommunityView] = None
    transferred_to_community: list[ModTransferCommunityView] = None
    added: list[ModAddView] = None
    admin_purged_persons: list[AdminPurgePersonView] = None
    admin_purged_communities: list[AdminPurgeCommunityView] = None
    admin_purged_posts: list[AdminPurgePostView] = None
    admin_purged_comments: list[AdminPurgeCommentView] = None
    hidden_communities: list[ModHideCommunityView] = None
    
    def parse(self, data: dict[str, Any]):
        self.removed_posts = [ModRemovePostView.parse(e0) for e0 in data["removed_posts"]]
        self.locked_posts = [ModLockPostView.parse(e0) for e0 in data["locked_posts"]]
        self.featured_posts = [ModFeaturePostView.parse(e0) for e0 in data["featured_posts"]]
        self.removed_comments = [ModRemoveCommentView.parse(e0) for e0 in data["removed_comments"]]
        self.removed_communities = [ModRemoveCommunityView.parse(e0) for e0 in data["removed_communities"]]
        self.banned_from_community = [ModBanFromCommunityView.parse(e0) for e0 in data["banned_from_community"]]
        self.banned = [ModBanView.parse(e0) for e0 in data["banned"]]
        self.added_to_community = [ModAddCommunityView.parse(e0) for e0 in data["added_to_community"]]
        self.transferred_to_community = [ModTransferCommunityView.parse(e0) for e0 in data["transferred_to_community"]]
        self.added = [ModAddView.parse(e0) for e0 in data["added"]]
        self.admin_purged_persons = [AdminPurgePersonView.parse(e0) for e0 in data["admin_purged_persons"]]
        self.admin_purged_communities = [AdminPurgeCommunityView.parse(e0) for e0 in data["admin_purged_communities"]]
        self.admin_purged_posts = [AdminPurgePostView.parse(e0) for e0 in data["admin_purged_posts"]]
        self.admin_purged_comments = [AdminPurgeCommentView.parse(e0) for e0 in data["admin_purged_comments"]]
        self.hidden_communities = [ModHideCommunityView.parse(e0) for e0 in data["hidden_communities"]]

    @classmethod
    def data(
        cls, 
        removed_posts: list[ModRemovePostView] = None,
        locked_posts: list[ModLockPostView] = None,
        featured_posts: list[ModFeaturePostView] = None,
        removed_comments: list[ModRemoveCommentView] = None,
        removed_communities: list[ModRemoveCommunityView] = None,
        banned_from_community: list[ModBanFromCommunityView] = None,
        banned: list[ModBanView] = None,
        added_to_community: list[ModAddCommunityView] = None,
        transferred_to_community: list[ModTransferCommunityView] = None,
        added: list[ModAddView] = None,
        admin_purged_persons: list[AdminPurgePersonView] = None,
        admin_purged_communities: list[AdminPurgeCommunityView] = None,
        admin_purged_posts: list[AdminPurgePostView] = None,
        admin_purged_comments: list[AdminPurgeCommentView] = None,
        hidden_communities: list[ModHideCommunityView] = None
    ):
        obj = cls.__new__(cls)
        obj.removed_posts = removed_posts
        obj.locked_posts = locked_posts
        obj.featured_posts = featured_posts
        obj.removed_comments = removed_comments
        obj.removed_communities = removed_communities
        obj.banned_from_community = banned_from_community
        obj.banned = banned
        obj.added_to_community = added_to_community
        obj.transferred_to_community = transferred_to_community
        obj.added = added
        obj.admin_purged_persons = admin_purged_persons
        obj.admin_purged_communities = admin_purged_communities
        obj.admin_purged_posts = admin_purged_posts
        obj.admin_purged_comments = admin_purged_comments
        obj.hidden_communities = hidden_communities
        return obj


class SuccessResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/SuccessResponse.html"""

    success: bool = None
    
    def parse(self, data: dict[str, Any]):
        self.success = data["success"]

    @classmethod
    def data(
        cls, 
        success: bool = None
    ):
        obj = cls.__new__(cls)
        obj.success = success
        return obj


class ListRegistrationApplicationsResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/ListRegistrationApplicationsResponse.html"""

    registration_applications: list[RegistrationApplicationView] = None
    
    def parse(self, data: dict[str, Any]):
        self.registration_applications = [RegistrationApplicationView.parse(e0) for e0 in data["registration_applications"]]

    @classmethod
    def data(
        cls, 
        registration_applications: list[RegistrationApplicationView] = None
    ):
        obj = cls.__new__(cls)
        obj.registration_applications = registration_applications
        return obj


class BlockInstanceResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/BlockInstanceResponse.html"""

    blocked: bool = None
    
    def parse(self, data: dict[str, Any]):
        self.blocked = data["blocked"]

    @classmethod
    def data(
        cls, 
        blocked: bool = None
    ):
        obj = cls.__new__(cls)
        obj.blocked = blocked
        return obj


class ResolveObjectResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/ResolveObjectResponse.html"""

    comment: Optional[CommentView] = None
    post: Optional[PostView] = None
    community: Optional[CommunityView] = None
    person: Optional[PersonView] = None
    
    def parse(self, data: dict[str, Any]):
        self.comment = CommentView.parse(data["comment"]) if "comment" in data else None
        self.post = PostView.parse(data["post"]) if "post" in data else None
        self.community = CommunityView.parse(data["community"]) if "community" in data else None
        self.person = PersonView.parse(data["person"]) if "person" in data else None

    @classmethod
    def data(
        cls, 
        comment: Optional[CommentView] = None,
        post: Optional[PostView] = None,
        community: Optional[CommunityView] = None,
        person: Optional[PersonView] = None
    ):
        obj = cls.__new__(cls)
        obj.comment = comment
        obj.post = post
        obj.community = community
        obj.person = person
        return obj


class PrivateMessageReportResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/PrivateMessageReportResponse.html"""

    private_message_report_view: PrivateMessageReportView = None
    
    def parse(self, data: dict[str, Any]):
        self.private_message_report_view = PrivateMessageReportView.parse(data["private_message_report_view"])

    @classmethod
    def data(
        cls, 
        private_message_report_view: PrivateMessageReportView = None
    ):
        obj = cls.__new__(cls)
        obj.private_message_report_view = private_message_report_view
        return obj


class SiteResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/SiteResponse.html"""

    site_view: SiteView = None
    taglines: list[Tagline] = None
    
    def parse(self, data: dict[str, Any]):
        self.site_view = SiteView.parse(data["site_view"])
        self.taglines = [Tagline.parse(e0) for e0 in data["taglines"]]

    @classmethod
    def data(
        cls, 
        site_view: SiteView = None,
        taglines: list[Tagline] = None
    ):
        obj = cls.__new__(cls)
        obj.site_view = site_view
        obj.taglines = taglines
        return obj


class ListPostReportsResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/ListPostReportsResponse.html"""

    post_reports: list[PostReportView] = None
    
    def parse(self, data: dict[str, Any]):
        self.post_reports = [PostReportView.parse(e0) for e0 in data["post_reports"]]

    @classmethod
    def data(
        cls, 
        post_reports: list[PostReportView] = None
    ):
        obj = cls.__new__(cls)
        obj.post_reports = post_reports
        return obj


class BlockCommunityResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/BlockCommunityResponse.html"""

    community_view: CommunityView = None
    blocked: bool = None
    
    def parse(self, data: dict[str, Any]):
        self.community_view = CommunityView.parse(data["community_view"])
        self.blocked = data["blocked"]

    @classmethod
    def data(
        cls, 
        community_view: CommunityView = None,
        blocked: bool = None
    ):
        obj = cls.__new__(cls)
        obj.community_view = community_view
        obj.blocked = blocked
        return obj


class PrivateMessagesResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/PrivateMessagesResponse.html"""

    private_messages: list[PrivateMessageView] = None
    
    def parse(self, data: dict[str, Any]):
        self.private_messages = [PrivateMessageView.parse(e0) for e0 in data["private_messages"]]

    @classmethod
    def data(
        cls, 
        private_messages: list[PrivateMessageView] = None
    ):
        obj = cls.__new__(cls)
        obj.private_messages = private_messages
        return obj


class LoginResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/LoginResponse.html"""

    jwt: Optional[str] = None
    registration_created: bool = None
    verify_email_sent: bool = None
    
    def parse(self, data: dict[str, Any]):
        self.jwt = data["jwt"] if "jwt" in data else None
        self.registration_created = data["registration_created"]
        self.verify_email_sent = data["verify_email_sent"]

    @classmethod
    def data(
        cls, 
        jwt: Optional[str] = None,
        registration_created: bool = None,
        verify_email_sent: bool = None
    ):
        obj = cls.__new__(cls)
        obj.jwt = jwt
        obj.registration_created = registration_created
        obj.verify_email_sent = verify_email_sent
        return obj


class GetUnreadCountResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetUnreadCountResponse.html"""

    replies: int = None
    mentions: int = None
    private_messages: int = None
    
    def parse(self, data: dict[str, Any]):
        self.replies = data["replies"]
        self.mentions = data["mentions"]
        self.private_messages = data["private_messages"]

    @classmethod
    def data(
        cls, 
        replies: int = None,
        mentions: int = None,
        private_messages: int = None
    ):
        obj = cls.__new__(cls)
        obj.replies = replies
        obj.mentions = mentions
        obj.private_messages = private_messages
        return obj


class BanFromCommunityResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/BanFromCommunityResponse.html"""

    person_view: PersonView = None
    banned: bool = None
    
    def parse(self, data: dict[str, Any]):
        self.person_view = PersonView.parse(data["person_view"])
        self.banned = data["banned"]

    @classmethod
    def data(
        cls, 
        person_view: PersonView = None,
        banned: bool = None
    ):
        obj = cls.__new__(cls)
        obj.person_view = person_view
        obj.banned = banned
        return obj


class CommentReplyResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/CommentReplyResponse.html"""

    comment_reply_view: CommentReplyView = None
    
    def parse(self, data: dict[str, Any]):
        self.comment_reply_view = CommentReplyView.parse(data["comment_reply_view"])

    @classmethod
    def data(
        cls, 
        comment_reply_view: CommentReplyView = None
    ):
        obj = cls.__new__(cls)
        obj.comment_reply_view = comment_reply_view
        return obj


class ListPostLikesResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/ListPostLikesResponse.html"""

    post_likes: list[VoteView] = None
    
    def parse(self, data: dict[str, Any]):
        self.post_likes = [VoteView.parse(e0) for e0 in data["post_likes"]]

    @classmethod
    def data(
        cls, 
        post_likes: list[VoteView] = None
    ):
        obj = cls.__new__(cls)
        obj.post_likes = post_likes
        return obj


class ListCommentReportsResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/ListCommentReportsResponse.html"""

    comment_reports: list[CommentReportView] = None
    
    def parse(self, data: dict[str, Any]):
        self.comment_reports = [CommentReportView.parse(e0) for e0 in data["comment_reports"]]

    @classmethod
    def data(
        cls, 
        comment_reports: list[CommentReportView] = None
    ):
        obj = cls.__new__(cls)
        obj.comment_reports = comment_reports
        return obj


class GetSiteMetadataResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetSiteMetadataResponse.html"""

    metadata: LinkMetadata = None
    
    def parse(self, data: dict[str, Any]):
        self.metadata = LinkMetadata.parse(data["metadata"])

    @classmethod
    def data(
        cls, 
        metadata: LinkMetadata = None
    ):
        obj = cls.__new__(cls)
        obj.metadata = metadata
        return obj


class BanPersonResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/BanPersonResponse.html"""

    person_view: PersonView = None
    banned: bool = None
    
    def parse(self, data: dict[str, Any]):
        self.person_view = PersonView.parse(data["person_view"])
        self.banned = data["banned"]

    @classmethod
    def data(
        cls, 
        person_view: PersonView = None,
        banned: bool = None
    ):
        obj = cls.__new__(cls)
        obj.person_view = person_view
        obj.banned = banned
        return obj


class CommentResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/CommentResponse.html"""

    comment_view: CommentView = None
    recipient_ids: list[int] = None
    
    def parse(self, data: dict[str, Any]):
        self.comment_view = CommentView.parse(data["comment_view"])
        self.recipient_ids = [e0 for e0 in data["recipient_ids"]]

    @classmethod
    def data(
        cls, 
        comment_view: CommentView = None,
        recipient_ids: list[int] = None
    ):
        obj = cls.__new__(cls)
        obj.comment_view = comment_view
        obj.recipient_ids = recipient_ids
        return obj


class GetRepliesResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetRepliesResponse.html"""

    replies: list[CommentReplyView] = None
    
    def parse(self, data: dict[str, Any]):
        self.replies = [CommentReplyView.parse(e0) for e0 in data["replies"]]

    @classmethod
    def data(
        cls, 
        replies: list[CommentReplyView] = None
    ):
        obj = cls.__new__(cls)
        obj.replies = replies
        return obj


class GetUnreadRegistrationApplicationCountResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetUnreadRegistrationApplicationCountResponse.html"""

    registration_applications: int = None
    
    def parse(self, data: dict[str, Any]):
        self.registration_applications = data["registration_applications"]

    @classmethod
    def data(
        cls, 
        registration_applications: int = None
    ):
        obj = cls.__new__(cls)
        obj.registration_applications = registration_applications
        return obj


class CustomEmojiResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/CustomEmojiResponse.html"""

    custom_emoji: CustomEmojiView = None
    
    def parse(self, data: dict[str, Any]):
        self.custom_emoji = CustomEmojiView.parse(data["custom_emoji"])

    @classmethod
    def data(
        cls, 
        custom_emoji: CustomEmojiView = None
    ):
        obj = cls.__new__(cls)
        obj.custom_emoji = custom_emoji
        return obj


class GetPersonDetailsResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetPersonDetailsResponse.html"""

    person_view: PersonView = None
    site: Optional[Site] = None
    comments: list[CommentView] = None
    posts: list[PostView] = None
    moderates: list[CommunityModeratorView] = None
    
    def parse(self, data: dict[str, Any]):
        self.person_view = PersonView.parse(data["person_view"])
        self.site = Site.parse(data["site"]) if "site" in data else None
        self.comments = [CommentView.parse(e0) for e0 in data["comments"]]
        self.posts = [PostView.parse(e0) for e0 in data["posts"]]
        self.moderates = [CommunityModeratorView.parse(e0) for e0 in data["moderates"]]

    @classmethod
    def data(
        cls, 
        person_view: PersonView = None,
        site: Optional[Site] = None,
        comments: list[CommentView] = None,
        posts: list[PostView] = None,
        moderates: list[CommunityModeratorView] = None
    ):
        obj = cls.__new__(cls)
        obj.person_view = person_view
        obj.site = site
        obj.comments = comments
        obj.posts = posts
        obj.moderates = moderates
        return obj


class ListCommunitiesResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/ListCommunitiesResponse.html"""

    communities: list[CommunityView] = None
    
    def parse(self, data: dict[str, Any]):
        self.communities = [CommunityView.parse(e0) for e0 in data["communities"]]

    @classmethod
    def data(
        cls, 
        communities: list[CommunityView] = None
    ):
        obj = cls.__new__(cls)
        obj.communities = communities
        return obj


class GetPersonMentionsResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetPersonMentionsResponse.html"""

    mentions: list[PersonMentionView] = None
    
    def parse(self, data: dict[str, Any]):
        self.mentions = [PersonMentionView.parse(e0) for e0 in data["mentions"]]

    @classmethod
    def data(
        cls, 
        mentions: list[PersonMentionView] = None
    ):
        obj = cls.__new__(cls)
        obj.mentions = mentions
        return obj


class AddAdminResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/AddAdminResponse.html"""

    admins: list[PersonView] = None
    
    def parse(self, data: dict[str, Any]):
        self.admins = [PersonView.parse(e0) for e0 in data["admins"]]

    @classmethod
    def data(
        cls, 
        admins: list[PersonView] = None
    ):
        obj = cls.__new__(cls)
        obj.admins = admins
        return obj


class GetFederatedInstancesResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetFederatedInstancesResponse.html"""

    federated_instances: Optional[FederatedInstances] = None
    
    def parse(self, data: dict[str, Any]):
        self.federated_instances = FederatedInstances.parse(data["federated_instances"]) if "federated_instances" in data else None

    @classmethod
    def data(
        cls, 
        federated_instances: Optional[FederatedInstances] = None
    ):
        obj = cls.__new__(cls)
        obj.federated_instances = federated_instances
        return obj


class PostResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/PostResponse.html"""

    post_view: PostView = None
    
    def parse(self, data: dict[str, Any]):
        self.post_view = PostView.parse(data["post_view"])

    @classmethod
    def data(
        cls, 
        post_view: PostView = None
    ):
        obj = cls.__new__(cls)
        obj.post_view = post_view
        return obj


class GenerateTotpSecretResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GenerateTotpSecretResponse.html"""

    totp_secret_url: str = None
    
    def parse(self, data: dict[str, Any]):
        self.totp_secret_url = data["totp_secret_url"]

    @classmethod
    def data(
        cls, 
        totp_secret_url: str = None
    ):
        obj = cls.__new__(cls)
        obj.totp_secret_url = totp_secret_url
        return obj


class ListPrivateMessageReportsResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/ListPrivateMessageReportsResponse.html"""

    private_message_reports: list[PrivateMessageReportView] = None
    
    def parse(self, data: dict[str, Any]):
        self.private_message_reports = [PrivateMessageReportView.parse(e0) for e0 in data["private_message_reports"]]

    @classmethod
    def data(
        cls, 
        private_message_reports: list[PrivateMessageReportView] = None
    ):
        obj = cls.__new__(cls)
        obj.private_message_reports = private_message_reports
        return obj


class BlockPersonResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/BlockPersonResponse.html"""

    person_view: PersonView = None
    blocked: bool = None
    
    def parse(self, data: dict[str, Any]):
        self.person_view = PersonView.parse(data["person_view"])
        self.blocked = data["blocked"]

    @classmethod
    def data(
        cls, 
        person_view: PersonView = None,
        blocked: bool = None
    ):
        obj = cls.__new__(cls)
        obj.person_view = person_view
        obj.blocked = blocked
        return obj


class GetPostResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/GetPostResponse.html"""

    post_view: PostView = None
    community_view: CommunityView = None
    moderators: list[CommunityModeratorView] = None
    cross_posts: list[PostView] = None
    
    def parse(self, data: dict[str, Any]):
        self.post_view = PostView.parse(data["post_view"])
        self.community_view = CommunityView.parse(data["community_view"])
        self.moderators = [CommunityModeratorView.parse(e0) for e0 in data["moderators"]]
        self.cross_posts = [PostView.parse(e0) for e0 in data["cross_posts"]]

    @classmethod
    def data(
        cls, 
        post_view: PostView = None,
        community_view: CommunityView = None,
        moderators: list[CommunityModeratorView] = None,
        cross_posts: list[PostView] = None
    ):
        obj = cls.__new__(cls)
        obj.post_view = post_view
        obj.community_view = community_view
        obj.moderators = moderators
        obj.cross_posts = cross_posts
        return obj


class ListCommentLikesResponse(ResponseWrapper):
    """https://join-lemmy.org/api/interfaces/ListCommentLikesResponse.html"""

    comment_likes: list[VoteView] = None
    
    def parse(self, data: dict[str, Any]):
        self.comment_likes = [VoteView.parse(e0) for e0 in data["comment_likes"]]

    @classmethod
    def data(
        cls, 
        comment_likes: list[VoteView] = None
    ):
        obj = cls.__new__(cls)
        obj.comment_likes = comment_likes
        return obj

from dataclasses import dataclass
from typing import Optional, Any

from .objects import *


@dataclass
class LocalUserView:
    """https://join-lemmy.org/api/interfaces/LocalUserView.html"""

    local_user: LocalUser = None
    local_user_vote_display_mode: LocalUserVoteDisplayMode = None
    person: Person = None
    counts: PersonAggregates = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            local_user=LocalUser.parse(data["local_user"]),
            local_user_vote_display_mode=LocalUserVoteDisplayMode.parse(data["local_user_vote_display_mode"]),
            person=Person.parse(data["person"]),
            counts=PersonAggregates.parse(data["counts"])
        )


@dataclass
class CommentReplyView:
    """https://join-lemmy.org/api/interfaces/CommentReplyView.html"""

    comment_reply: CommentReply = None
    comment: Comment = None
    creator: Person = None
    post: Post = None
    community: Community = None
    recipient: Person = None
    counts: CommentAggregates = None
    creator_banned_from_community: bool = None
    banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    subscribed: str = None
    saved: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_reply=CommentReply.parse(data["comment_reply"]),
            comment=Comment.parse(data["comment"]),
            creator=Person.parse(data["creator"]),
            post=Post.parse(data["post"]),
            community=Community.parse(data["community"]),
            recipient=Person.parse(data["recipient"]),
            counts=CommentAggregates.parse(data["counts"]),
            creator_banned_from_community=data["creator_banned_from_community"],
            banned_from_community=data["banned_from_community"],
            creator_is_moderator=data["creator_is_moderator"],
            creator_is_admin=data["creator_is_admin"],
            subscribed=data["subscribed"],
            saved=data["saved"],
            creator_blocked=data["creator_blocked"],
            my_vote=data["my_vote"] if "my_vote" in data else None
        )


@dataclass
class CommunityFollowerView:
    """https://join-lemmy.org/api/interfaces/CommunityFollowerView.html"""

    community: Community = None
    follower: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community=Community.parse(data["community"]),
            follower=Person.parse(data["follower"])
        )


@dataclass
class VoteView:
    """https://join-lemmy.org/api/interfaces/VoteView.html"""

    creator: Person = None
    creator_banned_from_community: bool = None
    score: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            creator=Person.parse(data["creator"]),
            creator_banned_from_community=data["creator_banned_from_community"],
            score=data["score"]
        )


@dataclass
class PrivateMessageReportView:
    """https://join-lemmy.org/api/interfaces/PrivateMessageReportView.html"""

    private_message_report: PrivateMessageReport = None
    private_message: PrivateMessage = None
    private_message_creator: Person = None
    creator: Person = None
    resolver: Optional[Person] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            private_message_report=PrivateMessageReport.parse(data["private_message_report"]),
            private_message=PrivateMessage.parse(data["private_message"]),
            private_message_creator=Person.parse(data["private_message_creator"]),
            creator=Person.parse(data["creator"]),
            resolver=Person.parse(data["resolver"]) if "resolver" in data else None
        )


@dataclass
class ModAddView:
    """https://join-lemmy.org/api/interfaces/ModAddView.html"""

    mod_add: ModAdd = None
    moderator: Optional[Person] = None
    modded_person: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_add=ModAdd.parse(data["mod_add"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            modded_person=Person.parse(data["modded_person"])
        )


@dataclass
class PersonView:
    """https://join-lemmy.org/api/interfaces/PersonView.html"""

    person: Person = None
    counts: PersonAggregates = None
    is_admin: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person=Person.parse(data["person"]),
            counts=PersonAggregates.parse(data["counts"]),
            is_admin=data["is_admin"]
        )


@dataclass
class ModBanView:
    """https://join-lemmy.org/api/interfaces/ModBanView.html"""

    mod_ban: ModBan = None
    moderator: Optional[Person] = None
    banned_person: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_ban=ModBan.parse(data["mod_ban"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            banned_person=Person.parse(data["banned_person"])
        )


@dataclass
class RegistrationApplicationView:
    """https://join-lemmy.org/api/interfaces/RegistrationApplicationView.html"""

    registration_application: RegistrationApplication = None
    creator_local_user: LocalUser = None
    creator: Person = None
    admin: Optional[Person] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            registration_application=RegistrationApplication.parse(data["registration_application"]),
            creator_local_user=LocalUser.parse(data["creator_local_user"]),
            creator=Person.parse(data["creator"]),
            admin=Person.parse(data["admin"]) if "admin" in data else None
        )


@dataclass
class CommunityBlockView:
    """https://join-lemmy.org/api/interfaces/CommunityBlockView.html"""

    person: Person = None
    community: Community = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person=Person.parse(data["person"]),
            community=Community.parse(data["community"])
        )


@dataclass
class ModBanFromCommunityView:
    """https://join-lemmy.org/api/interfaces/ModBanFromCommunityView.html"""

    mod_ban_from_community: ModBanFromCommunity = None
    moderator: Optional[Person] = None
    community: Community = None
    banned_person: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_ban_from_community=ModBanFromCommunity.parse(data["mod_ban_from_community"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            community=Community.parse(data["community"]),
            banned_person=Person.parse(data["banned_person"])
        )


@dataclass
class PostView:
    """https://join-lemmy.org/api/interfaces/PostView.html"""

    post: Post = None
    creator: Person = None
    community: Community = None
    image_details: Optional[ImageDetails] = None
    creator_banned_from_community: bool = None
    banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    counts: PostAggregates = None
    subscribed: str = None
    saved: bool = None
    read: bool = None
    hidden: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None
    unread_comments: int = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post=Post.parse(data["post"]),
            creator=Person.parse(data["creator"]),
            community=Community.parse(data["community"]),
            image_details=ImageDetails.parse(data["image_details"]) if "image_details" in data else None,
            creator_banned_from_community=data["creator_banned_from_community"],
            banned_from_community=data["banned_from_community"],
            creator_is_moderator=data["creator_is_moderator"],
            creator_is_admin=data["creator_is_admin"],
            counts=PostAggregates.parse(data["counts"]),
            subscribed=data["subscribed"],
            saved=data["saved"],
            read=data["read"],
            hidden=data["hidden"],
            creator_blocked=data["creator_blocked"],
            my_vote=data["my_vote"] if "my_vote" in data else None,
            unread_comments=data["unread_comments"]
        )


@dataclass
class InstanceBlockView:
    """https://join-lemmy.org/api/interfaces/InstanceBlockView.html"""

    person: Person = None
    instance: Instance = None
    site: Optional[Site] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person=Person.parse(data["person"]),
            instance=Instance.parse(data["instance"]),
            site=Site.parse(data["site"]) if "site" in data else None
        )


@dataclass
class ModRemoveCommunityView:
    """https://join-lemmy.org/api/interfaces/ModRemoveCommunityView.html"""

    mod_remove_community: ModRemoveCommunity = None
    moderator: Optional[Person] = None
    community: Community = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_remove_community=ModRemoveCommunity.parse(data["mod_remove_community"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            community=Community.parse(data["community"])
        )


@dataclass
class ModHideCommunityView:
    """https://join-lemmy.org/api/interfaces/ModHideCommunityView.html"""

    mod_hide_community: ModHideCommunity = None
    admin: Optional[Person] = None
    community: Community = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_hide_community=ModHideCommunity.parse(data["mod_hide_community"]),
            admin=Person.parse(data["admin"]) if "admin" in data else None,
            community=Community.parse(data["community"])
        )


@dataclass
class ModRemoveCommentView:
    """https://join-lemmy.org/api/interfaces/ModRemoveCommentView.html"""

    mod_remove_comment: ModRemoveComment = None
    moderator: Optional[Person] = None
    comment: Comment = None
    commenter: Person = None
    post: Post = None
    community: Community = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_remove_comment=ModRemoveComment.parse(data["mod_remove_comment"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            comment=Comment.parse(data["comment"]),
            commenter=Person.parse(data["commenter"]),
            post=Post.parse(data["post"]),
            community=Community.parse(data["community"])
        )


@dataclass
class AdminPurgeCommentView:
    """https://join-lemmy.org/api/interfaces/AdminPurgeCommentView.html"""

    admin_purge_comment: AdminPurgeComment = None
    admin: Optional[Person] = None
    post: Post = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            admin_purge_comment=AdminPurgeComment.parse(data["admin_purge_comment"]),
            admin=Person.parse(data["admin"]) if "admin" in data else None,
            post=Post.parse(data["post"])
        )


@dataclass
class ModAddCommunityView:
    """https://join-lemmy.org/api/interfaces/ModAddCommunityView.html"""

    mod_add_community: ModAddCommunity = None
    moderator: Optional[Person] = None
    community: Community = None
    modded_person: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_add_community=ModAddCommunity.parse(data["mod_add_community"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            community=Community.parse(data["community"]),
            modded_person=Person.parse(data["modded_person"])
        )


@dataclass
class PersonBlockView:
    """https://join-lemmy.org/api/interfaces/PersonBlockView.html"""

    person: Person = None
    target: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person=Person.parse(data["person"]),
            target=Person.parse(data["target"])
        )


@dataclass
class CommunityModeratorView:
    """https://join-lemmy.org/api/interfaces/CommunityModeratorView.html"""

    community: Community = None
    moderator: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community=Community.parse(data["community"]),
            moderator=Person.parse(data["moderator"])
        )


@dataclass
class ModFeaturePostView:
    """https://join-lemmy.org/api/interfaces/ModFeaturePostView.html"""

    mod_feature_post: ModFeaturePost = None
    moderator: Optional[Person] = None
    post: Post = None
    community: Community = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_feature_post=ModFeaturePost.parse(data["mod_feature_post"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            post=Post.parse(data["post"]),
            community=Community.parse(data["community"])
        )


@dataclass
class PrivateMessageView:
    """https://join-lemmy.org/api/interfaces/PrivateMessageView.html"""

    private_message: PrivateMessage = None
    creator: Person = None
    recipient: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            private_message=PrivateMessage.parse(data["private_message"]),
            creator=Person.parse(data["creator"]),
            recipient=Person.parse(data["recipient"])
        )


@dataclass
class SiteView:
    """https://join-lemmy.org/api/interfaces/SiteView.html"""

    site: Site = None
    local_site: LocalSite = None
    local_site_rate_limit: LocalSiteRateLimit = None
    counts: SiteAggregates = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            site=Site.parse(data["site"]),
            local_site=LocalSite.parse(data["local_site"]),
            local_site_rate_limit=LocalSiteRateLimit.parse(data["local_site_rate_limit"]),
            counts=SiteAggregates.parse(data["counts"])
        )


@dataclass
class ModLockPostView:
    """https://join-lemmy.org/api/interfaces/ModLockPostView.html"""

    mod_lock_post: ModLockPost = None
    moderator: Optional[Person] = None
    post: Post = None
    community: Community = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_lock_post=ModLockPost.parse(data["mod_lock_post"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            post=Post.parse(data["post"]),
            community=Community.parse(data["community"])
        )


@dataclass
class MyUserInfo:
    """https://join-lemmy.org/api/interfaces/MyUserInfo.html"""

    local_user_view: LocalUserView = None
    follows: list[CommunityFollowerView] = None
    moderates: list[CommunityModeratorView] = None
    community_blocks: list[CommunityBlockView] = None
    instance_blocks: list[InstanceBlockView] = None
    person_blocks: list[PersonBlockView] = None
    discussion_languages: list[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            local_user_view=LocalUserView.parse(data["local_user_view"]),
            follows=[CommunityFollowerView.parse(e0) for e0 in data["follows"]],
            moderates=[CommunityModeratorView.parse(e0) for e0 in data["moderates"]],
            community_blocks=[CommunityBlockView.parse(e0) for e0 in data["community_blocks"]],
            instance_blocks=[InstanceBlockView.parse(e0) for e0 in data["instance_blocks"]],
            person_blocks=[PersonBlockView.parse(e0) for e0 in data["person_blocks"]],
            discussion_languages=[e0 for e0 in data["discussion_languages"]]
        )


@dataclass
class AdminPurgePersonView:
    """https://join-lemmy.org/api/interfaces/AdminPurgePersonView.html"""

    admin_purge_person: AdminPurgePerson = None
    admin: Optional[Person] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            admin_purge_person=AdminPurgePerson.parse(data["admin_purge_person"]),
            admin=Person.parse(data["admin"]) if "admin" in data else None
        )


@dataclass
class CommentReportView:
    """https://join-lemmy.org/api/interfaces/CommentReportView.html"""

    comment_report: CommentReport = None
    comment: Comment = None
    post: Post = None
    community: Community = None
    creator: Person = None
    comment_creator: Person = None
    counts: CommentAggregates = None
    creator_banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    creator_blocked: bool = None
    subscribed: str = None
    saved: bool = None
    my_vote: Optional[int] = None
    resolver: Optional[Person] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment_report=CommentReport.parse(data["comment_report"]),
            comment=Comment.parse(data["comment"]),
            post=Post.parse(data["post"]),
            community=Community.parse(data["community"]),
            creator=Person.parse(data["creator"]),
            comment_creator=Person.parse(data["comment_creator"]),
            counts=CommentAggregates.parse(data["counts"]),
            creator_banned_from_community=data["creator_banned_from_community"],
            creator_is_moderator=data["creator_is_moderator"],
            creator_is_admin=data["creator_is_admin"],
            creator_blocked=data["creator_blocked"],
            subscribed=data["subscribed"],
            saved=data["saved"],
            my_vote=data["my_vote"] if "my_vote" in data else None,
            resolver=Person.parse(data["resolver"]) if "resolver" in data else None
        )


@dataclass
class ModRemovePostView:
    """https://join-lemmy.org/api/interfaces/ModRemovePostView.html"""

    mod_remove_post: ModRemovePost = None
    moderator: Optional[Person] = None
    post: Post = None
    community: Community = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_remove_post=ModRemovePost.parse(data["mod_remove_post"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            post=Post.parse(data["post"]),
            community=Community.parse(data["community"])
        )


@dataclass
class CommunityView:
    """https://join-lemmy.org/api/interfaces/CommunityView.html"""

    community: Community = None
    subscribed: str = None
    blocked: bool = None
    counts: CommunityAggregates = None
    banned_from_community: bool = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            community=Community.parse(data["community"]),
            subscribed=data["subscribed"],
            blocked=data["blocked"],
            counts=CommunityAggregates.parse(data["counts"]),
            banned_from_community=data["banned_from_community"]
        )


@dataclass
class AdminPurgeCommunityView:
    """https://join-lemmy.org/api/interfaces/AdminPurgeCommunityView.html"""

    admin_purge_community: AdminPurgeCommunity = None
    admin: Optional[Person] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            admin_purge_community=AdminPurgeCommunity.parse(data["admin_purge_community"]),
            admin=Person.parse(data["admin"]) if "admin" in data else None
        )


@dataclass
class AdminPurgePostView:
    """https://join-lemmy.org/api/interfaces/AdminPurgePostView.html"""

    admin_purge_post: AdminPurgePost = None
    admin: Optional[Person] = None
    community: Community = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            admin_purge_post=AdminPurgePost.parse(data["admin_purge_post"]),
            admin=Person.parse(data["admin"]) if "admin" in data else None,
            community=Community.parse(data["community"])
        )


@dataclass
class ModTransferCommunityView:
    """https://join-lemmy.org/api/interfaces/ModTransferCommunityView.html"""

    mod_transfer_community: ModTransferCommunity = None
    moderator: Optional[Person] = None
    community: Community = None
    modded_person: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            mod_transfer_community=ModTransferCommunity.parse(data["mod_transfer_community"]),
            moderator=Person.parse(data["moderator"]) if "moderator" in data else None,
            community=Community.parse(data["community"]),
            modded_person=Person.parse(data["modded_person"])
        )


@dataclass
class LocalImageView:
    """https://join-lemmy.org/api/interfaces/LocalImageView.html"""

    local_image: LocalImage = None
    person: Person = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            local_image=LocalImage.parse(data["local_image"]),
            person=Person.parse(data["person"])
        )


@dataclass
class PersonMentionView:
    """https://join-lemmy.org/api/interfaces/PersonMentionView.html"""

    person_mention: PersonMention = None
    comment: Comment = None
    creator: Person = None
    post: Post = None
    community: Community = None
    recipient: Person = None
    counts: CommentAggregates = None
    creator_banned_from_community: bool = None
    banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    subscribed: str = None
    saved: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            person_mention=PersonMention.parse(data["person_mention"]),
            comment=Comment.parse(data["comment"]),
            creator=Person.parse(data["creator"]),
            post=Post.parse(data["post"]),
            community=Community.parse(data["community"]),
            recipient=Person.parse(data["recipient"]),
            counts=CommentAggregates.parse(data["counts"]),
            creator_banned_from_community=data["creator_banned_from_community"],
            banned_from_community=data["banned_from_community"],
            creator_is_moderator=data["creator_is_moderator"],
            creator_is_admin=data["creator_is_admin"],
            subscribed=data["subscribed"],
            saved=data["saved"],
            creator_blocked=data["creator_blocked"],
            my_vote=data["my_vote"] if "my_vote" in data else None
        )


@dataclass
class CustomEmojiView:
    """https://join-lemmy.org/api/interfaces/CustomEmojiView.html"""

    custom_emoji: CustomEmoji = None
    keywords: list[CustomEmojiKeyword] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            custom_emoji=CustomEmoji.parse(data["custom_emoji"]),
            keywords=[CustomEmojiKeyword.parse(e0) for e0 in data["keywords"]]
        )


@dataclass
class CommentView:
    """https://join-lemmy.org/api/interfaces/CommentView.html"""

    comment: Comment = None
    creator: Person = None
    post: Post = None
    community: Community = None
    counts: CommentAggregates = None
    creator_banned_from_community: bool = None
    banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    subscribed: str = None
    saved: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            comment=Comment.parse(data["comment"]),
            creator=Person.parse(data["creator"]),
            post=Post.parse(data["post"]),
            community=Community.parse(data["community"]),
            counts=CommentAggregates.parse(data["counts"]),
            creator_banned_from_community=data["creator_banned_from_community"],
            banned_from_community=data["banned_from_community"],
            creator_is_moderator=data["creator_is_moderator"],
            creator_is_admin=data["creator_is_admin"],
            subscribed=data["subscribed"],
            saved=data["saved"],
            creator_blocked=data["creator_blocked"],
            my_vote=data["my_vote"] if "my_vote" in data else None
        )


@dataclass
class PostReportView:
    """https://join-lemmy.org/api/interfaces/PostReportView.html"""

    post_report: PostReport = None
    post: Post = None
    community: Community = None
    creator: Person = None
    post_creator: Person = None
    creator_banned_from_community: bool = None
    creator_is_moderator: bool = None
    creator_is_admin: bool = None
    subscribed: str = None
    saved: bool = None
    read: bool = None
    hidden: bool = None
    creator_blocked: bool = None
    my_vote: Optional[int] = None
    unread_comments: int = None
    counts: PostAggregates = None
    resolver: Optional[Person] = None
    
    @classmethod
    def parse(cls, data: dict[str, Any]):
        return cls(
            post_report=PostReport.parse(data["post_report"]),
            post=Post.parse(data["post"]),
            community=Community.parse(data["community"]),
            creator=Person.parse(data["creator"]),
            post_creator=Person.parse(data["post_creator"]),
            creator_banned_from_community=data["creator_banned_from_community"],
            creator_is_moderator=data["creator_is_moderator"],
            creator_is_admin=data["creator_is_admin"],
            subscribed=data["subscribed"],
            saved=data["saved"],
            read=data["read"],
            hidden=data["hidden"],
            creator_blocked=data["creator_blocked"],
            my_vote=data["my_vote"] if "my_vote" in data else None,
            unread_comments=data["unread_comments"],
            counts=PostAggregates.parse(data["counts"]),
            resolver=Person.parse(data["resolver"]) if "resolver" in data else None
        )
